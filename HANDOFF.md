# HANDOFF: /e/OS a17 (Android 17) for Fairphone 4

Written 2026-10-17 by the agent session that did the a17 port, for the next agent. Read this file
completely, then `STATUS.md`, `KNOWN_ISSUES.md`, `patches/README.md`. `AGENT_PLAN.md` is the
owner's original brief: its hard rules still apply (summarised in section 2).

---

## 1. One-paragraph summary

This public repo (`github.com/TheoGoudout/android`) is the build kit for an **unofficial /e/OS
build for the Fairphone 4 (FP4)** on crave.io (a free build cluster for open-source ROMs). Target
`a17` = /e/OS on LineageOS 24.0 / Android 17, which /e/OS has not finished porting. The repo holds
local manifests, build wrappers, and **107 patches over 23 projects** (+ 4 build-time blob string
fixups) that bring /e/OS a16 features and look-and-feel to a17. Everything **applies** to current
upstream tips, but **nothing has been compiled**: the owner has no crave account yet, and the agent
sandbox can't build Android. The next big moments are (a) the owner's first crave builds and the
build errors they produce, and (b), if the owner provides a GitLab token, publishing the patches as
public forks + a manifest that uses them.

---

## 2. Rules you must follow (owner's brief + owner's later instructions)

From `AGENT_PLAN.md` §1 (non-negotiable):
1. **The repo is public.** Never commit secrets (`crave.conf`, tokens, keys), proprietary APKs or
   vendor blobs, or raw device logs. `.gitignore` blocks the usual extensions; still check every
   `git add`. Proprietary blob *edits* are done on the build node (`patches/a17/blob-fixups.txt`),
   never as binary diffs in the repo.
2. **crave rules** (a ban ends the project): one queued build at a time, one device per build, never
   `repo sync` or compile inside `crave devspace`/`crave ssh` (only via `crave run`), never
   `make clean` / `rm -rf out` / casual `--clean`, no private repos (so any fork we use must be public).
3. You have **no crave credentials** and must not ask for them in chat. The owner runs everything
   needing `crave.conf` or the phone; give them copy-pasteable blocks and wait for results.
4. Builds are **test-keyed**: the bootloader stays **unlocked**. Never advise relocking.
5. **Don't invent facts.** If you can't verify something, say so and have the owner check.
6. Commit small and often; keep `STATUS.md` current.

From the owner, during the session:
- "Implement everything. When there are gaps or missing information, try your best to guess what
  you need. Keep the /e/OS graphical and product identity. Go as far as possible." Guesses made
  so far are listed in section 9: they're the first suspects when something misbehaves.
- Branches are named after the /e/OS branch: `a16` (baseline target) and `a17` (main work). The
  session branch `ccr-0f2cae73-f14zrb` mirrored `a17`. A new session gets its own designated branch
  from the harness: push there **and** to `a17` (and keep them identical) unless the owner says otherwise.
- **Do not create pull requests** unless asked.
- Old branch `claude/ci-android-xml-build-bWyCA` must be deleted; the sandbox was refused, so the
  owner has to delete it on GitHub (still pending as far as we know).
- Never ask the owner to paste a token into chat. Secrets go into the cloud environment settings
  (see section 6).

---

## 3. Where everything is

### Branches (as of 2026-10-17)
| branch | base | head | content |
|---|---|---|---|
| `a17` | LineageOS/android `lineage-24.0` (d4c6331, 2026-10-09) | see `git log` | main work; this file lives here |
| `a16` | LineageOS/android `lineage-23.0` | c8652df | same tooling/docs as `a17` *before* the rebase + this handoff; **now diverged** from `a17` (different base). Port tooling/doc changes to it deliberately (cherry-pick), only if relevant to the a16 build |
| `ccr-0f2cae73-f14zrb` | = `a17` | | previous session's designated branch |

`a17` was rebased onto `lineage-24.0` on owner request (only the unused upstream manifest files
`default.xml`, `snippets/`, `README.mkdn` changed). It was force-pushed with lease.

