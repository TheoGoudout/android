#!/usr/bin/env bash
# tools/apply_test.sh [TARGET [WORKDIR]]: textual check that every patches/<TARGET>/ series applies
# to the current upstream tips, without an Android checkout (no compiler involved).
#
# For each patched project: shallow, blobless fetch of its upstream branch, sparse checkout of
# only the files the series touches, then the real apply-patches.sh (git am -3). Re-runnable:
# existing project dirs are re-fetched and reset. Prints apply-patches.sh's log; exit 1 on failure.
# Blob fixups are skipped (vendor/fairphone/FP4 is excluded): they need the real blobs.
#
# Note: with depth-1 clones apply-patches.sh cannot see older upstream commits, so a patch that
# upstream already merged under the same subject shows up as a conflict here instead of "= already has".
set -eo pipefail
TARGET="${1:-a17}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${2:-$HERE/../apply-test-$TARGET}"
PDIR="$HERE/patches/$TARGET"
mkdir -p "$WORK"; WORK="$(cd "$WORK" && pwd)"

# project path -> "<git url> <branch>" (table: tools/upstreams.txt)
upstream() {
  awk -v t="$TARGET" -v p="$1" '$1 == t && $2 == p { print $3, $4; f = 1 } END { exit !f }' "$HERE/tools/upstreams.txt" \
    || { echo "no upstream for $TARGET:$1 in tools/upstreams.txt" >&2; return 1; }
}

cd "$WORK"
find "$PDIR" -name '*.patch' -printf '%h\n' | sort -u | sed "s|^$PDIR/||" | while IFS= read -r proj; do
  read -r url branch < <(upstream "$proj")
  echo ">> $proj <- $url $branch"
  [ -d "$proj/.git" ] || { mkdir -p "$proj"; git -C "$proj" init -q; }
  git -C "$proj" am --abort >/dev/null 2>&1 || true
  git -C "$proj" fetch -q --depth 1 --filter=blob:none "$url" "+refs/heads/$branch:refs/remotes/up/$branch"
  # only the files the series touches (+ new files' parents come along automatically)
  sed -n 's|^diff --git a/\(.*\) b/.*|/\1|p' "$PDIR/$proj"/*.patch | sort -u > "$proj/.git/info/sparse-checkout.list"
  git -C "$proj" sparse-checkout set --no-cone --stdin < "$proj/.git/info/sparse-checkout.list" >/dev/null 2>&1
  git -C "$proj" checkout -q -f -B test "refs/remotes/up/$branch"
done
rm -f .eos-patched-projects
PATCH_EXCLUDE="vendor/fairphone/FP4 ${PATCH_EXCLUDE:-}" \
  GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=user.name GIT_CONFIG_VALUE_0=apply-test \
  GIT_CONFIG_KEY_1=user.email GIT_CONFIG_VALUE_1=apply-test@localhost \
  bash "$HERE/apply-patches.sh" apply "$PDIR"
echo ">> all patches/$TARGET series apply ($(find "$PDIR" -name '*.patch' | wc -l) patches)"
