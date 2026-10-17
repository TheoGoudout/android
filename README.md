# /e/OS for Fairphone 4 — built for free on crave.io

Targets: `a16` (/e/OS on LineageOS 23.0, what FP4 ships today) or `a17` (/e/OS on
LineageOS 24.0, work in progress). See PORTING.md for why not `a16.2`.

## Why not GitHub Actions / GitLab CI

| Need (e/OS docs, A16) | GitHub free runner (public repo) |
|---|---|
| ≥ 400 GB disk (a real build writes ~336 GB) | 14 GB guaranteed, ~70 GB after deleting preinstalled tools |
| 16 GB RAM min, 32–64 GB realistic | 16 GB |
| ~6 h on an 8-core/16-thread i9 | 4 vCPU, 6 h hard job limit |

Cache is 10 GB/repo, so the 100+ GB `out/` can't be carried between jobs, and ccache
doesn't cover the Java/Kotlin/R8 half of the build. Projects that spawn Android builds
from GitHub-hosted runners have also had their Actions access restricted.
GitLab.com free (400 min/month, small runners) is far smaller. Cirrus CI (the old free
ROM-builder host) shut down on 2026-06-01. Oracle Always Free is ARM, and AOSP's host
toolchain is x86_64-only.

**crave.io's free FOSS tier** is the one free option sized for this: it's a build cluster
for open-source Android ROM builders, with a persistent workspace (synced source + `out/`
kept between builds → incremental rebuilds ~15–30 min).

## Setup (once)

1. Request an account: https://forms.gle/Jhvy9osvdmcS9B7fA (self sign-up is off;
   give name, email, GitHub profile). Join https://discord.crave.io.
2. Download `crave.conf` from foss.crave.io → API Keys, install the client:
   `curl -s https://raw.githubusercontent.com/accupara/crave/master/get_crave.sh | bash -s --`
3. This repo (public, `github.com/TheoGoudout/android`) is the local-manifests repo, with one
   branch per target named like the /e/OS branch: `a16` (baseline) and `a17` (main work).
   `build.sh` clones the branch matching `EOS_BRANCH` and uses `local_manifests/<target>/`.
   Tooling and docs are developed on `a17` and merged into `a16` when relevant. Public only:
   crave forbids private repos. (`default.xml`, `snippets/` and `README.mkdn` are the
   LineageOS 23.0 manifest this repo was forked from; the build does not use them.)
4. Run `crave clone list` and make the key in `crave.yaml` match the LOS 23.2 project name.
5. Edit the variables at the top of `build.sh`, then from inside `crave devspace`:
   `./build.sh setup`

## Each build

```
./build.sh build    # queues on crave, streams the log
./build.sh pull     # eos-latest-ota.zip + eos-latest-img.zip + SHA256SUMS
./build.sh log      # out/error.log after a failure
```

Your customisations = forks of the relevant repos, referenced from the local manifest.

## What a build applies on top of /e/OS

1. `local_manifests/<target>/*.xml`: FP4 device tree, kernel and blobs (LineageOS + TheMuppets).
2. `patches/<target>/<project path>/*.patch`: port work this project carries (see
   `patches/README.md`). `apply-patches.sh` applies them after sync, skips any patch the project
   already has, and undoes them before the next sync.
3. Optional, per build, set in `build.sh`:
   - `OPTIONAL_MANIFESTS="<name>"` adds `local_manifests/<target>/optional/<name>.xml`
   - `PATCH_EXCLUDE="packages/apps/Settings"` leaves that project's series out
   Change one of these per build iteration so a failure points at one cause.

## Tools (run anywhere with git + python3; no Android checkout needed)

- `port-audit/port_audit.py`: how much of an /e/OS branch's patch set moves to a new LineageOS.
- `tools/check_manifest.py --eos-branch a17 [--optional NAME] [--device-tree DIR]`: resolves the
  /e/OS manifest plus local manifests offline (duplicates, dangling removes, missing FP4 paths).
- `tools/port_series.py`: cherry-picks a downstream series onto a new base and exports what applies.

`PLAY_INTEGRITY.md`: what the build carries for Play Integrity BASIC and how to test it.
`UPSTREAM.md` lists where each patch should be merged so the series can shrink.

## Rules that will get you banned if ignored

- One queued build at a time, one device per build, one account.
- Never `make clean`, `rm -rf out` or casual `--clean` (destroys the shared incremental cache).
- Never `repo sync` or build inside devspace/`crave ssh` — only via `crave run`.
- No private repos.

## Notes

- `a16.2` exists in /e/OS's manifest but most of its forks are plain LineageOS 23.2 (no /e/OS
  changes), so building it gives you mostly LineageOS. Use `a16` or `a17`.
- `a16` on crave: synced on the LineageOS 23.2 base project (both Android 16). `a17` needs a
  LineageOS 24 base project; ask crave on discord for its ID.
- Builds are signed with **test keys**: flash with the bootloader **unlocked** and keep it
  unlocked. Don't relock it on a test-key build.
- `INCLUDE_IH8SN=true` adds /e/OS's prop-masking helper (normally only in community/official builds).
- Rename/rebrand if you distribute a build that changes features or default apps (e/OS
  "custom" category rules).
- `port-audit/` measures how much of /e/OS's patch set moves to a newer LineageOS (see PORTING.md).
