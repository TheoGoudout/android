#!/usr/bin/env python3
"""rescheck.py BASE: run inside a patched project checkout. Every XML changed since BASE parses, and
every @res / R.res reference on an added line is defined in the repo or already referenced at BASE
(then it comes from a library). No-compiler sanity check; prints MISSING lines."""
import os, re, subprocess, sys, xml.etree.ElementTree as ET
base = sys.argv[1]
run = lambda *a: subprocess.run(a, capture_output=True, text=True).stdout
files = run("git", "diff", "--name-only", "--diff-filter=AM", f"{base}..HEAD").split()
bad = 0
for f in files:
    if f.endswith(".xml"):
        try: ET.parse(f)
        except Exception as e: print("XML-PARSE", f, e); bad += 1
# defined resources in this repo
defined = set()
for root, _, fs in os.walk("."):
    if "/.git" in root: continue
    for fn in fs:
        p = os.path.join(root, fn)
        if "/res" in root and fn.endswith(".xml") and "/values" in root:
            for m in re.finditer(r'<(string|bool|integer|dimen|color|array|string-array|plurals|style|item)\s+name="([^"]+)"', open(p, errors="replace").read()):
                defined.add((("string" if m.group(1) in ("string","plurals","string-array","array") else m.group(1)), m.group(2)))
        if "/res" in root and "/values" not in root:
            kind = os.path.basename(root).split("-")[0]
            defined.add((kind, os.path.splitext(fn)[0]))
        if "/res" in root and fn.endswith(".xml"):
            for m in re.finditer(r'@\+id/([A-Za-z0-9_]+)', open(p, errors="replace").read()): defined.add(("id", m.group(1)))
# resources referenced anywhere at the base (= provided by libs if not defined locally)
basetext = run("git", "grep", "-h", "-o", "-E", r"(@(string|drawable|layout|xml|id|raw|dimen|color|bool|integer)/[A-Za-z0-9_]+|R\.(string|drawable|layout|xml|id|raw|dimen|color|bool|integer)\.[A-Za-z0-9_]+)", base, "--", "src", "res", "AndroidManifest.xml")
known = set(re.findall(r'[@R][./]?(string|drawable|layout|xml|id|raw|dimen|color|bool|integer)[/.]([A-Za-z0-9_]+)', basetext))
added = run("git", "diff", "-U0", f"{base}..HEAD", "--", "src", "res", "AndroidManifest.xml")
miss = set()
for line in added.splitlines():
    if not line.startswith("+") or line.startswith("+++"): continue
    for kind, name in re.findall(r'(?<![\w.])(?:@|R\.)(string|drawable|layout|xml|id|raw|dimen|color|bool|integer)[/.]([A-Za-z0-9_]+)', line):
        if (kind, name) not in defined and (kind, name) not in known: miss.add((kind, name))
for k, n in sorted(miss): print("UNRESOLVED", k, n)
print(f">> {len(files)} files, {bad} XML errors, {len(miss)} unresolved new references")
