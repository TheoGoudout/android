#!/usr/bin/env python3
"""
check_manifest.py - resolve the /e/OS manifest + our local manifest the way `repo` would,
without syncing anything, and catch the errors that otherwise cost a crave build:

  * duplicate project paths (local manifest adds something /e/OS already has),
  * <remove-project> in the local manifest that matches nothing,
  * paths the FP4 device tree references (hardware/..., device/..., vendor/...) that no
    project provides (or that /e/OS's snippets/eos.xml removed).

Usage:
  tools/check_manifest.py --eos-branch a17 [--local local_manifests/a17] [--device-tree DIR]

--device-tree is a checkout of LineageOS/android_device_fairphone_FP4 at the matching branch;
without it only the manifest checks run. Exit code 1 if anything is wrong.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

EOS_MANIFEST_URL = os.environ.get("EOS_MANIFEST_URL", "https://gitlab.e.foundation/e/os/android.git")


def load(root_dir, rel, projects, removed, problems, origin):
    for el in ET.parse(os.path.join(root_dir, rel)).getroot():
        a = el.attrib
        if el.tag == "include":
            load(root_dir, a["name"], projects, removed, problems, origin)
        elif el.tag == "remove-project":
            hit = [p for p, v in projects.items()
                   if (a.get("path") and p == a["path"]) or (not a.get("path") and v["name"] == a.get("name"))]
            if not hit and a.get("optional") != "true":
                problems.append(f"{origin}/{rel}: remove-project {a} matches nothing")
            for p in hit:
                removed[p] = projects.pop(p)["name"]
        elif el.tag == "project":
            path = a.get("path", a["name"])
            if path in projects:
                problems.append(f"{origin}/{rel}: duplicate path {path} "
                                f"({projects[path]['name']} vs {a['name']})")
            projects[path] = {"name": a["name"], "origin": f"{origin}/{rel}",
                              "links": [c.get("dest") for c in el if c.tag in ("linkfile", "copyfile")]}
            removed.pop(path, None)


def tree_refs(tree):
    refs = set()
    pat = re.compile(r"\b((?:hardware|device|vendor)/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)")
    for dp, _, files in os.walk(tree):
        if "/.git" in dp:
            continue
        for f in files:
            if not f.endswith((".mk", ".bp", ".xml", ".txt", ".py")):
                continue
            for line in open(os.path.join(dp, f), errors="replace"):
                if line.lstrip().startswith("#"):
                    continue
                for m in pat.findall(line):
                    refs.add(m.rstrip("/."))
    return refs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eos-branch", required=True)
    ap.add_argument("--local", help="dir with local manifest XMLs (default local_manifests/<branch>)")
    ap.add_argument("--device-tree")
    ap.add_argument("--optional", nargs="*", default=[],
                    help="names from local_manifests/<branch>/optional/ to add, as OPTIONAL_MANIFESTS does")
    args = ap.parse_args()
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local = args.local or os.path.join(here, "local_manifests", args.eos_branch)

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "clone", "-q", "--depth=1", "-b", args.eos_branch, EOS_MANIFEST_URL, tmp], check=True)
        projects, removed, problems = {}, {}, []
        load(tmp, "default.xml", projects, removed, problems, "eos")
        eos_removed = dict(removed)
        for f in sorted(os.listdir(local)):
            if f.endswith(".xml"):
                load(local, f, projects, removed, problems, "local")
        for name in args.optional:
            load(os.path.join(local, "optional"), f"{name}.xml", projects, removed, problems, "optional")

    print(f">> {len(projects)} projects after local manifests; /e/OS removes {len(eos_removed)} LineageOS projects without replacing them")
    if args.device_tree:
        missing = []
        provided = set(projects) | {d for v in projects.values() for d in v["links"] if d}
        for ref in sorted(tree_refs(args.device_tree)):
            # a reference is satisfied if some project path is a prefix of it (or vice versa
            # for dirs like vendor/qcom/opensource that hold several projects)
            if any(ref == p or ref.startswith(p + "/") or p.startswith(ref + "/") for p in provided):
                continue
            # on-device paths (/vendor/etc/...) and kernel-tree defconfig paths, not source projects
            if ref.startswith(("vendor/etc", "vendor/lib", "vendor/bin", "vendor/firmware", "vendor/app",
                               "vendor/radio/", "vendor/lito-", "vendor/fairphone/FP4.config")):
                continue
            gone = [p for p in eos_removed if ref == p or ref.startswith(p + "/")]
            missing.append(f"{ref}" + (f"  (removed by /e/OS: {gone[0]})" if gone else ""))
        if missing:
            print(">> device-tree references with no project (check each; some are false positives such as"
                  " config-file names):")
            for m in missing:
                print(f"   {m}")
    for p in problems:
        print(f"!! {p}")
    print(">> OK" if not problems else f">> {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
