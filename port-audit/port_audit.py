#!/usr/bin/env python3
"""
port_audit.py - measure what it takes to move /e/OS's patches to a newer LineageOS.

For every repository /e/OS forks (remote "e" in the /e/OS manifest), it:
  1. finds the matching upstream repo + revision in the OLD LineageOS manifest
     (the base /e/OS currently sits on) and in the NEW one (the port target),
  2. lists the commits /e/OS carries on top of the old base,
  3. drops those already present upstream in the new base (same subject line,
     e.g. security backports /e/OS had to carry itself),
  4. replays the remaining ones, in order, onto the new base with
     `git merge-tree` (no checkout, no build) and records which apply cleanly
     and which conflict.

It needs only git >= 2.40 and python3 and runs fine on a weak laptop: repos are
fetched as partial clones (blob:none), file contents are downloaded lazily only
for the files the /e/OS patches touch. Expect a few GB of disk in total,
dominated by frameworks/base history.

Usage:
  ./port_audit.py --eos-branch a16 --old lineage-23.0 --new lineage-24.0
  ./port_audit.py --eos-branch a16 --old lineage-23.0 --new lineage-23.2 \
                  --only frameworks/base packages/apps/Settings

Output: <workdir>/report-<eos>-to-<new>.md and .csv
"""
import argparse
import csv
import os
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET

EOS_MANIFEST_URL = os.environ.get("EOS_MANIFEST_URL", "https://gitlab.e.foundation/e/os/android.git")
LINEAGE_MANIFEST_URL = os.environ.get("LINEAGE_MANIFEST_URL", "https://github.com/LineageOS/android.git")


