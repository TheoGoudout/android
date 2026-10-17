# STATUS

Target: a17 (LineageOS 24.0, Android 17), device FP4
Last verified base facts: 2026-10-16 (patch series re-checked 2026-10-17) (from the agent sandbox: `git ls-remote`, manifest clones, hudson)
Baseline a16 boots: **not yet built**. Waiting on the owner (Phase A)
crave LOS24 project ID: pending from owner (ask on crave Discord)
Project repo: `github.com/TheoGoudout/android`, branches `a16` (baseline) and `a17` (main work, this file's home)
crave account: requested by owner 2026-10-16, awaiting approval

Start every session by reading this file and `KNOWN_ISSUES.md`. Agent brief: `AGENT_PLAN.md`.

## Verified facts (2026-10-16)

- FP4 repos have both `lineage-23.0` and `lineage-24.0` heads:
  `LineageOS/android_device_fairphone_FP4` (24.0 @ 5e457df), `LineageOS/android_kernel_fairphone_sm7225`
  (24.0 @ 0ff1c1c, same commit as 23.2), `TheMuppets/proprietary_vendor_fairphone_FP4` (24.0 @ 49f104f).
  The `local_manifests/a16|a17/eos_fp4.xml` pin exactly these three repos at those branches. Both XMLs parse.
- FP4 `lineage.dependencies` (23.0 and 24.0) lists only the kernel, already in the local manifest,
  so `breakfast` needs no roomservice additions. Neither /e/OS manifest declares any FP4 path (no duplicates).
- hudson `lineage-build-targets`: `FP4 userdebug lineage-24.0 W`.
- /e/OS manifest `a17` @ c36ed7d (2026-10-14): default `lineage-24.0`, AOSP `android-17.0.0_r1`,
  40 forks in `snippets/eos.xml`. **Every a17 fork has its branch** (`a17`, or `main`/`master`/`develop`
  where pinned), so an a17 `repo sync` should not fail on a missing ref.
- /e/OS `a16` has 61 forks. The 21 that are not on `a17` are listed under Port status below.
- **/e/OS ships FP4 from its own device/kernel forks** (`e/devices/android_device_fairphone_FP4`,
  `e/devices/android_kernel_fairphone_sm7225`, branch `a16`; **no `a17` branch**). The device fork
  imports Fairphone's proprietary camera (FPCamera) from a blob set that isn't public, so we
  build on LineageOS's tree + TheMuppets blobs (like /e/OS's community builder) and carry the
  open-source /e/OS FP4 commits as patches (`patches/README.md`). The only lineage-23.0 FP4 commit
  missing from lineage-24.0 is a blob bump that 24.0 supersedes.
- `tools/check_manifest.py` resolves /e/OS manifest + our local manifest offline: a16 and a17 both
  clean (no duplicate paths, every path the FP4 tree references is provided).
- Not verifiable from here: crave project IDs/names (`PROJECT_ID=99`, `crave.yaml` key `LOS 23.2`),
  whether this repo is public **from crave's side** (anonymous `git ls-remote` works from the sandbox).

## Build log (newest first)

- 2026-10-17: rest of the a17 port (owner: "implement everything"). 99 patches over 23 projects,
  all apply to fresh checkouts (`apply-patches.sh` on /e/OS a17 + lineage-24.0 FP4). Not compiled.
- 2026-10-16: a17 prep without a build (owner request). Added the patch mechanism
  (`apply-patches.sh`, called by `remote-build.sh`) and the first a17 series: 10 FP4 device
  patches + 9 patches on /e/OS forks whose a17 branch is still empty. All apply to fresh
  checkouts. Not compiled.
- 2026-10-16: branches `a16`/`a17` created (owner request). Deleting `claude/ci-android-xml-build-bWyCA` is refused from the agent sandbox: owner to delete it on GitHub.
- 2026-10-16: no builds yet. Repo prepared; Phase A handed to owner (block below).

## Phase A: owner action needed (a16 baseline)

On your machine, with `crave.conf` in place (never commit it):

```
git clone -b a16 https://github.com/TheoGoudout/android eos-fp4 && cd eos-fp4
crave clone list          # confirm project 99 is the LineageOS 23.2 (Android 16) base and its exact name;
                          # if the name is not "LOS 23.2", fix the top-level key in crave.yaml
crave devspace            # then, inside the devspace, from this checkout:
./build.sh setup          # once: creates /crave-devspaces/Lineage23
./build.sh build          # EOS_BRANCH=a16 is the default in build.sh
./build.sh pull           # on success: eos-latest-ota.zip, eos-latest-img.zip, SHA256SUMS
./build.sh log            # on failure: paste the relevant part of out/error.log back
```