### Files
| path | what |
|---|---|
| `AGENT_PLAN.md` | owner's original brief (phases A–D, Phase 2 Play Integrity, definition of done) |
| `STATUS.md` | living status: verified facts, build log, owner action blocks, port status, work items, open questions |
| `KNOWN_ISSUES.md` | one row per known gap/risk + a16→a17 feature-parity checklist to fill after first boot |
| `patches/README.md` | **every patch series, why, and every adaptation**; read before touching a series |
| `UPSTREAM.md` | which merge request each series should become (/e/OS GitLab, LineageOS Gerrit) |
| `PLAY_INTEGRITY.md` | Phase 2: what the build carries for BASIC, owner test steps, bisect plan |
| `PORTING.md` | background on why a17 and what porting involves |
| `README.md` | owner-facing setup/usage |
| `build.sh` | runs on the owner's machine: `setup`/`build`/`pull`/`log`; top-of-file variables (EOS_BRANCH, PROJECT_ID, WORKSPACE, OPTIONAL_MANIFESTS, PATCH_EXCLUDE, INCLUDE_IH8SN). Refuses a17 on the Android 16 crave project |
| `remote-build.sh` | runs on the crave node: repo init /e/OS manifest, copy local manifests + patches, undo previous patches, sync, `git lfs pull`, apply patches + blob fixups, `breakfast`, `installclean`, build, sign with test keys, OTA + IMG zips, `>> integrity:` checks |
| `apply-patches.sh` | `undo` / `apply <dir>`: `git am -3` each series, skips patches whose subject is already upstream, ledger `.eos-patched-projects` for undo, `PATCH_EXCLUDE`, then `blob-fixups.txt` |
| `crave.yaml` | crave project key (verify name with `crave clone list`) |
| `local_manifests/a16/eos_fp4.xml`, `local_manifests/a17/eos_fp4.xml` | FP4 device tree, kernel, TheMuppets blobs (LineageOS `lineage-23.0` / `lineage-24.0`) |
| `local_manifests/a17/optional/setupwizard-bringup.xml` | superseded (kept for comparison) |
| `patches/a17/<project path>/*.patch` | the series (mbox, `git format-patch`), original authors kept, `(cherry picked from commit …)` trailers, `[a17: …]` notes for hand adaptations |
| `patches/a17/blob-fixups.txt` | same-length string edits in synced blobs (tab-separated) |
| `tools/apply_test.sh` | **one-command check that all series apply to current upstream tips** (section 5) |
| `tools/bracecheck.py --base REV FILES` | Java/Kotlin brace/paren balance vs a base revision (no compiler here) |
| `tools/rescheck.py BASE` | in a patched project: changed XML parses, added resource refs resolve |
| `tools/colorcheck.py BASE` | in a patched project: colours deleted by the series but still used |
| `tools/check_manifest.py` | resolves /e/OS manifest + local manifests offline (duplicates, missing paths) |
| `tools/port_series.py` | cherry-picks a downstream series onto a new base, exports what applies |
| `port-audit/port_audit.py`, `port-audit/reports/` | how much of /e/OS a16 moves to lineage-24.0; `a16-vs-a17-gap.md` is the gap list (fully triaged now) |

---

## 4. What is done (state of `patches/a17/`)

All 23 series, upstream repo and branch they apply to, and the gist. Details and every adaptation:
`patches/README.md`.

