#!/usr/bin/env bash
# Runs ON THE CRAVE BUILD NODE from the source root (called by remote-build.sh).
#   apply-patches.sh undo                reset every project patched last time (run before repo sync)
#   apply-patches.sh apply <patch-dir>   git am <patch-dir>/<project path>/*.patch onto each project
#                                        (skips projects listed in $PATCH_EXCLUDE)
# A ledger (.eos-patched-projects: "<path> <pre-patch HEAD>") lets `undo` restore exactly what
# repo had checked out, so the next sync updates those projects normally.
set -eo pipefail
LEDGER=.eos-patched-projects
mode="${1:?apply|undo}"

case "$mode" in
  undo)
    [ -f "$LEDGER" ] || exit 0
    while read -r proj head; do
      [ -e "$proj/.git" ] || continue
      git -C "$proj" am --abort >/dev/null 2>&1 || true
      git -C "$proj" reset -q --hard "$head"
      echo "   - $proj: reset to ${head:0:12}"
    done < "$LEDGER"
    rm -f "$LEDGER"
    ;;
  apply)
    pdir="${2:?patch dir}"
    [ -d "$pdir" ] || exit 0
    find "$pdir" -name '*.patch' -printf '%h\n' | sort -u | sed "s|^$pdir/||" | while IFS= read -r proj; do
      if [[ " ${PATCH_EXCLUDE:-} " == *" $proj "* ]]; then echo "   ~ $proj: excluded (PATCH_EXCLUDE)"; continue; fi
      [ -e "$proj/.git" ] || { echo ">> $pdir/$proj: no such project in the tree" >&2; exit 1; }
      grep -q "^$proj " "$LEDGER" 2>/dev/null || echo "$proj $(git -C "$proj" rev-parse HEAD)" >> "$LEDGER"
      have="$(git -C "$proj" log -1000 --format=%s)"
      for p in "$pdir/$proj"/*.patch; do
        subj="$(git mailinfo /dev/null /dev/null < "$p" | sed -n 's/^Subject: //p')"
        # Skip what upstream already carries (e.g. /e/OS ported it after we exported the series)
        if grep -qxF -- "$subj" <<<"$have"; then echo "   = $proj: already has: $subj"; continue; fi
        echo "   + $proj: $subj"
        GIT_COMMITTER_NAME=eos-builder GIT_COMMITTER_EMAIL=eos-builder@localhost \
          git -C "$proj" am -3 -q --keep-cr "$(realpath "$p")" \
          || { echo ">> $(basename "$p") does not apply to $proj: refresh the series" >&2; exit 1; }
      done
    done
    # Same-length string edits in synced proprietary blobs (what LineageOS's extract-files.py
    # blob_fixup().binary_regex_replace() does at extraction time). Done here on the build node,
    # so no blob or binary diff ever lives in this public repo. Format, tab-separated:
    #   <project path> <file in project> <old string> <new string>   (new is NUL-padded)
    fx="$pdir/blob-fixups.txt"
    [ -f "$fx" ] || exit 0
    grep -v '^#' "$fx" | while IFS=$'\t' read -r proj file old new; do
      [ -n "$proj" ] || continue
      if [[ " ${PATCH_EXCLUDE:-} " == *" $proj "* ]]; then echo "   ~ $proj: blob fixups excluded (PATCH_EXCLUDE)"; continue; fi
      [ -f "$proj/$file" ] || { echo ">> blob fixup: $proj/$file not found" >&2; exit 1; }
      grep -q "^$proj " "$LEDGER" 2>/dev/null || echo "$proj $(git -C "$proj" rev-parse HEAD)" >> "$LEDGER"
      python3 - "$proj/$file" "$old" "$new" <<'PY' || exit 1
import sys
path, old, new = sys.argv[1], sys.argv[2].encode(), sys.argv[3].encode()
if len(new) > len(old):
    sys.exit(f">> blob fixup: replacement longer than original in {path}")
new = new.ljust(len(old), b"\0")
data = open(path, "rb").read()
n = data.count(old)
if n == 0:
    print(f"   = {path}: already fixed or string absent" if new in data else f">> blob fixup: '{old.decode()}' not in {path}")
    sys.exit(0 if new in data else 1)
open(path, "wb").write(data.replace(old, new))
print(f"   * {path}: {old.decode()} -> {new.rstrip(chr(0).encode()).decode()} ({n}x)")
PY
    done
    ;;
  *) echo "usage: $0 undo | apply <patch-dir>" >&2; exit 1 ;;
esac