Flash with the bootloader **unlocked** (test-key build; do not relock). Report back:
1. boots? (yes/no) and `adb shell getprop ro.build.fingerprint`
2. App Lounge, microG self-check, Advanced Privacy, BlissLauncher open and work?
3. any failure: the build-log excerpt (no raw device logs in this repo)

Do not start a17 (Phase C) until a16 boots.

## Port status (port_audit 2026-10-16)

Full reports: `port-audit/reports/`. a16 → lineage-24.0: 1142 /e/OS commits; 273 already upstream,
317 apply cleanly, 552 conflict (BlissLauncher3 alone: 285). What /e/OS already carries on a17 vs
what a16 had (subject match, so reworded/squashed ports count as missing):
`port-audit/reports/a16-vs-a17-gap.md`.

| repo | already on a17 | audit verdict (a16→24.0: clean / conflict) | a16 patches missing on a17 | who |
|---|---|---|---|---|
| packages/apps/Launcher3 (BlissLauncher3) | partial (44 commits) | 42 / 285 | 316* | /e/OS |
| frameworks/base | partial (36: sig spoofing, fake location, parental ctl, e colors…) | 46 / 47 | 57 | /e/OS (watch) |
| packages/apps/Settings | branch only (CI commit) | 13 / 30 | 42 | /e/OS |
| packages/apps/SetupWizard | branch only | 2 / 32 | 33 | /e/OS |
| vendor/lineage | partial (36) | 32 / 38 | 33 | /e/OS |
| frameworks/libs/systemui | branch only | 3 / 23 | 25 | /e/OS |
| packages/modules/Permission | branch only | 5 / 9 | 13 | /e/OS |
| packages/apps/ThemePicker, WallpaperPicker2 | branch only | 4/2, 3/1 | 5, 3 | /e/OS |
| packages/modules/DnsResolver, Connectivity | branch only | 6/0, 5/0 | 5, 4 | /e/OS (clean: easy MR candidates) |
| packages/apps/LineageParts | mostly (12) | 8 / 8 | 4 | /e/OS |
| overlays/Lineage, FMRadio, SettingsIntelligence, Telephony, fm-commonsys, system/core | branch only | clean except overlays and SettingsIntelligence (1 conflict each) | 1–3 each | /e/OS (clean: MR candidates) |
| Contacts, Dialer, DocumentsUI | mostly | 7/6, 4/1, 3/1 | 2, 1, 1 | /e/OS |
| Updater, LatinIME, apn, Backgrounds, Gallery2, recovery, soong, sepolicy, lineage-sdk, vcard, EmergencyInfo, ImsServiceEntitlement, deprecated-ota | yes (all subjects present) | n/a | 0 | done |
| vendor/eos, elib, prebuiltapks, ih8sn, svox | /e/OS-only | build-test only | n/a | build-test |
| FP4 device / kernel / blobs | LineageOS lineage-24.0 | n/a | n/a | us (local manifest) |

\* BlissLauncher3 on a17 was likely re-based rather than replayed; subject matching overstates the gap.

**a16-only forks (not on a17), checked commit by commit:** dng_sdk, libpng, thermal, st/nfc, CertInstaller,
KeyChain, ContactsProvider, TelephonyProvider, system/apex, Profiling, Virtualization: only CI/licence
commits left after dropping what lineage-24.0 has → **drop**. sqlite, build/release, libopenapv: /e/OS
version bumps for 23.0 → **drop** (24.0 ships its own). Security self-carries whose subject does not
appear in lineage-24.0 (frameworks/av ×2, Bluetooth ×3, Nfc ×2, adb ×2, MediaProvider ×1, Telecomm ×1):
probably covered by the android-17.0.0_r1 / LOS 24.0 security level, **to verify** against the ASB
bulletins before relying on it. frameworks/native: only MediaTek-specific (irrelevant to FP4, Qualcomm).
frameworks/av `libcameraservice: Customize camera stack based on active app` (2021): **check** whether
LineageOS 24.0 dropped it on purpose. It may matter for FP4 camera apps.

**Reading (updated 2026-10-17):** plain /e/OS a17 = LineageOS 24.0 + /e/OS branding, prebuilt
apps, microG signature spoofing, fake location, parental-control hooks, BlissLauncher3, but stock
LineageOS Settings/SetupWizard and no /e/ theming. With `patches/a17/` (99 patches, 23 projects)
the build also gets:
- /e/ Settings (Advanced Privacy, Parental control, Find my device, Updater/Accounts on top, /e/
  legal + version, /e/ dev options, Quad9)
- /e/ SetupWizard (/e/ account, restore, parental control, Find my device, MDM QR)
- /e/ palette across the system (Settings, SystemUI incl. light/dark QS, SettingsLib, framework, 6
  apps; Monet disabled)
