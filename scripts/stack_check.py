#!/usr/bin/env python3
"""Read-only version report for a Claris FileMaker agentic stack.

Checks, in order: installed CadenceUX skills against versions.json, Claris's FileMaker Agentic
Development Kit (ADK) against Claris's ADK manifest, FileMaker Pro against ADK's minimum and the
public Claris feed, FileMaker Server's public release, and an ADK project if one is found. Runs
only `adk --version`, `adk doctor --json`, `adk standards --json` and (macOS) `mdfind`; it never
installs or updates anything.

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
# Where Claris's ADK installs: ~/Library/Application Support/ADK on macOS,
# %LOCALAPPDATA%\ADK on 64-bit Windows (supported since ADK 0.17.0).
if os.name == "nt":
    ADK_HOME = os.path.join(os.environ.get("LOCALAPPDATA", os.path.join(HOME, "AppData", "Local")), "ADK")
else:
    ADK_HOME = os.path.join(HOME, "Library", "Application Support", "ADK")


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
    # "same_as": one skill published under two names (fmp-dev-orchestrator is cadenceux-dx's
    # earlier name). Only one is needed, so neither is listed as missing while the other is
    # installed, and both being installed gets a note.
    twin = {}
    for n, d in latest.items():
        if isinstance(d, dict) and d.get("same_as"):
            twin[n], twin[d["same_as"]] = d["same_as"], n
    for name in sorted(set(latest) | set(found)):
        copies = found.get(name, [])
        if not copies and name in twin and (found.get(twin[name]) or latest.get(name, {}).get("same_as")):
            continue
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
            if name in twin and found.get(twin[name]):
                rows[-1]["note"] = f"same skill as {twin[name]}, which is also installed: keep one"
    return rows


# ---------- ADK ----------

ADK_MANIFEST = "https://downloads.claris.com/adk/manifest.json"
FMP_MINIMUM = "26.1"      # ADK works with FileMaker Pro 26.1 or later
FMS_MINIMUM = "26.1.1"    # files hosted on FileMaker Server need 26.1.1 or later


def find_adk():
    cands = [shutil.which("adk"), os.path.join(ADK_HOME, "bin", "adk.exe" if os.name == "nt" else "adk")]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return None


def legacy_adt():
    """An earlier ADT preview install left behind (it's replaced by ADK)."""
    found = []
    if shutil.which("adt"):
        found.append(shutil.which("adt"))
    for p in (os.path.join(HOME, "Library", "Application Support", "ADT"),):
        if os.path.isdir(p):
            found.append(p)
    return found


def check_adk(versions, project):
    out = {}
    adk = find_adk()
    old = legacy_adt()
    if old:
        out["legacy_adt"] = old
    if not adk:
        out.update(status="NOT FOUND", detail="Claris's ADK isn't installed on this machine (or not on PATH). "
                   "It needs FileMaker Pro " + FMP_MINIMUM + " or later.")
        return out, None
    out["path"] = adk
    _, so, se = run([adk, "--version"], timeout=30)
    m = re.search(r"(\d+\.\d+\.\d+)(?:\s*\((\d+)\))?", (so or "") + (se or ""))
    out["installed"] = m.group(1) if m else None
    out["build"] = m.group(2) if m and m.group(2) else None
    latest = None
    uc = read_json(os.path.join(ADK_HOME, "update-check.json")) or {}
    if uc.get("latestVersion"):
        latest, out["latest_checked_at"] = uc["latestVersion"], uc.get("checkedAt")
    man = fetch_json(ADK_MANIFEST)
    if isinstance(man, dict) and man.get("version"):
        latest = man["version"]
    out["latest"] = latest
    c = vcmp(out["installed"], latest)
    out["status"] = "UNKNOWN" if c is None else ("OK" if c == 0 else ("UPDATE" if c < 0 else "AHEAD"))
    code, so, se = run([adk, "doctor", "--json"], cwd=project or HOME, timeout=120)
    doctor = None
    try:
        doctor = json.loads(so) if so.strip() else None
    except ValueError:
        doctor = None
    if doctor:
        cp = doctor.get("claudePlugin") or {}
        out["claude_plugin"] = cp.get("installedVersion") if cp.get("registered") else None
        out["mcp"] = doctor.get("mcpVersion")
        out["fm_cli"] = bool(doctor.get("fmCliInstalled"))
        out["agents"] = [a.get("id") if isinstance(a, dict) else a for a in doctor.get("configuredAgents") or []]
        out["install"] = ((doctor.get("installState") or {}).get("lastRun") or {}).get("status")
        pv = out.get("claude_plugin")
        if pv and out["installed"] and vcmp(pv, out["installed"]) not in (0, None):
            out["plugin_mismatch"] = f"Claude Code plugin {pv} but ADK {out['installed']}: run adk install (ask first)."
    return out, doctor


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
    need = ((versions.get("requirements") or {}).get("adk") or {}).get("filemaker_pro") or FMP_MINIMUM
    plat = "Mac" if sys.platform == "darwin" else ("Win" if os.name == "nt" else None)
    apps = fmp_installed()
    newest = None
    for a in apps:
        if newest is None or (vcmp(a["version"], newest) or 0) > 0:
            newest = a["version"]
    out = {"installed": [a["version"] for a in apps], "newest_installed": newest, "adk_requires": need,
           "public_latest": feed_latest(feed, "FileMaker Pro", plat) if plat else None}
    if newest is None:
        out["status"] = "UNKNOWN"
        out["detail"] = "Couldn't read installed versions here. In FileMaker Pro: Help > About, or Get ( ApplicationVersion )."
    else:
        c = vcmp(newest, need)
        out["status"] = "UNKNOWN" if c is None else ("OK" if c >= 0 else "BELOW ADK MINIMUM")
        pl = out["public_latest"]
        if pl and (vcmp(newest, pl) or 0) > 0:
            out["note"] = f"{newest} is newer than Claris's public release {pl}: a testing build. Don't ship solutions that depend on it."
    fm = (doctor or {}).get("fileMaker") or {}
    if fm:
        out["agent_access"] = fm.get("overallStatus")
        out["agent_access_detail"] = [c.get("summary") or c.get("message") for c in fm.get("checks", [])
                                      if isinstance(c, dict) and c.get("status") not in ("ok", "pass")][:3]
        nd = (fm.get("notDiagnosed") or {}).get("reason")
        if nd:
            out["not_diagnosed"] = nd
    return out


# ---------- ADK project ----------

def find_project(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "adk.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def pkg_version(app_dir, name):
    for p in (os.path.join(app_dir, "node_modules", *name.split("/"), "package.json"),):
        j = read_json(p)
        if j and j.get("version"):
            return j["version"]
    return None


def check_project(project, adk_info):
    if not project:
        return None
    cfg = read_json(os.path.join(project, "adk.json")) or {}
    out = {"path": project, "standards_pack": (cfg.get("standards") or {}).get("pack"),
           "files": list((cfg.get("files") or {}).keys()), "apps": []}
    tmpl = read_json(os.path.join(ADK_HOME, "template", "vite-wv", "vendor", "@adk", "fmdapi", "package.template.json")) or {}
    out["adk_ships_fmdapi"] = tmpl.get("version")
    adk = adk_info.get("path")
    if adk:
        code, so, _ = run([adk, "standards", "--json"], cwd=project, timeout=60)
        try:
            st = json.loads(so) if so.strip() else {}
            out["standards_resolved"] = st.get("pack") or st
        except ValueError:
            pass
    for pj in sorted(glob.glob(os.path.join(project, "webviewer-apps", "*", "package.json"))):
        app_dir = os.path.dirname(pj)
        p = read_json(pj) or {}
        deps = dict(p.get("dependencies", {}), **p.get("devDependencies", {}))
        meta = p.get("adkMetadata") or p.get("adtMetadata") or {}
        app = {"app": os.path.basename(app_dir), "created_with": meta.get("initVersion"),
               "typescript": {"declared": deps.get("typescript"), "installed": pkg_version(app_dir, "typescript")}}
        flags = []
        for lib in ("@adk/fmdapi", "@adt/fmdapi"):
            if lib in deps:
                inst = pkg_version(app_dir, lib)
                app[lib] = {"declared": deps[lib], "installed": inst}
                if lib == "@adt/fmdapi":
                    flags.append("uses the old @adt/fmdapi package from the ADT preview: adk update in the app folder (ask first)")
                elif inst and out["adk_ships_fmdapi"] and (vcmp(inst, out["adk_ships_fmdapi"]) or 0) < 0:
                    flags.append(f"@adk/fmdapi {inst}; installed ADK ships {out['adk_ships_fmdapi']}: adk update (ask first)")
        cv = vcmp(app["created_with"], adk_info.get("installed"))
        if cv is not None and cv < 0:
            flags.append(f"created with ADK {app['created_with']}; ADK {adk_info.get('installed')} is installed")
        app["flags"] = flags
        out["apps"].append(app)
    out["components_hint"] = "With the file open in FileMaker Pro: adk components status --json (read-only)."
    return out


# ---------- report ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", help="ADK project folder (default: search upward from the current folder)")
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
    adk_info, doctor = check_adk(versions, project)
    me = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md")
    my_name, my_ver = frontmatter(me)
    my_latest = (versions.get("skills", {}).get(my_name or "cadenceux-dx") or {}).get("version")
    st = vcmp(my_ver, my_latest)
    report = {
        "this_skill": {"item": f"{my_name} (running copy)", "installed": my_ver, "latest": my_latest,
                       "status": "UNKNOWN" if st is None else ("OK" if st == 0 else ("UPDATE" if st < 0 else "AHEAD"))},
        "versions_json": {"updated": versions.get("updated"), "error": versions.get("_error")},
        "skills": check_skills(versions, None) if not versions.get("_error") else [],
        "adk": adk_info,
        "filemaker_pro": check_fmp(versions, feed, doctor),
        "filemaker_server": {"public_latest": feed_latest(feed, "FileMaker Server", "Linux") or feed_latest(feed, "FileMaker Server", "Mac"),
                             "adk_requires": FMS_MINIMUM,
                             "detail": "Files hosted for ADK need FileMaker Server " + FMS_MINIMUM + " or later. Installed servers "
                                       "are checked by cadenceux-fms-docker-setup (Docker) or the Admin Console."},
        "project": check_project(project, adk_info),
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
            note = f" ({r['note']})" if r.get("note") else ""
            p(f"- {r['item']} [{r['where']}]: {r['installed']} vs latest {r['latest']} -> {r['status']}{extra}{note}")
    ad = report["adk"]
    p("\n## Claris ADK")
    if ad.get("status") == "NOT FOUND":
        p(f"- {ad['detail']}")
    else:
        b = f" (build {ad['build']})" if ad.get("build") else ""
        p(f"- installed {ad.get('installed', '-')}{b}, latest {ad.get('latest') or 'unknown'} -> {ad.get('status')}")
        p(f"- Claude Code plugin {ad.get('claude_plugin') or 'not registered'}; MCP server {ad.get('mcp') or '-'}; "
          f"filemaker CLI {'installed' if ad.get('fm_cli') else 'missing'}; last install {ad.get('install') or '-'}")
        if ad.get("plugin_mismatch"):
            p(f"  ! {ad['plugin_mismatch']}")
    if ad.get("legacy_adt"):
        p(f"  ! Old ADT preview files found ({', '.join(ad['legacy_adt'])}). ADK replaces ADT; remove them (ask first).")
    fp = report["filemaker_pro"]
    p("\n## FileMaker Pro")
    counts = {}
    for v in fp["installed"]:
        counts[v] = counts.get(v, 0) + 1
    allv = ", ".join(f"{v} x{n}" if n > 1 else v for v, n in sorted(counts.items(), key=lambda kv: vparse(kv[0]) or ()))
    p(f"- newest installed {fp.get('newest_installed') or '?'} (all copies: {allv or '-'}); public latest "
      f"{fp.get('public_latest') or '?'}; ADK requires {fp.get('adk_requires')} -> {fp['status']}")
    if fp.get("note"):
        p(f"  {fp['note']}")
    if fp.get("agent_access"):
        p(f"- ADK connection: {fp['agent_access']}")
        for d in fp.get("agent_access_detail") or []:
            if d:
                p(f"  {d}")
    fs = report["filemaker_server"]
    p("\n## FileMaker Server")
    p(f"- public latest {fs['public_latest'] or '?'}. {fs['detail']}")
    pr = report["project"]
    p("\n## ADK project")
    if not pr:
        p("- none found in this folder or its parents (no adk.json)")
    else:
        p(f"- {pr['path']}: standards pack {pr.get('standards_pack') or 'none'}; connected files "
          f"{', '.join(pr['files']) or 'none'}; installed ADK ships @adk/fmdapi {pr.get('adk_ships_fmdapi') or '?'}")
        for app in pr["apps"]:
            p(f"  - app {app['app']}: created with {app['created_with'] or '?'}; TypeScript "
              f"{app['typescript']['installed'] or app['typescript']['declared']}")
            for fl in app["flags"]:
                p(f"    ! {fl}")
        p(f"  {pr['components_hint']}")
    p("\nNothing was installed or changed. Ask before running any update (adk upgrade, adk update, adk install, "
      "adk components reconcile, skill installs).")


if __name__ == "__main__":
    main()