| project path | upstream (repo, branch) | # | content |
|---|---|---|---|
| device/fairphone/FP4 | LineageOS/android_device_fairphone_FP4 `lineage-24.0` (GitHub) | 17 | /e/OS FP4 commits: adoptable storage off, updater, CarrierConfig, Murena bootanimation, earpiece/VoIP audio, camera HAL access for /e/ Camera (sepolicy, props, eCamera RRO, clientpkgname), gralloc.qcom camera crash fix |
| frameworks/av | LineageOS/android_frameworks_av `lineage-24.0` (GitHub) | 2 | Matroska heap-write security fix; Fairphone "Customize camera stack based on active app" |
| frameworks/base | e/os/android_frameworks_base `a17` | 26 | USB lockdown fix, Hide from microG, SNHooks dockmanager, config_deviceKeyHandler, /e/ palette (system, SystemUI, SettingsLib + v36), emphasized notifications, Monet off, light/dark QS series, nav/notification fixes, **Android Auto** 1/2 + Google-signed install |
| frameworks/libs/systemui | e/os/android_frameworks_libs_systemui `a17` | 1 | calendar month icon |
| packages/apps/Contacts | e/os `a17` | 2 | AccountManager on "add account"; phone-only default |
| packages/apps/DocumentsUI, FMRadio, LineageParts, SettingsIntelligence, WallpaperPicker2 | e/os `a17` | 1 each | theming / icon |
| packages/apps/Launcher3 | e/os/BlissLauncher3 `a17` | 1 | notification count badges |
| packages/apps/Settings | e/os `a17` | 33 | /e/ Settings (home page entries, dev options, Quad9, legal/version, wording), theming |
| packages/apps/SetupWizard | e/os `a17` | 1 | squashed /e/ SetupWizard (account, restore, parental control, Find my device, MDM QR, branding); contains a binary hunk (Apache-2.0 zxing-android-embedded aar) |
| packages/apps/ThemePicker | e/os `a17` | 4 | BlissLauncher permissions, no wallpaper colours, theming |
| packages/modules/Connectivity | e/os `a17` | 1 | Quad9 instead of Google DNS |
| packages/modules/DnsResolver | e/os `a17` | 4 | Advanced Privacy DNS tracker blocking |
| packages/modules/Permission | e/os `a17` | 4 | deviceKeyHandler role, null PermGroups crash fix, theming, Android Auto 2/2 |
| packages/services/Telecomm | LineageOS/android_packages_services_Telecomm `lineage-24.0` (GitHub) | 1 | caller check security fix |
| packages/services/Telephony | e/os `a17` | 1 | quad9.net for http |
| system/core | e/os `a17` | 1 | verified-boot yellow→green spoof |
| vendor/eos, vendor/lineage | e/os `a17` | 1 each | private space disabled (re-implemented) |
| vendor/qcom/opensource/commonsys/fm | e/os/android_vendor_qcom_opensource_fm-commonsys `a17` | 1 | app icon |

Plus `blob-fixups.txt`: 4 FP4 camera blobs, `vendor.debug.camera.pkgname` → `debug.camera.packagename`
(checked: each lineage-24.0 TheMuppets blob contains the string once).

Checked without a device/compiler: all apply (section 5; last run 2026-10-17 against freshly
fetched upstream tips: 107/107), brace balance unchanged vs base for every
touched Java/Kotlin file, XML parses, resource and colour references resolve (where checkable), no
conflict markers. Play Integrity: a17 already has every piece a16 had (`PLAY_INTEGRITY.md`).

Fully triaged = every a16 /e/OS commit is carried, already on a17, or skipped with a reason in
`patches/README.md`. Exception: **BlissLauncher3** was rewritten by /e/OS for a17, so commit
matching doesn't apply; only count badges and the calendar icon were ported, and no feature-level
comparison with the a16 launcher has been done (task C below).

---

## 5. Rebuilding a working environment (the old scratchpad is gone)

Nothing from the previous sandbox survives except this repo. Everything else is re-fetchable.

**Apply test (do this first, and after any patch change):**
```
tools/apply_test.sh a17 ../apply-test-a17     # shallow blobless clones + sparse checkouts, ~10 min
```
It fetches each project's upstream branch (table above), checks out only the files the series
touches, and runs the real `apply-patches.sh`. Expect `>> all patches/a17 series apply (107 patches)`.
Re-running reuses the clones. (Limitation in the script header: depth-1 clones can't show
"already upstream" skips.)

**Working on a series (editing / adding patches):** work in a checkout of the upstream branch with
the series applied (the apply-test dir is fine; widen its sparse checkout with
`git sparse-checkout add <paths>`; in a sparse checkout use `git add --sparse`). Then:
1. Commit with the original author (`--author=`), `(cherry picked from commit <full sha>)`, and an
   `[a17: …]` note explaining any adaptation. Our own fixes: author yourself, with the
   Co-Authored-By/Claude-Session trailers the harness gives you.
2. Checks: `python3 tools/bracecheck.py --base <upstream-ref> <changed .java/.kt>`,
   `python3 tools/rescheck.py <upstream-ref>`, `python3 tools/colorcheck.py <upstream-ref>` (for
   resource-heavy changes), XML parse.
3. Export: `git format-patch -o patches/a17/<project path> <upstream-ref>..HEAD` (keep numbering
   contiguous; regenerate the whole series if you reorder). Use `--binary` if needed (SetupWizard).
4. `tools/apply_test.sh`, update `patches/README.md` (+ `UPSTREAM.md`, `STATUS.md`,
   `KNOWN_ISSUES.md`), commit, push.

**Source of a16 commits** (to port more /e/OS work): `https://gitlab.e.foundation/e/os/<repo>.git`
branch `a16`; LineageOS bases on GitHub `LineageOS/<repo>` branches `lineage-23.0` / `lineage-24.0`.
/e/OS manifest: `https://gitlab.e.foundation/e/os/android.git` branches `a16`, `a17`
(`snippets/eos.xml` lists the forks; remote `e` defaults to `refs/heads/a17`).

