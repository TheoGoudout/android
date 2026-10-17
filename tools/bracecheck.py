#!/usr/bin/env python3
"""
bracecheck.py [--base REV] FILE...: no-compiler sanity check for ported Java/Kotlin.

Counts {} () [] after stripping comments, strings and char literals and reports files where
they do not balance. The stripping is approximate (text blocks, regex literals), so with
--base REV (run inside the git repo) a file is only reported when its imbalance differs from
the same file at REV, i.e. when the port changed the balance.
"""
import re
import subprocess
import sys


def strip(src):
    src = re.sub(r'//[^\n]*', '', src)
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    src = re.sub(r'"""(?:.|\n)*?"""', '""', src)
    src = re.sub(r'"(?:\\.|[^"\\\n])*"', '""', src)
    src = re.sub(r"'(?:\\.|[^'\\\n])'", "''", src)
    return src


def balance(text):
    s = strip(text)
    return tuple(s.count(o) - s.count(c) for o, c in ("{}", "()", "[]"))


def main(argv):
    base = None
    if argv[:1] == ["--base"]:
        base, argv = argv[1], argv[2:]
    bad = 0
    for f in argv:
        cur = balance(open(f, errors="replace").read())
        ref = (0, 0, 0)
        if base:
            p = subprocess.run(["git", "show", f"{base}:{f}"], capture_output=True, text=True)
            if p.returncode == 0:
                ref = balance(p.stdout)
        if cur != ref:
            print("UNBALANCED", f, "delta {} () [] =", cur, "base =", ref)
            bad += 1
    print(">>", len(argv), "files,", bad, "imbalances")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
