#!/usr/bin/env python3
"""colorcheck.py BASE: run inside a patched project checkout. Reports colours that BASE defined, the
series deleted, and something still references (DELETED-BUT-USED). Handles res/flag(...) dirs."""
# colorcheck.py: in the cwd repo, every @color/X and R.color.X reference must be defined locally
# (values*/ <color name>, res/color*/X.xml) or be referenced by the base commit (then it comes from a lib).
import os, re, subprocess, sys
base = sys.argv[1]
defined=set()
for root,_,fs in os.walk("."):
    if "/.git" in root: continue
    for f in fs:
        p=os.path.join(root,f)
        if re.search(r'/res[^/]*(/flag\([^)]*\))?/values[^/]*$', root) and f.endswith(".xml"):
            defined |= set(re.findall(r'<(?:color|item type="color")\s+name="([^"]+)"', open(p,errors="replace").read()))
        if re.search(r'/res[^/]*(/flag\([^)]*\))?/color[^/]*$', root): defined.add(os.path.splitext(f)[0])
refs=set()
for root,_,fs in os.walk("."):
    if "/.git" in root: continue
    for f in fs:
        if f.endswith((".xml",".java",".kt")):
            t=open(os.path.join(root,f),errors="replace").read()
            refs |= {(m, os.path.join(root,f)) for m in re.findall(r'(?<![\w*:])@color/([A-Za-z0-9_]+)', t)}
            refs |= {(m, os.path.join(root,f)) for m in re.findall(r'(?<![\w.])R\.color\.([A-Za-z0-9_]+)', t)}
basetext=subprocess.run(["git","grep","-h","-o","-E",r"(@color/|R\.color\.)[A-Za-z0-9_]+",base],capture_output=True,text=True).stdout
basedef=subprocess.run(["git","grep","-h","-o","-E",r'<color name="[A-Za-z0-9_]+"',base,"--","*/values*/*.xml"],capture_output=True,text=True).stdout
basedefined=set(re.findall(r'name="([^"]+)"',basedef))
basefiles=set(os.path.splitext(os.path.basename(l))[0] for l in subprocess.run(["git","ls-tree","-r","--name-only",base],capture_output=True,text=True).stdout.split() if re.search(r'/res[^/]*(/flag\([^)]*\))?/color[^/]*/',l))
missing={}
for name,f in refs:
    if name in defined: continue
    # defined at base but not now = we deleted it -> real problem; never defined at base = library color
    if name in basedefined or name in basefiles: missing.setdefault(name,[]).append(f)
for n,fs in sorted(missing.items()): print("DELETED-BUT-USED", n, fs[:3])
print(">>", len(missing), "problems")