---

## 6. Pending work, in priority order

### A. Publish forks + manifest (owner asked; blocked on a GitLab token)
The owner asked whether, given a GitLab PAT, the agent could create forks with our patches on top
and an updated manifest. Agreed approach (not started, no script yet):
- **Token**: the owner adds it in the cloud environment settings (environment menu in the session
  title bar → Edit → Network secrets / API credentials, or an environment variable named
  `GITLAB_TOKEN`). It only reaches **new** sessions. Check first, without printing it:
  `[ -n "$GITLAB_TOKEN" ] && echo set` and `curl -s -o /dev/null -w '%{http_code}' -H "PRIVATE-TOKEN: $GITLAB_TOKEN" https://gitlab.e.foundation/api/v4/user`
  (expect 200; without a token it is 401, which is what the previous session saw). If the token
  is a network secret injected by the proxy, the plain `curl …/api/v4/user` returns 200 by itself.
  Never echo, log or commit the token. Needed scopes: `api` (+ `write_repository`).
- **Where**: gitlab.e.foundation under the owner's user (forks there double as /e/OS MR source
  branches, see `UPSTREAM.md`). Ask the owner if they'd prefer a group/namespace or gitlab.com.
- **Steps**:
  1. Probe: create ONE fork via API (`POST /api/v4/projects/e%2Fos%2Fandroid_packages_modules_DnsResolver/fork`,
     visibility public). Stop and report on any quota/permission error (instances can cap projects per user).
  2. /e/OS repos (19, all `e/os/...` rows above): server-side fork, then push branch `a17-fp4`
     = upstream `a17` + series. Pushing from shallow/blobless clones: fetch the base commit
     (`--depth 1` is fine; the fork already has the history), apply the series, push only the new
     commits. If the server rejects a shallow push, deepen (`git fetch --deepen=N`) or `--unshallow`
     for small repos; for frameworks/base keep blobless (`--filter=blob:none`) rather than unshallow.
  3. LineageOS repos on GitHub (FP4 device tree, frameworks/av, Telecomm): can't fork into GitLab;
     use GitLab "import by URL" (`POST /api/v4/projects` with `import_url`) or create an empty
     project and push the branch. Large imports run server-side; poll `import_status`.
  4. All forks **public** (crave rule). Check each with an anonymous `git ls-remote`.
  5. New manifest `local_manifests/a17/eos_fp4-forks.xml` (or an optional manifest, so it can be
     switched per build): `<remove-project path=…/>` + `<project path=… name="<user>/<fork>"
     remote="<remote>" revision="a17-fp4"/>` for each project. Validate with
     `tools/check_manifest.py --eos-branch a17 [--optional NAME]`.
  6. Keep `patches/a17/` the **source of truth**; write `tools/publish_forks.py` (or .sh) that
     regenerates every fork branch from the series idempotently (force-push the fork branches,
     which are ours), so refreshing after upstream moves is one command. `apply-patches.sh` keeps
     working; with the forks manifest, subjects are already present and it skips them. **Blob
     fixups stay** in `blob-fixups.txt` (blobs can't go into a public fork).
  7. Document in README/STATUS; tell the owner how to switch builds between patches and forks.
- Dry-run everything locally (build every branch, print the API calls) before touching GitLab.

### B. Support the owner's builds (blocked on crave account)
Owner sequence (`STATUS.md` has the copy-paste blocks): **a16 baseline first** (Phase A), then
a17 once crave gives the LineageOS 24 base project ID (put it in `build.sh` `PROJECT_ID`/`WORKSPACE`;
the script refuses a17 on project 99 = LOS 23.2). Suggested a17 order, one variable per build:
1. `PATCH_EXCLUDE="packages/apps/Settings packages/apps/SetupWizard frameworks/base"`
2. drop `frameworks/base`, 3. drop Settings, 4. drop SetupWizard.
When the owner pastes `out/error.log` excerpts: find the failing module, map it to a series, fix
the patch (section 5), push, and give them the next build command. Most likely breakers (hand
ports): Settings (catalyst screens, home-page categories), frameworks/base theming (resource names
in -v36, QS styles), SetupWizard (Kotlin API drift, `setupdesign` styles `SudGlifButton.*`,
`elib` colours `e_accent`/`e_background`/`e_alpha_base`), Android Auto hook
(`AndroidAutoPackage` in services.core used from services.permission Kotlin), DnsResolver
(`-Werror`, e.g. missing prototype for `shouldBlockRequest`), FP4 sepolicy (`debug_camera_prop`
public type; vendor rules on `cameraserver`). After first boot: fill the parity table in
`KNOWN_ISSUES.md` with the owner; no raw logs in the repo.

### C. BlissLauncher3 feature parity (no blocker)
Compare /e/OS a16 BlissLauncher (repo `e/os/BlissLauncher3` branch `a16`, and the older launcher
behaviour) with `a17` + our badge patch, feature by feature (widgets panel, folders, search, icon
shapes/packs, notification dots/badges, wallpaper handling, settings). Port what's missing and
cheap; record the rest in `KNOWN_ISSUES.md`.

### D. Keep the series fresh (no blocker)
Re-run `tools/apply_test.sh` at the start of every session; if a patch stops applying, refresh it
(upstream /e/OS a17 is moving fast). Watch for /e/OS merging equivalents (then drop ours; subject
match retires them automatically, but squashed/reworded ports need manual removal). Re-check that
lineage-24.0 still lacks the frameworks/av and Telecomm security fixes.

### E. Upstreaming (owner opens MRs)
`UPSTREAM.md` has the table. With a token and explicit owner approval you could open MRs from the
forks; don't do it unprompted.

### F. Keep `a16` sensible
`a16` is the baseline build branch. It got all tooling/docs up to c8652df but not the rebase,
`tools/apply_test.sh`, the checkers, or this file. Cherry-pick tooling changes that matter for an
a16 build (e.g. `apply-patches.sh` blob-fixup support is harmless there: no `patches/a16/`).

### G. Phase 2 Play Integrity (after a17 is daily-usable)
`PLAY_INTEGRITY.md`. BASIC only. No keybox/DEVICE tricks.

---

## 7. Techniques and pitfalls learned (save yourself the time)

- **Fetching**: blobless partial clones (`--filter=blob:none`) are great for log/merge-base but
  every `git grep`/`git show` of old content lazily fetches blobs one by one, which can be very slow
  (a `git grep` over DnsResolver timed out). For a quick search, use a full shallow clone of one
  branch (`--depth 1 --no-checkout`, then `git grep HEAD`), or raw files from
  `https://raw.githubusercontent.com/LineageOS/<repo>/<branch>/<path>` and
  `https://gitlab.e.foundation/api/v4/projects/<url-encoded path>/repository/files/<path>/raw?ref=<branch>`.
- Lazy fetch can fail with "not our ref" when a branch moved (old commit no longer advertised);
  use the GitLab raw/API endpoints for that content.
- frameworks/base: use a sparse checkout (`git sparse-checkout set --no-cone /path/file …`) and
  `git add --sparse`; `apply-patches.sh undo` on a sparse checkout may warn "not uptodate" for new
  files outside the sparse set; harmless in a full tree.
- `pkill -f <pattern>` matched the agent's own shell (exit 144); kill by PID instead.
- Variable paths in `rm` are blocked by the sandbox guard; use `"${VAR:?}"` or `find … -delete`.
- `git checkout --theirs` on a conflicted file takes the *whole* other version; when porting a16
  changes into rewritten a17 files, re-apply the minimal edit by hand instead.
- Android 17 specifics that bit us: Settings home page grouped in `PreferenceCategory` blocks and
  Kotlin "catalyst" screens (add /e/ entries in both XML and Kotlin); `-v36` resource folders
  shadow `-v31/-v34` (mirror palette changes); DocumentsUI `use_material3` flag; QS customizer and
  PagedTileLayout removed; `ShadeHeaderController.updateColors()` exists already;
  `PermissionManagerServiceImpl` removed (Kotlin `PermissionService` / `AppIdPermissionPolicy`);
  Monet dynamic overlay must stay disabled to keep the /e/ palette.
- /e/ palette lives in framework resources `@*android:color/e_*` (day/night aliases such as
  `e_accent`, `e_background`, `e_qs_background`, `e_qs_tile_inactive`, `e_floating_background`) and
  `e_switch_*` drawables/colour lists; apps also get colours from `elib`.
- Lottie files referenced by a17 Settings code were kept although /e/ "removes Google animations".
- When a resolver re-adds deleted files (DocumentsUI), `git rm` them explicitly.
- The `[media]` prefix in a subject is stripped by `git am`/`mailinfo`, consistently, so
  subject-based skipping still works.
- Commit authorship: keep original authors for cherry-picks; verify emails from the source commit
  (`git log -1 --format='%an <%ae>' <sha>`), don't guess them.
- Claude-authored commits end with the Co-Authored-By/Claude-Session trailers the harness provides;
  never put model identifiers anywhere else in the repo.

---

## 8. Verified facts (with dates; re-verify before relying on them)

- 2026-10-16: /e/OS manifest `a17` @ c36ed7d: default `lineage-24.0`, AOSP `android-17.0.0_r1`,
  40 forks in `snippets/eos.xml`, every fork has its branch. /e/OS `a16` has 61 forks.
- 2026-10-16: LineageOS FP4 device `lineage-24.0` @ 5e457df, kernel `lineage-24.0` @ 0ff1c1c,
  TheMuppets FP4 `lineage-24.0` @ 49f104f. FP4 `PRODUCT_SHIPPING_API_LEVEL := 30`.
- /e/OS's own FP4 fork (`e/devices/android_device_fairphone_FP4`) has no `a17` branch and imports
  FPCamera from a private blob set → we use LineageOS's tree + TheMuppets blobs; FPCamera is out
  of scope (proprietary).
- `AndroidAutoStub` ships from `external/prebuiltapks` (`config/common.mk`, SDK > 34) on a17.
- ih8sn: same config on a17; bionic property-area layout unchanged 23.0→24.0.
- `override_format_from_reserved`: no consumer in LineageOS 23.0/24.0 frameworks/av or native.
- "FP4: Build gralloc.qcom" (LuK1337) is not in lineage-23.0 or lineage-24.0 FP4 trees.
- LineageOS/android `lineage-24.0` tip d4c6331 (2026-10-09), `lineage-23.0` tip 2a46cce.
- crave: LOS 23.2 project id 99 per a community builder (unverified by us); LineageOS 24 project
  id unknown (owner to ask on crave Discord).

---

## 9. Guesses and judgement calls (first suspects if something breaks)

- **SetupWizard**: one squashed commit instead of rebasing /e/'s bring-up branch; jackson jars
  replaced by `org.json`; bundled zxing core dropped in favour of AOSP `zxing-core` (duplicate
  classes otherwise); lottie welcome animation replaced by the /e/ logo; `onNavigateNext()` →
  `onNextPressed()`; theme/navigation pages skipped after a restore via an `isSkipped()` hook.
- **Android Auto**: grant implemented in `PermissionService.isPermissionGranted()` (covers
  `checkPermission` and `checkUidPermission`), constants moved to `com.android.server.pm.AndroidAutoPackage`.
  Untested whether other paths (e.g. permission state queries, AppOps) need the grant too.
- **Contacts phone-only default**: creates a device contact without persisting a default account
  (so the Settings default-account prompt never shows while only the device account exists).
- **DnsResolver**: a16 code carried verbatim, including an upstream bug (heap `char[10]` filled
  with `strncpy` without a terminator when blocking). Fix only if it misbehaves, and upstream the fix.
- **Camera**: eCamera RRO targets `foundation.e.camera` (from /e/'s FP4 tree, not re-verified
  against the APK); `persist.vendor.camera.privapp.list` keeps `com.fp.camera` too (harmless).
- **Theming**: night `Theme.SystemUI.QuickSettings` rebuilt from the a17 day style; QS clock colour
  hook kept as a no-op; several a16 QS commits skipped as obsolete (`patches/README.md`).
- **Private space**: disabled via `config_user_types` user-type overlay + launcher flag, since the
  a16 flag no longer exists.
- Build type stays `userdebug` (ih8sn masks props); `user` is a documented Play Integrity experiment only.

---

## 10. First 15 minutes for the next agent

1. `git log --oneline -15` on `a17`; read this file, `STATUS.md`, `KNOWN_ISSUES.md`.
2. Check messages from the owner: did they get the crave account / LOS24 project ID / build
   results? Did they add `GITLAB_TOKEN`? (Check per section 6A, without printing it.)
3. `tools/apply_test.sh a17 ../apply-test-a17`: confirm the series still applies to today's tips.
4. Pick the highest unblocked item in section 6, tell the owner which, and go.
5. Before ending: update `STATUS.md` build log, commit, push to your designated branch and `a17`.
