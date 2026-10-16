#!/usr/bin/env python3
"""
port_series.py - cherry-pick a downstream patch series onto a new base and export what applies.

Takes the commits in SRC_REF that are not in OLD_REF (i.e. a downstream's own work), drops
those whose subject already exists in NEW_REF, then cherry-picks the rest, in order, onto
NEW_REF in a scratch worktree. Commits that conflict are skipped and listed; everything that
applied is written as `git format-patch` files (original authorship kept) into OUT_DIR.

Textual application only: nothing is compiled. Review the list before shipping a series.

  tools/port_series.py --repo https://github.com/LineageOS/android_device_fairphone_FP4 \\
      --old lineage-23.0 --new lineage-24.0 \\
      --src https://gitlab.e.foundation/e/devices/android_device_fairphone_FP4 --src-ref a16 \\
      --out patches/a17/device/fairphone/FP4 [--exclude SHA ...] [--only SHA ...]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def git(*a, cwd, check=True):
    p = subprocess.run(["git", *a], cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode:
        sys.exit(f"git {' '.join(a)} failed:\n{p.stderr}")
    return p


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="upstream URL holding --old and --new")
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--src", help="URL of the downstream fork (default: --repo)")
    ap.add_argument("--src-ref", required=True)
    ap.add_argument("--new-repo", help="URL holding --new if different from --repo (e.g. /e/OS a17 fork)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--exclude", nargs="*", default=[], help="commit SHA prefixes to leave out")
    ap.add_argument("--only", nargs="*", help="only consider these commit SHA prefixes")
    ap.add_argument("--cache", default=os.path.expanduser("~/.cache/port_series"))
    args = ap.parse_args()

    os.makedirs(args.cache, exist_ok=True)
    repo = os.path.join(args.cache, args.repo.rstrip("/").split("/")[-1].removesuffix(".git") + ".git")
    if not os.path.isdir(repo):
        git("init", "-q", "--bare", repo, cwd=args.cache)
    # Partial (blob:none) promisor remotes: blobs are fetched lazily, only for the files the
    # checkout and the cherry-picks touch. Keeps frameworks/base to a few GB instead of ~10.
    remotes = git("remote", cwd=repo).stdout.split()
    for name, url, ref in (("old", args.repo, args.old), ("new", args.new_repo or args.repo, args.new),
                           ("src", args.src or args.repo, args.src_ref)):
        git("remote", "set-url" if name in remotes else "add", name, url, cwd=repo)
        git("config", f"remote.{name}.promisor", "true", cwd=repo)
        git("config", f"remote.{name}.partialclonefilter", "blob:none", cwd=repo)
        git("fetch", "-q", "--no-tags", "--filter=blob:none", name, f"+refs/heads/{ref}:refs/ps/{name}", cwd=repo)

    commits = git("rev-list", "--no-merges", "--reverse", "refs/ps/old..refs/ps/src", cwd=repo).stdout.split()
    upstream = set(git("log", "--no-merges", "--format=%s", "refs/ps/old..refs/ps/new", cwd=repo).stdout.splitlines())

    wt = tempfile.mkdtemp(prefix="port_series-")
    git("worktree", "add", "-q", "--detach", wt, "refs/ps/new", cwd=repo)
    applied, skipped = [], []
    try:
        for c in commits:
            subj = git("log", "-1", "--format=%s", c, cwd=repo).stdout.strip()
            tag = f"{c[:12]} {subj}"
            if args.only and not any(c.startswith(x) for x in args.only):
                continue
            if any(c.startswith(x) for x in args.exclude):
                skipped.append(f"excluded   {tag}")
                continue
            if subj in upstream:
                skipped.append(f"upstream   {tag}")
                continue
            p = git("cherry-pick", "-x", "--allow-empty", c, cwd=wt, check=False)
            if p.returncode:
                files = git("diff", "--name-only", "--diff-filter=U", cwd=wt, check=False).stdout.split()
                git("cherry-pick", "--abort", cwd=wt, check=False)
                skipped.append(f"CONFLICT   {tag}  [{', '.join(files[:4])}]")
                continue
            if git("diff", "--quiet", "HEAD~1", "HEAD", cwd=wt, check=False).returncode == 0:
                git("reset", "-q", "--hard", "HEAD~1", cwd=wt)
                skipped.append(f"empty      {tag}")
                continue
            applied.append(tag)
        if os.path.isdir(args.out):
            shutil.rmtree(args.out)
        os.makedirs(args.out)
        if applied:
            git("format-patch", "-q", "--no-signature", "--zero-commit", "-o", os.path.abspath(args.out),
                "refs/ps/new..HEAD", cwd=wt)
    finally:
        git("worktree", "remove", "--force", wt, cwd=repo, check=False)

    print(f">> {len(applied)} applied, {len(skipped)} not applied")
    for t in applied:
        print(f"applied    {t}")
    for t in skipped:
        print(t)


if __name__ == "__main__":
    main()
