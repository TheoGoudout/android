# Agent brief: /e/OS for Fairphone 4 on LineageOS 24.0 (Android 17)

You are an agent working on a custom /e/OS build for a Fairphone 4 (codename `FP4`). You have
push access to one GitHub repository (the **project repo**) and nothing else on GitHub. You
cannot build Android yourself (a build needs ~400 GB disk and 16–64 GB RAM) and you cannot touch
the phone. Builds run on **crave.io** (a free build cluster for open-source Android ROMs); the
phone is flashed and tested by the **owner**. Your job: prepare manifests, patches, tooling and
analysis; drive the build/test loop; keep a written trail so the work survives between sessions.

Read this whole file, then `PORTING.md` and `README.md` in the project repo, before acting.

---

## 0. Ground truth (researched 2026-10-16 — re-verify anything you depend on)

- /e/OS for FP4 today = branch **`a16`** on **LineageOS 23.0** (Android 16). LineageOS 23.0 is
  effectively frozen upstream (FP4 device tree last touched Jan 2026, blobs Sept 2025).
- /e/OS branch **`a16.2`** (LineageOS 23.2) exists but is mostly un-ported (40 forks vs 61 on a16;
  its `vendor/lineage` is plain LineageOS 23.2 without the `vendor/eos` inherit). **Do not target it.**
- /e/OS branch **`a17`** = /e/OS on **LineageOS 24.0** (Android 17), in progress by the /e/OS team:
  `vendor/lineage` already reads /e/OS 4.4 / a17 and inherits `vendor/eos`; manifest default
  revision `lineage-24.0`, AOSP tag `android-17.0.0_r1`; `snippets/eos.xml` lists ~40 forks.
- LineageOS 24.0 released ~2026-10-11. FP4 official LineageOS is on `lineage-24.0`
  (hudson `lineage-build-targets`: `FP4 userdebug lineage-24.0 W`). FP4 repos with a `lineage-24.0`
  branch: `LineageOS/android_device_fairphone_FP4`, `LineageOS/android_kernel_fairphone_sm7225`,
  `TheMuppets/proprietary_vendor_fairphone_FP4` (blobs from stock FP4.QREL.15.20.0, Aug 2026).
- /e/OS staff (Oct 2026): "We use LOS 23.0 as our base", no plans to move to 23.2.
- /e/OS manifest: `https://gitlab.e.foundation/e/os/android.git` (forks in `snippets/eos.xml`,
  remote `e`). Reference builder: `.../e/os/docker-lineage-cicd/-/raw/master/build-community.sh`
  (for a17 it uses TheMuppets `lineage-24.0`, builds `target-files-package otatools`, signs, then
  emits OTA + IMG zips).

**Goal:** a booting, daily-usable /e/OS `a17` build for FP4, with every /e/OS feature that exists
in `a16` either working in `a17` or recorded as a known gap. Upstream fixes to /e/OS so the owner
does not maintain a private fork forever.

**Out of scope:** targeting LineageOS 23.2; bundling proprietary Fairphone apps (e.g. the stock
camera) in the public repo; Play Integrity DEVICE/STRONG, which a custom build cannot obtain
(see §8).

---

## 1. Hard rules

1. The project repo is **public**. Never commit secrets or proprietary content: `crave.conf`,
   API tokens, signing keys, proprietary APKs or vendor blobs, or raw device logs. Keep a
   `.gitignore` that blocks `*.conf`, `*.keystore`, `*.jks`, `keys/`, `*.apk`, `*.img`, `*.zip`.
2. **crave rules** (a ban ends the whole effort): one queued build at a time; one device per
   build; never `repo sync` or compile inside `crave devspace` / `crave ssh` (use `crave run`);
   never `make clean` / `rm -rf out` / casual `--clean` — it destroys the shared incremental cache;
   no private repos.
3. You do not have crave credentials and must not ask for them in chat. You produce the files and
   commands; the **owner** runs anything that needs `crave.conf` or the phone. Where a step is the
   owner's, write it out as a copy-pasteable block and stop for their result.
4. Builds are signed with **test keys**: the phone keeps its bootloader **unlocked**. Never advise
   relocking on a test-key build.
5. Do not invent facts about repos, branches or build output. If you can't verify something
   (e.g. GitLab is unreachable from your sandbox), say so and have the owner check.
