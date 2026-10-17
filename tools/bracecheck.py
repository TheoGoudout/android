import sys, re
def strip(src):
    # remove comments, strings, char literals
    src = re.sub(r'//[^\n]*', '', src)
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    src = re.sub(r'"(?:\\.|[^"\\])*"', '""', src)
    src = re.sub(r"'(?:\\.|[^'\\])'", "''", src)
    return src
bad = 0
for f in sys.argv[1:]:
    s = strip(open(f, errors="replace").read())
    for o, c in ("{}", "()", "[]"):
        if s.count(o) != s.count(c):
            print("UNBALANCED", o + c, f, s.count(o), s.count(c)); bad += 1
print(">>", len(sys.argv) - 1, "files,", bad, "imbalances")