# --------------------------------------------------------------------------- git helpers
def git(*args, cwd=None, check=True, quiet=False):
    p = subprocess.run(["git", *args], cwd=cwd, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        if not quiet:
            sys.stderr.write(f"git {' '.join(args)}\n{p.stderr}\n")
        raise RuntimeError(f"git {args[0]} failed")
    return p


def require_git(minimum=(2, 40)):
    out = git("--version").stdout.split()[2]
    ver = tuple(int(x) for x in out.split(".")[:2] if x.isdigit())
    if ver < minimum:
        sys.exit(f"git >= {minimum[0]}.{minimum[1]} required (merge-tree --merge-base), found {out}")


# --------------------------------------------------------------------------- manifest parsing
class Manifest:
    """Minimal `repo` manifest resolver: remotes, default, include, project,
    remove-project (by name or path) and extend-project."""

    def __init__(self, root_dir, manifest_url):
        self.root_dir = root_dir
        self.manifest_url = manifest_url
        self.remotes = {}
        self.default = {}
        self.projects = []  # list of dicts, in declaration order
        self._load("default.xml")

    def _load(self, rel):
        tree = ET.parse(os.path.join(self.root_dir, rel))
        for el in tree.getroot():
            tag, a = el.tag, el.attrib
            if tag == "remote":
                self.remotes[a["name"]] = dict(a)
            elif tag == "default":
                self.default.update(a)
            elif tag == "include":
                self._load(a["name"])
            elif tag == "remove-project":
                name, path = a.get("name"), a.get("path")
                self.projects = [p for p in self.projects
                                 if not ((name and p["name"] == name and (not path or p["path"] == path))
                                         or (path and not name and p["path"] == path))]
            elif tag == "extend-project":
                for p in self.projects:
                    if p["name"] == a["name"] and ("path" not in a or p["path"] == a["path"]):
                        for k in ("revision", "remote", "dest-path"):
                            if k in a:
                                p[k if k != "dest-path" else "path"] = a[k]
            elif tag == "project":
                p = dict(a)
                p.setdefault("path", p["name"])
                self.projects.append(p)

    def resolve(self, p):
        remote_name = p.get("remote") or self.default.get("remote")
        remote = self.remotes[remote_name]
        fetch = remote["fetch"]
        if not urllib.parse.urlparse(fetch).scheme:          # relative fetch like ".."
            # same rule as `repo`: resolve against the manifest URL itself (".." on
            # https://github.com/LineageOS/android -> https://github.com/)
            base = self.manifest_url.rstrip("/")
            base = base[:-4] if base.endswith(".git") else base
            fetch = urllib.parse.urljoin(base, fetch)
        url = fetch.rstrip("/") + "/" + p["name"]
        rev = p.get("revision") or remote.get("revision") or self.default.get("revision")
        if rev and not rev.startswith("refs/") and len(rev) != 40:
            rev = "refs/heads/" + rev
        return {"path": p["path"], "name": p["name"], "remote": remote_name, "url": url, "rev": rev}

    def by_path(self):
        return {p["path"]: self.resolve(p) for p in self.projects}


def clone_manifest(url, branch, dest):
    if os.path.isdir(dest):
        git("fetch", "-q", "--depth=1", "origin", branch, cwd=dest)
        git("checkout", "-q", "FETCH_HEAD", cwd=dest)
    else:
        git("clone", "-q", "--depth=1", "-b", branch, url, dest)
    return dest


# --------------------------------------------------------------------------- per-repo audit
def ensure_repo(workdir, path):
    repo = os.path.join(workdir, "repos", path.replace("/", "__") + ".git")
    if not os.path.isdir(repo):
        os.makedirs(repo)
        git("init", "-q", "--bare", repo)
    return repo


def fetch_into(repo, label, url, rev):
    """Fetch `rev` from `url` as a promisor (partial) remote into refs/audit/<label>."""
    existing = git("remote", cwd=repo).stdout.split()
    if label in existing:
        git("remote", "set-url", label, url, cwd=repo)
    else:
        git("remote", "add", label, url, cwd=repo)
    git("config", f"remote.{label}.promisor", "true", cwd=repo)
    git("config", f"remote.{label}.partialclonefilter", "blob:none", cwd=repo)
    git("fetch", "-q", "--no-tags", "--filter=blob:none", label, f"+{rev}:refs/audit/{label}", cwd=repo)
    return f"refs/audit/{label}"


def audit_repo(workdir, eos_proj, old_proj, new_proj):
    res = {"path": eos_proj["path"], "eos_repo": eos_proj["name"], "status": "", "eos_commits": 0,
           "already_upstream": 0, "clean": 0, "conflicts": 0, "conflict_list": [], "note": ""}
    if eos_proj["remote"] == "e-priv":
        res["status"] = "private"
        res["note"] = "Private /e/OS repo (ssh): not publicly available."
        return res
    if old_proj is None:
        res["status"] = "eos-only"
        res["note"] = "Repo has no LineageOS counterpart at this path: no rebase, only build-test it."
        return res
    if new_proj is None:
        res["status"] = "gone-upstream"
        res["note"] = "Path no longer exists in the new LineageOS manifest: needs a manual decision."
        return res

    repo = ensure_repo(workdir, eos_proj["path"])
    try:
        e = fetch_into(repo, "eos", eos_proj["url"], eos_proj["rev"])
        old = fetch_into(repo, "old", old_proj["url"], old_proj["rev"])
        new = fetch_into(repo, "new", new_proj["url"], new_proj["rev"])
    except RuntimeError:
        res["status"] = "fetch-failed"
        res["note"] = "Could not fetch one of the refs (branch missing or network)."
        return res

    if git("merge-base", e, old, cwd=repo, check=False).returncode != 0:
        res["status"] = "unrelated"
        res["note"] = "No common history between /e/OS fork and old upstream."
        return res

    commits = git("rev-list", "--no-merges", "--reverse", f"{old}..{e}", cwd=repo).stdout.split()
    res["eos_commits"] = len(commits)
    upstream_subjects = set(git("log", "--no-merges", "--format=%s", f"{old}..{new}", cwd=repo).stdout.splitlines())

    cur = git("rev-parse", new, cwd=repo).stdout.strip()
    for c in commits:
        subject = git("log", "-1", "--format=%s", c, cwd=repo).stdout.strip()
        if subject in upstream_subjects:
            res["already_upstream"] += 1
            continue
        parents = git("rev-list", "--parents", "-n1", c, cwd=repo).stdout.split()[1:]
        if not parents:
            continue
        mt = git("merge-tree", "--write-tree", "--name-only", "--no-messages",
                 f"--merge-base={parents[0]}", cur, c, cwd=repo, check=False)
        lines = mt.stdout.splitlines()
        if mt.returncode == 0:
            tree = lines[0].strip()
            cur = git("commit-tree", tree, "-p", cur, "-m", subject, cwd=repo).stdout.strip()
            res["clean"] += 1
        elif mt.returncode == 1:
            files = [l for l in lines[1:] if l.strip()]
            res["conflicts"] += 1
            res["conflict_list"].append(f"{c[:12]} {subject}  [{', '.join(files[:4])}{' ...' if len(files) > 4 else ''}]")
        else:
            res["conflicts"] += 1
            res["conflict_list"].append(f"{c[:12]} {subject}  [merge-tree error: {mt.stderr.strip()[:120]}]")
    res["status"] = "ok"
    return res


# --------------------------------------------------------------------------- report
def write_report(workdir, args, results):
    stem = os.path.join(workdir, f"report-{args.eos_branch}-to-{args.new}")
    with open(stem + ".csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path", "status", "eos_commits", "already_upstream", "clean", "conflicts", "note"])
        for r in results:
            w.writerow([r["path"], r["status"], r["eos_commits"], r["already_upstream"],
                        r["clean"], r["conflicts"], r["note"]])
    tot = {k: sum(r[k] for r in results) for k in ("eos_commits", "already_upstream", "clean", "conflicts")}
    with open(stem + ".md", "w") as f:
        f.write(f"# /e/OS {args.eos_branch} ({args.old}) -> {args.new}\n\n")
        f.write(f"- forked repos audited: {len(results)}\n")
        f.write(f"- /e/OS commits on top of {args.old}: {tot['eos_commits']}\n")
        f.write(f"- already upstream in {args.new} (dropped): {tot['already_upstream']}\n")
        f.write(f"- apply cleanly: {tot['clean']}\n")
        f.write(f"- conflict (manual port): {tot['conflicts']}\n\n")
        f.write("| path | status | e commits | upstream | clean | conflicts |\n|---|---|---|---|---|---|\n")
        for r in sorted(results, key=lambda r: (-r["conflicts"], r["path"])):
            f.write(f"| {r['path']} | {r['status']} | {r['eos_commits']} | {r['already_upstream']} | "
                    f"{r['clean']} | {r['conflicts']} |\n")
        f.write("\n## Conflicting commits\n")
        for r in results:
            if r["conflict_list"]:
                f.write(f"\n### {r['path']}\n")
                for line in r["conflict_list"]:
                    f.write(f"- {line}\n")
        notes = [r for r in results if r["note"]]
        if notes:
            f.write("\n## Notes\n")
            for r in notes:
                f.write(f"- {r['path']}: {r['note']}\n")
    return stem


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eos-branch", default="a16", help="/e/OS manifest branch (default a16)")
    ap.add_argument("--old", default="lineage-23.0", help="LineageOS branch /e/OS is based on")
    ap.add_argument("--new", default="lineage-24.0", help="LineageOS branch to port to")
    ap.add_argument("--workdir", default="./audit-work")
    ap.add_argument("--only", nargs="*", help="restrict to these repo paths")
    args = ap.parse_args()

    require_git()
    os.makedirs(args.workdir, exist_ok=True)
    wd = os.path.abspath(args.workdir)

    print(">> fetching manifests")
    eos_dir = clone_manifest(EOS_MANIFEST_URL, args.eos_branch, os.path.join(wd, f"manifest-eos-{args.eos_branch}"))
    old_dir = clone_manifest(LINEAGE_MANIFEST_URL, args.old, os.path.join(wd, f"manifest-{args.old}"))
    new_dir = clone_manifest(LINEAGE_MANIFEST_URL, args.new, os.path.join(wd, f"manifest-{args.new}"))
    eos = Manifest(eos_dir, EOS_MANIFEST_URL)
    old = Manifest(old_dir, LINEAGE_MANIFEST_URL).by_path()
    new = Manifest(new_dir, LINEAGE_MANIFEST_URL).by_path()

    eos_projects = [eos.resolve(p) for p in eos.projects
                    if (p.get("remote") or eos.default.get("remote")) in ("e", "e-priv")]
    if args.only:
        eos_projects = [p for p in eos_projects if p["path"] in args.only]
    print(f">> {len(eos_projects)} /e/OS repos to audit")

    results = []
    for i, p in enumerate(eos_projects, 1):
        print(f"[{i}/{len(eos_projects)}] {p['path']}", flush=True)
        r = audit_repo(wd, p, old.get(p["path"]), new.get(p["path"]))
        print(f"    {r['status']}: {r['eos_commits']} e commits, {r['already_upstream']} upstream, "
              f"{r['clean']} clean, {r['conflicts']} conflicts", flush=True)
        results.append(r)

    stem = write_report(wd, args, results)
    print(f">> report: {stem}.md / {stem}.csv")


if __name__ == "__main__":
    main()