6. Commit small and often with clear messages. Keep `STATUS.md` (see §7) current so a fresh
   session can resume.

---

## 2. What the project repo holds (you own this)

```
local_manifests/
  a16/eos_fp4.xml         # FP4 device+kernel+blobs on lineage-23.0  (baseline target)
  a17/eos_fp4.xml         # FP4 device+kernel+blobs on lineage-24.0  (main target)
build.sh  remote-build.sh  crave.yaml   # crave build wrappers (owner runs build.sh)
port-audit/port_audit.py                 # patch-portability analyser
PORTING.md  README.md  STATUS.md  AGENT_PLAN.md
```

The single file crave consumes is the per-target local manifest (what the owner called
"android.xml"). It pins the FP4 device tree, kernel and proprietary blobs, and is where you add
device-specific forks and `<remove-project>` overrides. The owner points crave at a branch of this
repo; `remote-build.sh` copies `local_manifests/<branch>/*.xml` into `.repo/local_manifests/`.

Branch convention: keep a repo branch per target (`a16`, `a17`) matching the `/e/OS` branch name.

---

## 3. Phase A — reproduce the current build (`a16`) as a baseline

Prove the toolchain end to end before changing versions.

1. Confirm the three FP4 repos have a `lineage-23.0` branch (device, kernel, TheMuppets blobs)
   with `git ls-remote --heads`. Confirm `local_manifests/a16/eos_fp4.xml` references them.
2. Hand the owner the `a16` build block (from `README.md`): request crave access if needed, set
   `EOS_BRANCH=a16`, run `./build.sh setup`, `./build.sh build`, `./build.sh pull`.
3. Owner flashes and confirms it boots and that core /e/OS apps work. Record the result and the
   build fingerprint in `STATUS.md`. **Do not proceed until `a16` boots.**

If `a16` fails, fix that first — it isolates toolchain problems from porting problems.

---

## 4. Phase B — measure the port (`a16` → `lineage-24.0`)

Use `port-audit/port_audit.py` (no build, no checkout; `git merge-tree` replay). Run it where it
has network to gitlab.e.foundation and github.com — if your sandbox is blocked, write the exact
commands into `STATUS.md` for the owner and ask them to paste back the two report files.

```
cd port-audit
./port_audit.py --eos-branch a16 --old lineage-23.0 --new lineage-24.0
```

Read `report-a16-to-lineage-24.0.md`:
- **already upstream** → free (LineageOS 24.0 already carries it; typically the security backports
  /e/OS had to self-carry on dead 23.0).
- **clean** → applies textually; still must compile.
- **conflicts** → manual porting, listed per repo with the touched files.

Also diff /e/OS's own `a16` vs `a17` `snippets/eos.xml` (they are in the manifest repo): the repos
/e/OS has **already** moved to `a17` are done for you — you only owe FP4-specific work plus
whatever /e/OS hasn't finished. Write a short table in `STATUS.md`:
`repo | already on a17? | audit verdict | who does it`.

Expected hotspots (Material 3 Expressive redesign from Android 16 QPR1/QPR2 lands on exactly the
repos /e/OS customises): `frameworks/base` (incl. SystemUI + microG signature-spoofing patch),
`packages/apps/Settings`, `Launcher3`→BlissLauncher3, `ThemePicker`, `WallpaperPicker2`,
`SetupWizard`, `frameworks/libs/systemui`. The ~21 AOSP-only forks that exist only on `a16`
(libpng, sqlite, dng_sdk, Bluetooth, MediaProvider, system/apex, …) are most likely 23.0 security
self-carries and can usually be dropped on 24.0 — confirm each against the `a17` manifest.

---

## 5. Phase C — first `a17` build

1. Verify `local_manifests/a17/eos_fp4.xml` pins FP4 device + kernel + TheMuppets blobs at
   `lineage-24.0`. Validate the XML (`xmllint --noout` or Python `xml.etree`).
2. crave base project: `a17` needs a **LineageOS 24** base project, and crave rules require the
   base project to match the ROM's Android version. The owner must ask crave (Discord) for the
   LineageOS 24 project ID and set `PROJECT_ID` / `WORKSPACE` in `build.sh`. Until then, do not
   build a17 on the Android-16 base project.
