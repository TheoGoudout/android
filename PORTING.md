# Porting /e/OS for FP4 to a newer LineageOS: research and plan

Researched 2026-10-16. Re-check the dated facts before acting on them.

## 1. Where things stand

| | Base | Android | State for FP4 |
|---|---|---|---|
| /e/OS `a16` (v4.3 / 4.4) | LineageOS 23.0 | 16 | What FP4 runs today (official, A14 → A16 upgrade done in v4.3, v4.3.1 FP4 audio fix) |
| /e/OS `a16.2` | LineageOS 23.2 | 16 QPR2 | Branch exists but is mostly un-ported: 40 forks vs 61 on a16, and e.g. `vendor/lineage` there is plain LineageOS 23.2 (version 23.2, no `vendor/eos` inherit) |
| /e/OS `a17` | LineageOS 24.0 | 17 | Work in progress by the /e/OS team: `vendor/lineage` already says /e/OS 4.4 / a17 and inherits `vendor/eos` |
| LineageOS 23.0 | | 16 | Dead upstream: FP4 tree last touched Jan 2026, FP4 blobs Sept 2025 (FP4.QREL.15.14.3) |
| LineageOS 23.2 | | 16 QPR2 | Superseded |
| LineageOS 24.0 | | 17 | Released ~Oct 2026; **FP4 official builds are on lineage-24.0** (hudson build targets); FP4 tree has Aug 2026 stock blobs (FP4.QREL.15.20.0) |

/e/OS staff (week 41 update, Oct 2026): "We use LOS 23.0 as our base" and "do not have any plans
to move to LOS 23.2". Their next step is visibly a17/LOS 24.0.

**Conclusion: don't port to 23.2.** It is already superseded upstream, /e/OS will never ship it,
and you'd carry the whole port alone. The useful target is **LineageOS 24.0 (a17)**, where the
/e/OS team is already doing most of the work.

## 2. What "porting" actually involves (it is not just the manifest)

/e/OS = LineageOS + forks of ~40-60 repos + extra repos:

- **Forks with real feature patches** (must be rebased): frameworks/base (microG signature
  spoofing, privacy features), Settings, SetupWizard, Launcher3 → BlissLauncher3,
  frameworks/libs/systemui, ThemePicker, WallpaperPicker2, Contacts, Dialer, DocumentsUI,
  LatinIME, Updater, Telephony, modules (Connectivity, DnsResolver, Permission), system/core,
  vendor/lineage, lineage-sdk, bootable/recovery, build/soong…
- **Forks that only exist on a16 (~21)**: AOSP projects such as external/libpng, sqlite, dng_sdk,
  frameworks/av, frameworks/native, Bluetooth, MediaProvider, system/apex. LineageOS 23.0 stopped
  getting security merges, so these are most likely /e/OS carrying monthly security fixes itself
  (inference). On 23.2/24.0 LineageOS already ships those, so most of them can be dropped.
- **/e/OS-only repos** (no rebase, just build-test): vendor/eos, elib, prebuiltapks (microG,
  App Lounge, Advanced Privacy… as prebuilt APKs), ih8sn, picotts, vendor/apn.

Expected pain points going 23.0 → 23.2/24.0: the Material 3 Expressive redesign of QPR1/QPR2 hits
exactly the UI repos /e/OS customises most (SystemUI/frameworks/base, Settings, Launcher3,
ThemePicker, WallpaperPicker2), and prebuilt APKs may need targetSdk/permission updates.

## 3. Measure it before committing: `port-audit/port_audit.py`

For each /e/OS fork it lists /e/OS's own commits, drops those already upstream, and replays the
rest onto the target branch with `git merge-tree` (no checkout, no build). Tested on synthetic
repos and on real LineageOS frameworks/base (≈3 min, 1.2 GB). Run it on your laptop:

```
cd port-audit
./port_audit.py --eos-branch a16 --old lineage-23.0 --new lineage-24.0   # recommended target
./port_audit.py --eos-branch a16 --old lineage-23.0 --new lineage-23.2   # your original plan
```

Read the report as: *already upstream* = free, *clean* = mechanical, *conflicts* = manual work.
"Clean" means it applies textually, not that it compiles or works.

## 4. Recommended plan

1. **Baseline**: build real /e/OS `a16` for FP4 (`EOS_BRANCH=a16`) on crave, flash, confirm it boots.
2. **Audit**: run port_audit for a16 → lineage-24.0, and compare with what /e/OS already has on a17.
3. **Build `a17`** (`EOS_BRANCH=a17`, FP4 trees on lineage-24.0). Needs a LineageOS 24 base project
   on crave (ask on their discord; their rules require same-Android-version bases).
4. **Fix what breaks for FP4** and send the fixes upstream to /e/OS (gitlab.e.foundation MRs) so
   you don't maintain a fork forever.
5. Only if /e/OS's a17 stalls: finish the missing rebases yourself from the audit's conflict list.

## 5. Phase 2: the Play Integrity "hack"

What /e/OS ships today:
- **ih8sn** (vendor/eos): at boot it rewrites build props. The default /e/OS config only sets
  `DEBUGGABLE=0`, `BUILD_TAGS=release-keys`, `BUILD_TYPE=user` (hides userdebug/test-keys), and it is
  only included on community/official builds. This build script turns it on (`INCLUDE_IH8SN=true`).
- **microG device attestation (DroidGuard)**: Basic integrity can pass once a Google account is
  added to microG; users report it regressing on and off through 2026 with no confirmed root cause.

Hard limits since May 2025 (Google, Android 13+ devices): verdicts come from hardware-backed key
attestation.
- MEETS_BASIC: key attestation present; unlocked bootloader allowed → **reachable**.
- MEETS_DEVICE: locked bootloader + certified manufacturer image + verified boot → **not reachable**
  with any custom build (relocking FP4 with your own key gives a "yellow" boot state, not certified).
- MEETS_STRONG: DEVICE + patches within a year → not reachable.

No prop spoofing can change hardware-attested facts. What passes DEVICE on custom ROMs today relies
on someone else's leaked attestation keys: it gets revoked by Google and isn't something to build
into an OS; out of scope here.

Realistic phase-2 work: keep BASIC reliable on your build — check key attestation works on the
new base (KeyMint/TEE from the FP4 vendor blobs), keep microG's attestation settings correct, have
ih8sn hide debug/test-key markers, and accept that apps demanding DEVICE won't run.

## Sources
- /e/OS weekly update, week 41 (2026): community.e.foundation/t/week-41-development-and-testing-updates/85220
- /e/OS manifests: gitlab.e.foundation/e/os/android (branches a16, a16.2, a17; snippets/eos.xml)
- /e/OS build docs: doc.e.foundation/os/advanced/build/
- LineageOS FP4 trees and hudson build targets (github.com/LineageOS)
- LineageOS 24.0 release: linuxiac.com (2026-10-11)
- Play Integrity, Android 13+ verdicts: developer.android.com/google/play/integrity/improvements
- microG on /e/OS: doc.e.foundation/os/apps/microg/
