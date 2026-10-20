#!/usr/bin/env python3
"""
publish_forks.py - publish every patches/<target>/ series as a public fork branch, plus an
optional local manifest that builds from those forks instead of applying the patches.

patches/<target>/ stays the source of truth: each fork branch (default `a17-fp4`) is rebuilt
from scratch as <upstream tip> + <series>, by the same tools/apply_test.sh + apply-patches.sh
run that checks the series (committer date = author date, so an unchanged base and series give
the same commit ids, and re-publishing is a no-op). The fork's copy of the upstream branch is
also updated, so the fork stays a valid merge-request source. Blob fixups are not published
(proprietary blobs can't go into a public repo); apply-patches.sh still does them on the node.

Dry run by default: builds the branches, prints the GitLab API calls and pushes it would make,
writes the manifest to <workdir>/forks.xml and validates it. Nothing leaves the machine.

  tools/publish_forks.py [--target a17] [--namespace USER] [--only PATH ...] [--push]

--push needs $GITLAB_TOKEN (scope api) for --host. It creates missing forks (server-side fork for
repos on the same host, import by URL for the GitHub-hosted LineageOS repos), makes them public,
force-pushes the fork branch, then checks it anonymously with git ls-remote. Without --only it
also writes local_manifests/<target>/optional/forks.xml (OPTIONAL_MANIFESTS="forks" uses it).
The token is never printed or passed on a command line.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tools"))
import check_manifest  # noqa: E402

REMOTE = "fp4-forks"


def upstreams(target):
    rows = {}
    for line in open(os.path.join(HERE, "tools", "upstreams.txt")):
        f = line.split()
        if f and not f[0].startswith("#") and f[0] == target:
            rows[f[1]] = (f[2], f[3])
    return rows


def git(proj_dir, *args, env=None, check=True):
    return subprocess.run(["git", "-C", proj_dir, *args], check=check, text=True,
                          capture_output=True, env=env).stdout.strip()


class GitLab:
    def __init__(self, host, token, push):
        self.base = f"https://{host}/api/v4"
        self.token, self.push = token, push

    def call(self, method, path, data=None):
        if not self.push and method != "GET":
            print(f"   [dry-run] {method} {path} {json.dumps(data) if data else ''}")
            return None
        req = urllib.request.Request(self.base + path, method=method,
                                     data=json.dumps(data).encode() if data else None)
        req.add_header("Content-Type", "application/json")
        if self.token:
            req.add_header("PRIVATE-TOKEN", self.token)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404 and method == "GET":
                return None
            sys.exit(f"!! {method} {path}: HTTP {e.code} {e.read().decode(errors='replace')[:500]}")


def wait_import(gl, pid, what):
    for _ in range(240):
        p = gl.call("GET", f"/projects/{pid}")
        st = p.get("import_status", "none")
        if st in ("finished", "none"):
            return p
        if st == "failed":
            sys.exit(f"!! {what}: import failed: {p.get('import_error')}")
        time.sleep(15)
    sys.exit(f"!! {what}: import still running after 1 h; re-run later")


def ensure_project(gl, host, ns, name, url, ubranch):
    full = f"{ns}/{name}"
    enc = urllib.parse.quote(full, safe="")
    p = gl.call("GET", f"/projects/{enc}")
    if p is None:
        u = urllib.parse.urlparse(url)
        if u.hostname == host:
            src = urllib.parse.quote(u.path.strip("/").removesuffix(".git"), safe="")
            p = gl.call("POST", f"/projects/{src}/fork",
                        {"namespace_path": ns, "path": name, "name": name, "visibility": "public"})
        else:
            p = gl.call("POST", "/projects", {"path": name, "name": name, "visibility": "public",
                                              "import_url": url, "default_branch": ubranch})
        if p is None:  # dry run
            return
        p = wait_import(gl, p["id"], full)
    if p.get("visibility") != "public":
        gl.call("PUT", f"/projects/{p['id']}", {"visibility": "public"})


def push(proj_dir, host, token, ns, name, ubranch, branch, do_push):
    url = f"https://{host}/{ns}/{name}.git"
    refspecs = [f"+refs/remotes/up/{ubranch}:refs/heads/{ubranch}", f"+HEAD:refs/heads/{branch}"]
    if not do_push:
        print(f"   [dry-run] git push {url} {' '.join(refspecs)}")
        return
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_CONFIG_COUNT="1",
               GIT_CONFIG_KEY_0=f"http.https://{host}/.extraHeader",
               GIT_CONFIG_VALUE_0="Authorization: Basic "
               + base64.b64encode(f"oauth2:{token}".encode()).decode())
    # Shallow clone: the server must already have a common ancestor. Deepen until the fork's
    # current copy of the upstream branch is in our history (a fresh fork is at the tip already).
    have = git(proj_dir, "ls-remote", url, f"refs/heads/{ubranch}", env=env).split()
    if have:
        for depth in (50, 200, 1000, 5000, None):
            if subprocess.run(["git", "-C", proj_dir, "cat-file", "-e", f"{have[0]}^{{commit}}"],
                              capture_output=True).returncode == 0:
                break
            git(proj_dir, "fetch", "-q", *(["--deepen", str(depth)] if depth else ["--unshallow"]),
                "up", f"+refs/heads/{ubranch}:refs/remotes/up/{ubranch}")
        else:
            print(f"   !! {ubranch} on the fork is not an ancestor of upstream's (force-pushed upstream?)")
    r = subprocess.run(["git", "-C", proj_dir, "push", "-q", url, *refspecs], env=env,
                       text=True, capture_output=True)
    if r.returncode:
        sys.exit(f"!! push to {ns}/{name} failed:\n{r.stderr.replace(token, '***')}")
    anon = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="true")
    seen = git(proj_dir, "ls-remote", url, f"refs/heads/{branch}", env=anon, check=False).split()
    head = git(proj_dir, "rev-parse", "HEAD")
    print(f"   anonymous ls-remote: {'OK' if seen and seen[0] == head else 'MISMATCH ' + str(seen)}")
    if not seen or seen[0] != head:
        sys.exit(f"!! {ns}/{name}: {branch} not publicly visible at {head[:12]}")


def manifest(target, host, ns, branch, forks, out):
    """Write the forks manifest (attributes/children copied from the resolved /e/OS manifest),
    then resolve /e/OS + local manifests + it the way check_manifest.py does."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "clone", "-q", "--depth=1", "-b", target, check_manifest.EOS_MANIFEST_URL, tmp],
                       check=True)
        projects, removed, problems = {}, {}, []
        check_manifest.load(tmp, "default.xml", projects, removed, problems, "eos")
        local = os.path.join(HERE, "local_manifests", target)
        for f in sorted(os.listdir(local)):
            if f.endswith(".xml"):
                check_manifest.load(local, f, projects, removed, problems, "local")
        root = ET.Element("manifest")
        root.text = "\n  "
        ET.SubElement(root, "remote", name=REMOTE, fetch=f"https://{host}/")
        for path, name in forks:
            if path not in projects:
                problems.append(f"{path}: not in the /e/OS + local manifests")
                continue
            ET.SubElement(root, "remove-project", path=path)
            old = projects[path]["el"]
            attrs = {k: v for k, v in old.attrib.items()
                     if k not in ("name", "remote", "revision", "upstream", "dest-branch")}
            el = ET.SubElement(root, "project", path=path, name=f"{ns}/{name}", remote=REMOTE,
                               revision=branch, **{k: v for k, v in attrs.items() if k != "path"})
            el.extend(old)
        ET.indent(root, "  ")
        comment = (f"\n  Generated by tools/publish_forks.py: builds the {target} projects that carry\n"
                   f"  patches/{target}/ from public forks ({host}/{ns}, branch {branch}).\n"
                   f"  Enable with OPTIONAL_MANIFESTS=\"forks\" in build.sh. Do not edit by hand.\n")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as fh:
            fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<!--{comment}-->\n')
            fh.write(ET.tostring(root, encoding="unicode") + "\n")
        check_manifest.load(os.path.dirname(out), os.path.basename(out), projects, removed, problems, "forks")
        for path, name in forks:
            if projects.get(path, {}).get("name") != f"{ns}/{name}":
                problems.append(f"{path}: resolves to {projects.get(path, {}).get('name')}")
    for p in problems:
        print(f"!! manifest: {p}")
    print(f">> manifest {out}: {len(forks)} projects, {'OK' if not problems else 'PROBLEMS'}")
    return not problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", default="a17")
    ap.add_argument("--workdir", help="apply-test dir (default ../apply-test-<target>)")
    ap.add_argument("--host", default="gitlab.e.foundation")
    ap.add_argument("--namespace", help="fork owner (default: the token's user)")
    ap.add_argument("--branch", default="a17-fp4")
    ap.add_argument("--only", nargs="+", default=[], metavar="PATH", help="project paths (e.g. a probe)")
    ap.add_argument("--no-build", action="store_true", help="reuse the workdir as it is")
    ap.add_argument("--push", action="store_true", help="really create forks and push")
    args = ap.parse_args()
    work = os.path.abspath(args.workdir or os.path.join(HERE, "..", f"apply-test-{args.target}"))
    token = os.environ.get("GITLAB_TOKEN", "")
    if args.push and not token:
        sys.exit("!! --push needs $GITLAB_TOKEN")
    gl = GitLab(args.host, token, args.push)
    ns = args.namespace
    if not ns:
        me = gl.call("GET", "/user") if token else None
        if not me:
            sys.exit("!! --namespace needed (no usable $GITLAB_TOKEN)")
        ns = me["username"]
        if args.push and not me.get("can_create_project"):
            sys.exit(f"!! {args.host} user {ns} cannot create projects (projects_limit "
                     f"{me.get('projects_limit')}): ask the instance admins for a quota first")

    if not args.no_build:
        subprocess.run([os.path.join(HERE, "tools", "apply_test.sh"), args.target, work], check=True,
                       stdout=subprocess.DEVNULL)
    ups = upstreams(args.target)
    unknown = set(args.only) - set(ups)
    if unknown:
        sys.exit(f"!! not in tools/upstreams.txt: {' '.join(sorted(unknown))}")
    forks = []
    for path, (url, ubranch) in sorted(ups.items()):
        name = url.rstrip("/").rsplit("/", 1)[1].removesuffix(".git")
        forks.append((path, name))
        if args.only and path not in args.only:
            continue
        d = os.path.join(work, path)
        base = git(d, "rev-parse", f"refs/remotes/up/{ubranch}")
        n = git(d, "rev-list", "--count", f"{base}..HEAD")
        print(f">> {path}: {ns}/{name} {args.branch} = {url} {ubranch} @ {base[:12]} + {n} commit(s)"
              f" -> {git(d, 'rev-parse', 'HEAD')[:12]}")
        ensure_project(gl, args.host, ns, name, url, ubranch)
        push(d, args.host, token, ns, name, ubranch, args.branch, args.push)

    if args.only:
        print(">> --only: manifest not written")
        return 0
    out = (os.path.join(HERE, "local_manifests", args.target, "optional", "forks.xml") if args.push
           else os.path.join(work, "forks.xml"))
    return 0 if manifest(args.target, args.host, ns, args.branch, forks, out) else 1


if __name__ == "__main__":
    sys.exit(main())