3. Owner runs the `a17` build (`EOS_BRANCH=a17`). Capture `out/error.log` via `./build.sh log`.
4. Triage failures from the log, lowest layer first (sync/manifest → device/kernel → vendor/eos
   prebuilts → frameworks). For each fix: change the manifest or add a fork reference, commit,
   push, ask for a rebuild. One variable per iteration. Record each attempt in `STATUS.md`.

A sync that leaves conflicts usually means a `<remove-project>` is missing or a path moved between
23.0 and 24.0 — fix in the local manifest, never by deleting the source tree on the build node.

---

## 6. Phase D — bring up and parity

Once it builds and the owner confirms it boots:
1. Walk the /e/OS feature set present in `a16` and check each in `a17`: App Lounge / microG,
   Advanced Privacy, BlissLauncher, Parental Control, the /e/ account, OTA updater, default apps.
2. For each regression, find the owning /e/OS repo, port the missing patch (use the audit's
   conflict detail), and rebuild. FP4-specific breakage (camera lenses, fingerprint, VoLTE, audio
   routing — the v4.3 FP4 audio-distortion fix is a known recent example) goes against the FP4
   device tree / blobs.
3. Keep a living `KNOWN_ISSUES.md`: symptom, suspected repo, status.
4. **Upstream**: open merge requests against the matching `e/os/...` repo on gitlab.e.foundation
   for each fix (the owner has/creates the account; you prepare the branch, patch and MR text).
   This is how the work stops being a private fork.

---

## 7. STATUS.md (keep current every session)

```
# STATUS
Target: a17 (LineageOS 24.0, Android 17), device FP4
Last verified base facts: <date>
Baseline a16 boots: yes/no (<fingerprint>, <date>)
crave LOS24 project ID: <id or "pending from owner">

## Build log (newest first)
- <date> a17 attempt N: <result>, error at <stage>, next: <action>

## Port status (from port_audit + a17 manifest diff)
repo | already on a17 | audit verdict | owner

## Open questions for the owner
- ...
```

Start every session by reading `STATUS.md` and `KNOWN_ISSUES.md`.

---

## 8. Phase 2 — Play Integrity (only after a17 is daily-usable)

Understand the ceiling before touching it. Since May 2025, on Android 13+ devices Google derives
Play Integrity verdicts from **hardware-backed key attestation**:
- **BASIC** — reachable on a custom ROM with an unlocked bootloader (needs working key attestation
  + microG's device-attestation path). **This is the only realistic target.**
- **DEVICE / STRONG** — require a locked bootloader with a manufacturer-certified image; a custom
  build cannot obtain them, and relocking the FP4 with your own key yields an uncertified
  ("yellow") boot state, not a passing one. Out of scope.

What /e/OS already includes and what to keep healthy on the new base:
- **microG** (prebuilt, from `vendor/eos` / prebuiltapks): BASIC passes once a Google account is
  tethered to microG's device attestation. Owners have reported it regressing intermittently
  through 2026 with no confirmed root cause — treat "BASIC works" as something to re-test per build.
- **ih8sn** (`external/ih8sn`, pulled by `vendor/eos`): a boot-time service that normalises a few
  build properties. /e/OS's default config only sets `DEBUGGABLE=0`, `BUILD_TAGS=release-keys`,
  `BUILD_TYPE=user`, and it is auto-included only on community/official builds — so for this
  UNOFFICIAL build pass `INCLUDE_IH8SN=true` (the build script already does). Confirm the config
  copies to `/system/etc/ih8sn.conf` on a17 and that the service starts.

Phase-2 work items: (a) confirm hardware key attestation functions on a17 (KeyMint/TEE via FP4
blobs); (b) confirm microG self-check passes (Settings → System → App compatibility); (c) confirm
BASIC with the Play Integrity API Checker; (d) if BASIC regressed vs a16, bisect microG version and
the frameworks/base signature-spoofing patch. Do not pursue leaked-keybox approaches to fake
DEVICE — they get revoked and don't belong in an OS. Record outcomes; don't promise DEVICE/STRONG.

---

## 9. Definition of done
- `a17` FP4 build boots and is daily-usable (owner-confirmed).
- /e/OS feature parity with `a16` documented: each feature working or in `KNOWN_ISSUES.md`.
- Fixes submitted upstream as /e/OS merge requests where applicable.
- Play Integrity BASIC status documented (passing, or the precise blocker).
- Repo reproducible from scratch: manifests + `STATUS.md` let a fresh agent rebuild without you.