- Advanced Privacy DNS tracker blocking, Android Auto as a user app, launcher count badges,
  calendar month icon, Hide-from-microG
- Quad9 DNS defaults, private space disabled, Contacts phone-only default
- FP4 audio/VoIP/CarrierConfig fixes, 3 security fixes 24.0 lacks

The a16 → a17 gap list (`port-audit/reports/a16-vs-a17-gap.md`) is now fully triaged: everything is
carried, already on a17, or skipped with a reason in `patches/README.md`. None of it has been
compiled yet. Expect build errors in the hand-ported parts first (Settings, SystemUI theming,
SetupWizard, the Android Auto permission hook).

## a17 work items (no build needed)

- [x] FP4 device: carry /e/OS FP4 audio/VoIP/CarrierConfig/bootanimation changes (`patches/a17/device/fairphone/FP4`)
- [x] Small /e/OS forks: system/core, Connectivity, Telephony, Permission (part), ThemePicker, Contacts, FM
- [x] Big forks, first pass (2026-10-16). Mechanical replay barely works (Settings 9/62, SetupWizard
      1/34, vendor/lineage 1/71, frameworks/base 11/191), but /e/OS has active a17 work:
      - BlissLauncher3 `a17` is a fresh AOSP-17 rewrite (commits today), so the "316 missing" figure is an
        artefact. Nothing for us to do.
      - SetupWizard: /e/OS's `epic265-a17-bringup` has all /e/ pages, but on a pre-rewrite SUW base
        (LineageOS rewrote SUW at the end of September). Now squashed onto current a17 as
        `patches/a17/packages/apps/SetupWizard` (the optional manifest is superseded).
      - Settings, frameworks/base, frameworks/libs/systemui: bring-up branch = a17 (no hidden work).
- [x] Settings: 42 a16 commits walked on a17 → 32 patches (13 hand-resolved), 3 already in
      a17, 7 skipped with reason (`patches/README.md`). Static checks clean; not compiled.
- [x] frameworks/base: 57 missing a16 commits triaged. Carried Hide-from-microG + USB lockdown
      security fix + SNHooks; 4 security fixes already in a17; Android Auto needs re-implementation
      (KNOWN_ISSUES #1); SystemUI theming left to /e/OS.
- [x] vendor/lineage: 33 missing a16 commits triaged; only "Disable private space" still matters,
      re-implemented for Android 17 (vendor/eos overlay + vendor/lineage cp2a launcher flag).
- [x] 2026-10-17, "implement everything" (owner request): /e/ theming everywhere, SetupWizard pages,
      Android Auto (Kotlin permission service), DeviceKeyHandler role, launcher count badges,
      DnsResolver tracker blocking, Contacts phone-only default, calendar month icon.
- [x] frameworks/libs/systemui (25 a16 commits): notification-badge/DotRenderer work for the old
      BlissLauncher. Not carried: /e/OS's new launcher implements count badges inside the launcher
      (`CountBadge`, on BlissLauncher3 `epic265-a17-bringup` only, not yet on `a17`), without these
      libs/systemui changes. Ported onto BlissLauncher3 `a17` (`patches/a17/packages/apps/Launcher3`).
- [x] Remaining forks (DocumentsUI, SettingsIntelligence, WallpaperPicker2, LineageParts,
      Permission, SystemUI/SettingsLib palette): theming, now carried.
- [x] Permission "deviceKeyHandler" role + frameworks/base `config_deviceKeyHandler` resource
- [x] Verify the 11 a16 security self-carries: 8 present in lineage-24.0, 1 likely (rewritten), 2 still
      vulnerable (Matroska heap write, Telecomm caller check), now carried in `patches/a17/`.
      Worth reporting to LineageOS too.
- [ ] Prepare /e/OS MRs (a17 branches) for the clean patches, so the series can shrink
- [ ] Phase C build once crave LOS24 project ID is known (a16 baseline first if possible).
      Suggested a17 order, one variable per build: (1) a17 + FP4 + patches/a17 with
      `PATCH_EXCLUDE="packages/apps/Settings packages/apps/SetupWizard frameworks/base"`;
      (2) drop frameworks/base from the exclude; (3) drop Settings; (4) drop SetupWizard.

## Open questions for the owner

- Confirm crave project 99 = LineageOS 23.2 and its exact name in `crave clone list` (for `crave.yaml`).
- Ask crave (Discord) for the LineageOS 24 base project ID and workspace path; give them to me for `build.sh`.
- Phase 2 note: a17 `frameworks/base` carries `keystore: Block key attestation for SafetyNet`. Its
  interaction with BASIC on Android 17 needs testing once we get there.
