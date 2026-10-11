#!/usr/bin/env python3
"""Read-only version report for a Claris FileMaker agentic stack.

Checks, in order: installed CadenceUX skills against versions.json, Claris ADT, FileMaker Pro
(against ADT's minimum), the public Claris feed, and an ADT project if one is found. Runs only
`adt --version`, `adt doctor --json` and (macOS) `mdfind`; it never installs or updates anything.

Usage: python3 stack_check.py [--project PATH] [--json] [--offline] [--versions PATH_OR_URL]
Standard library only. Exit code is always 0; problems are reported, not raised.
"""
import argparse
import glob
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys
import urllib.request

VERSIONS_URL = "https://raw.githubusercontent.com/CadenceUX/cadenceux-skills/main/versions.json"
FEED_FALLBACK = "https://www.claris.com/cms/resources/downloads/updaters/product-updaters.txt"
HOME = os.path.expanduser("~")
ADT_HOME = os.path.join(HOME, "Library", "Application Support", "ADT", "MCP")


# ---------- helpers ----------

def vparse(s):
    """'v1.9' / '22.0.1' / '1.2.0-beta.1' / '2026 (26.0.3)' -> comparable tuple, or None."""
    if not s:
        return None
    s = str(s)
    m = re.search(r"\(([\d.]+)\)", s) or re.search(r"(\d+(?:\.\d+)*)(?:-([0-9A-Za-z.]+))?", s)
    if not m:
        return None
    nums = [int(x) for x in m.group(1).split(".") if x.isdigit()]
    nums = (nums + [0, 0, 0, 0])[:4]
    pre = m.group(2) if m.lastindex and m.lastindex >= 2 else None
    return tuple(nums) + ((0,) if pre else (1,))


def vnum(s):
    """'2026 (26.0.3)' -> '26.0.3'; other strings unchanged."""
    m = re.search(r"\(([\d.]+)\)", str(s or ""))
    return m.group(1) if m else s


def vcmp(a, b):
    pa, pb = vparse(a), vparse(b)
    if pa is None or pb is None:
        return None
    return (pa > pb) - (pa < pb)


def fetch_json(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "cadenceux-stack-check"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:  # noqa: BLE001 - report, never raise
        return {"_error": str(e)}


def run(cmd, cwd=None, timeout=90):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:  # noqa: BLE001
        return None, "", str(e)


def read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return None


def frontmatter(path):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read(6000)
    except Exception:  # noqa: BLE001
        return None, None
    if not text.startswith("---"):
        return None, None
    fm = text.split("\n---", 1)[0]
    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    ver = re.search(r"^\s*version:\s*[\"']?([^\"'\n]+)", fm, re.M)
    return (name.group(1) if name else None), (ver.group(1).strip() if ver else None)


# ---------- skills ----------

def skill_roots():
    roots = [("Claude Code personal skills", os.path.join(HOME, ".claude", "skills")),
             ("Claude Code project skills", os.path.join(os.getcwd(), ".claude", "skills"))]
    if sys.platform == "darwin":
        roots.append(("Claude desktop app / Cowork", os.path.join(HOME, "Library", "Application Support", "Claude")))
    elif os.name == "nt":
        roots.append(("Claude desktop app / Cowork", os.path.join(os.environ.get("APPDATA", ""), "Claude")))
    else:
        roots.append(("Claude desktop app / Cowork", os.path.join(HOME, ".config", "Claude")))
    return roots


def installed_skills(wanted):
    found = {}  # name -> list of {version, where, path, mtime}

    def add(name, ver, where, path):
        if name not in wanted:
            return
        try:
            mt = os.path.getmtime(path)
        except OSError:
            mt = 0
        found.setdefault(name, []).append({"version": ver, "where": where, "path": path, "mtime": mt})

    ip = read_json(os.path.join(HOME, ".claude", "plugins", "installed_plugins.json")) or {}
    for key, entries in (ip.get("plugins") or {}).items():
        name = key.split("@")[0]
        for e in entries or []:
            add(name, e.get("version"), "Claude Code plugin (" + key.split("@")[-1] + ")", e.get("installPath", key))

    for where, root in skill_roots():
        if not os.path.isdir(root):
            continue
        pattern = os.path.join(root, "**", "SKILL.md")
        for path in glob.glob(pattern, recursive=True):
            if "/plugins/cache/" in path.replace("\\", "/"):
                continue  # plugin installs are read from installed_plugins.json
            name, ver = frontmatter(path)
            if name:
                add(name, ver, where, path)
    return found


def check_skills(versions, wanted):
    rows = []
    latest = dict(versions.get("skills", {}))
    latest.update(versions.get("separate_installs", {}))
    outside = versions.get("outside_set", {})
    found = installed_skills(set(latest) | set(versions.get("retired", {})) | set(outside))
    for name in sorted(set(latest) | set(found)):
        copies = found.get(name, [])
        if name in outside:
            if copies:
                rows.append({"item": name, "status": "OUTSIDE SET", "installed": sorted({c["version"] or "?" for c in copies}),
                             "detail": outside[name]})
            continue
        if name in versions.get("retired", {}):
            if copies:
                rows.append({"item": name, "status": "REMOVE", "installed": sorted({c["version"] or "?" for c in copies}),
                             "detail": versions["retired"][name]})
            continue
        want = latest.get(name, {}).get("version")
        if not copies:
            rows.append({"item": name, "status": "NOT INSTALLED", "latest": want})
            continue
        by_where = {}
        for c in copies:
            if c["where"] not in by_where or c["mtime"] > by_where[c["where"]]["mtime"]:
                by_where[c["where"]] = c
        for where, c in sorted(by_where.items()):
            cmp = vcmp(c["version"], want)
            status = "UNKNOWN" if cmp is None else ("OK" if cmp == 0 else ("UPDATE" if cmp < 0 else "AHEAD"))
            n = sum(1 for x in copies if x["where"] == where)
            rows.append({"item": name, "where": where, "installed": c["version"], "latest": want, "status": status,
                         "copies": n, "versions_seen": sorted({x["version"] or "?" for x in copies if x["where"] == where})})
    return rows


# ---------- ADT ----------

def find_adt():
    cands = [shutil.which("adt")]
    ip = read_json(os.path.join(HOME, ".claude", "plugins", "installed_plugins.json")) or {}
    for e in (ip.get("plugins") or {}).get("filemaker-agentic-development@claris", []) or []:
        cands.append(os.path.join(e.get("installPath", ""), "bin", "adt"))
    cands.append(os.path.join(ADT_HOME, "bin", "adt"))
    for c in cands:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def adt_latest_from_feed(feed):
    best = None
    for e in feed if isinstance(feed, list) else []:
        prod = (e.get("product", "") + " " + e.get("name", "")).lower()
        if "agentic" in prod or re.search(r"\badt\b", prod):
            if best is None or (vcmp(e.get("version"), best) or 0) > 0:
                best = e.get("version")
    return vnum(best)


def adt_paths():
    ip = read_json(os.path.join(HOME, ".claude", "plugins", "installed_plugins.json")) or {}
    paths = [e.get("installPath", "") for e in (ip.get("plugins") or {}).get("filemaker-agentic-development@claris", []) or []]
    return [p for p in paths + [ADT_HOME] if p and os.path.isdir(p)]


def adt_fmp_minimum(doctor):
    """The FileMaker Pro version the installed ADT says it needs, read locally (never published)."""
    pat = re.compile(r"FileMaker Pro (\d+(?:\.\d+)+) or (?:newer|later)")
    texts = []
    for c in ((doctor or {}).get("fileMaker") or {}).get("checks", []):
        texts += [str(x) for x in c.get("remediation", []) + [c.get("summary", "")]]
    for t in texts:
        m = pat.search(t)
        if m:
            return m.group(1)
    found = {}
    for root in adt_paths():
        for path in glob.glob(os.path.join(root, "**", "*.md"), recursive=True)[:2000]:
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    for m in pat.finditer(f.read()):
                        found[m.group(1)] = found.get(m.group(1), 0) + 1
            except OSError:
                pass
    return max(found, key=lambda v: (found[v], vparse(v) or ())) if found else None


def check_adt(versions, feed, project):
    out = {"channel": (versions.get("tested_with", {}).get("adt") or {}).get("channel")}
    adt = find_adt()
    if not adt:
        out.update(status="NOT FOUND", detail="Claris ADT is not installed on this machine (or not on PATH).")
        return out, None
    out["path"] = adt
    _, so, se = run([adt, "--version"], timeout=30)
    out["installed"] = (re.search(r"\d+\.\d+\.\d+\S*", so + se) or [None])[0]
    latest = None
    if versions.get("sources", {}).get("adt_updates_feed"):
        f = fetch_json(versions["sources"]["adt_updates_feed"])
        latest = f.get("version") if isinstance(f, dict) else None
    latest = latest or adt_latest_from_feed(feed)
    out["latest_public"] = latest
    if latest:
        c = vcmp(out["installed"], latest)
        out["status"] = "UNKNOWN" if c is None else ("OK" if c == 0 else ("UPDATE" if c < 0 else "AHEAD"))
    else:
        out["status"] = "INSTALLED (preview)"
        out["detail"] = ("ADT is in Claris's preview programs and has no public update feed yet, so there's no "
                         "published latest version to compare with. Check the Developer Preview hub for new builds.")
    code, so, se = run([adt, "doctor", "--json"], cwd=project or HOME, timeout=120)
    doc = None
    try:
        doc = json.loads(so) if so.strip() else None
    except ValueError:
        doc = None
    out["doctor_stderr"] = [l.strip() for l in se.splitlines() if l.strip()][:5]
    return out, doc


# ---------- FileMaker Pro / Server ----------

def fmp_installed():
    apps = []
    if sys.platform != "darwin":
        return apps
    _, so, _ = run(["mdfind", "kMDItemCFBundleIdentifier == 'com.filemaker.client.pro12'"], timeout=30)
    for path in sorted(set(so.splitlines())):
        if "/.Trash/" in path or "/Previous/" in path:
            continue
        try:
            with open(os.path.join(path, "Contents", "Info.plist"), "rb") as f:
                apps.append({"path": path, "version": plistlib.load(f).get("CFBundleShortVersionString")})
        except Exception:  # noqa: BLE001
            pass
    return apps


def feed_latest(feed, product, platform_name):
    best = None
    for e in feed if isinstance(feed, list) else []:
        if e.get("product", "").strip().lower() == product.lower() and e.get("platform") == platform_name:
            if best is None or (vcmp(e.get("version"), best) or 0) > 0:
                best = e.get("version")
    return vnum(best)


def check_fmp(versions, feed, doctor):
    need = adt_fmp_minimum(doctor)
    plat = "Mac" if sys.platform == "darwin" else ("Win" if os.name == "nt" else None)
    apps = fmp_installed()
    newest = None
    for a in apps:
        if newest is None or (vcmp(a["version"], newest) or 0) > 0:
            newest = a["version"]
    out = {"installed": [a["version"] for a in apps], "newest_installed": newest, "adt_requires": need,
           "public_latest": feed_latest(feed, "FileMaker Pro", plat) if plat else None}
    if newest is None:
        out["status"] = "UNKNOWN"
        out["detail"] = "Couldn't read installed versions here. In FileMaker Pro: Help > About, or Get ( ApplicationVersion )."
    else:
        c = vcmp(newest, need) if need else None
        out["status"] = ("UNKNOWN (ADT minimum not found)" if c is None else
                         ("OK" if c >= 0 else "BELOW ADT MINIMUM"))
    if out.get("public_latest") and need and (vcmp(out["public_latest"], need) or 0) < 0:
        out["note"] = (f"Claris's public feed lists {out['public_latest']}; the build ADT needs comes from Claris's "
                       "preview program. Get it from the Developer Preview hub, not the public updater.")
    fm = (doctor or {}).get("fileMaker") or {}
    if fm:
        out["agent_access"] = fm.get("overallStatus")
        out["agent_access_detail"] = [c.get("summary") for c in fm.get("checks", []) if c.get("status") != "ok"][:3]
    return out


# ---------- ADT project ----------

def find_project(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "adt.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def pkg_version(app_dir, name):
    for p in (os.path.join(app_dir, "node_modules", name, "package.json"),
              os.path.join(app_dir, "node_modules", *name.split("/"), "package.json")):
        j = read_json(p)
        if j and j.get("version"):
            return j["version"]
    return None


def check_project(project, adt_info, doctor):
    if not project:
        return None
    out = {"path": project, "apps": []}
    tmpl = read_json(os.path.join(ADT_HOME, "template", "vite-wv", "vendor", "@adt", "fmdapi", "package.template.json")) or {}
    out["adt_ships_fmdapi"] = tmpl.get("version")
    root_vendor = read_json(os.path.join(project, "vendor", "@adt", "fmdapi", "package.json")) or {}
    for pj in sorted(glob.glob(os.path.join(project, "webviewer-apps", "*", "package.json"))):
        app_dir = os.path.dirname(pj)
        p = read_json(pj) or {}
        deps = dict(p.get("dependencies", {}), **p.get("devDependencies", {}))
        app = {"app": os.path.basename(app_dir),
               "created_with_adt": (p.get("adtMetadata") or {}).get("initVersion"),
               "typescript": {"declared": deps.get("typescript"), "installed": pkg_version(app_dir, "typescript")},
               "node_required": (p.get("engines") or {}).get("node")}
        for lib in ("@adt/fmdapi", "@proofkit/fmdapi"):
            if lib in deps:
                inst = pkg_version(app_dir, lib) or (root_vendor.get("version") if lib == "@adt/fmdapi" else None)
                app[lib] = {"declared": deps[lib], "installed": inst}
        flags = []
        cv = vcmp(app["created_with_adt"], adt_info.get("installed"))
        if cv is not None and cv < 0:
            flags.append(f"created with ADT {app['created_with_adt']}; ADT {adt_info.get('installed')} is installed")
        fd = (app.get("@adt/fmdapi") or {}).get("installed")
        if fd and out["adt_ships_fmdapi"] and (vcmp(fd, out["adt_ships_fmdapi"]) or 0) < 0:
            flags.append(f"@adt/fmdapi {fd}; installed ADT ships {out['adt_ships_fmdapi']}")
        app["flags"] = flags
        out["apps"].append(app)
    stale = [l for l in adt_info.get("doctor_stderr", []) if "out of date" in l.lower()]
    if stale:
        out["agents_md"] = stale[0]
    if doctor:
        out["node"] = doctor.get("nodeVersion")
        out["pnpm"] = doctor.get("pnpmVersion")
    out["components_hint"] = "With the file open in FileMaker Pro: adt components status --json (read-only)."
    return out


# ---------- report ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", help="ADT project folder (default: search upward from the current folder)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--offline", action="store_true", help="skip network fetches")
    ap.add_argument("--versions", help="versions.json path or URL (default: the cadenceux-skills repo)")
    a = ap.parse_args()

    src = a.versions or VERSIONS_URL
    if src and os.path.isfile(src):
        versions = read_json(src) or {"_error": "unreadable " + src}
    else:
        versions = {} if a.offline else fetch_json(src)
    if not isinstance(versions, dict) or versions.get("_error"):
        versions = {"_error": (versions or {}).get("_error", "unavailable")}
    feed_url = (versions.get("sources") or {}).get("claris_updates_feed") or FEED_FALLBACK
    feed = [] if a.offline else fetch_json(feed_url)
    if isinstance(feed, dict):
        feed = []

    project = a.project or find_project(os.getcwd())
    adt_info, doctor = check_adt(versions, feed, project)
    me = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md")
    _, my_ver = frontmatter(me)
    my_latest = (versions.get("skills", {}).get("fmp-dev-orchestrator") or {}).get("version")
    report = {
        "this_skill": {"item": "fmp-dev-orchestrator (running copy)", "installed": my_ver, "latest": my_latest,
                       "status": "UNKNOWN" if vcmp(my_ver, my_latest) is None else
                       ("OK" if vcmp(my_ver, my_latest) == 0 else ("UPDATE" if vcmp(my_ver, my_latest) < 0 else "AHEAD"))},
        "versions_json": {"updated": versions.get("updated"), "error": versions.get("_error")},
        "skills": check_skills(versions, None) if not versions.get("_error") else [],
        "adt": adt_info,
        "filemaker_pro": check_fmp(versions, feed, doctor),
        "filemaker_server": {"public_latest": feed_latest(feed, "FileMaker Server", "Linux") or feed_latest(feed, "FileMaker Server", "Mac"),
                             "tested_with": versions.get("tested_with", {}).get("filemaker_server", {}).get("version"),
                             "detail": "Installed servers are checked by cadenceux-fms-docker-setup (Docker) or the Admin Console."},
        "project": check_project(project, adt_info, doctor),
        "read_only": True,
    }
    if a.json:
        print(json.dumps(report, indent=2, default=str))
        return

    p = print
    p("# FileMaker stack check (read-only)\n")
    if versions.get("_error"):
        p(f"versions.json unavailable ({versions['_error']}); skill versions not compared.\n")
    ts = report["this_skill"]
    p("## CadenceUX skills")
    p(f"- {ts['item']}: {ts['installed']} vs latest {ts['latest']} -> {ts['status']}")
    for r in report["skills"]:
        if r["status"] == "NOT INSTALLED":
            p(f"- {r['item']}: not installed (latest {r['latest']})")
        elif r["status"] in ("REMOVE", "OUTSIDE SET"):
            p(f"- {r['item']}: {r['status']}, {r['detail']} Found: {', '.join(r['installed'])}")
        else:
            extra = (f"; {r['copies']} copies, versions seen {', '.join(r['versions_seen'])} (the newest copy is shown)"
                     if r["copies"] > 1 else "")
            p(f"- {r['item']} [{r['where']}]: {r['installed']} vs latest {r['latest']} -> {r['status']}{extra}")
    ad = report["adt"]
    p("\n## Claris ADT")
    p(f"- installed {ad.get('installed', '-')}, public latest {ad.get('latest_public') or 'none published'} -> {ad.get('status')}")
    if ad.get("detail"):
        p(f"  {ad['detail']}")
    fp = report["filemaker_pro"]
    p("\n## FileMaker Pro")
    counts = {}
    for v in fp["installed"]:
        counts[v] = counts.get(v, 0) + 1
    allv = ", ".join(f"{v} x{n}" if n > 1 else v for v, n in sorted(counts.items(), key=lambda kv: vparse(kv[0]) or ()))
    p(f"- newest installed {fp.get('newest_installed') or '?'} (all copies: {allv or '-'}); ADT requires {fp.get('adt_requires')} -> {fp['status']}")
    if fp.get("note"):
        p(f"  {fp['note']}")
    if fp.get("agent_access"):
        p(f"- Agent Access / connection: {fp['agent_access']}")
        for d in fp.get("agent_access_detail") or []:
            p(f"  {d}")
    fs = report["filemaker_server"]
    p("\n## FileMaker Server")
    p(f"- public latest {fs['public_latest']}, tested with {fs['tested_with']}. {fs['detail']}")
    pr = report["project"]
    p("\n## ADT project")
    if not pr:
        p("- none found in this folder or its parents (no adt.json)")
    else:
        p(f"- {pr['path']} (node {pr.get('node')}, pnpm {pr.get('pnpm')}; installed ADT ships @adt/fmdapi {pr.get('adt_ships_fmdapi')})")
        if pr.get("agents_md"):
            p(f"  {pr['agents_md']}")
        for app in pr["apps"]:
            libs = ", ".join(f"{k} {v.get('installed') or v.get('declared')}" for k, v in app.items() if k.endswith("fmdapi"))
            p(f"  - app {app['app']}: created with ADT {app['created_with_adt']}; TypeScript {app['typescript']['installed'] or app['typescript']['declared']}; {libs}")
            for fl in app["flags"]:
                p(f"    ! {fl}")
        p(f"  {pr['components_hint']}")
    p("\nNothing was installed or changed. Ask before running any update (adt update, adt components reconcile, skill installs).")


if __name__ == "__main__":
    main()
