# Play Integrity (Phase 2)

Target: **BASIC** only. DEVICE/STRONG need a locked bootloader with a manufacturer-certified
image, so a test-key build with an unlocked bootloader can't get them. No keybox tricks (AGENT_PLAN §8).

## What the a17 build carries (checked from source on 2026-10-17)

| piece | where | a16 | a17 |
|---|---|---|---|
| Spoof `Build.MODEL/DEVICE/PRODUCT/FINGERPRINT` (Pixel 2, walleye 8.1) for `com.google.android.gms` | frameworks/base `SafetyNetHooks` + `Instrumentation` | yes | yes, identical (/e/OS a17) |
| Block key attestation when DroidGuard asks (`AndroidKeyStoreSpi.engineGetCertificateChain`) | frameworks/base | yes | yes, identical (/e/OS a17) |
| Signature spoofing for microG (incl. system apps) | frameworks/base | yes | yes (/e/OS a17) |
| microG (GmsCore, GsfProxy, FakeStore) | `external/prebuiltapks` (`main`, shared by a16/a17) | yes | same prebuilts |
| ih8sn (masks `ro.debuggable`, build tags/type at boot) | `external/ih8sn` (`master`) + `vendor/eos/config/common.mk` | yes | same; forced on by `remote-build.sh` (`INCLUDE_IH8SN=true`) |
| ih8sn config | `vendor/eos/config/ih8sn/ih8sn_default.conf` (no FP4-specific file) | same | same: `DEBUGGABLE=0`, `BUILD_TAGS=release-keys`, `BUILD_TYPE=user` |
| Spoof yellow verified-boot state to green | system/core (`patches/a17/system/core`) | yes | carried. Only matters on a relocked custom-key device; ours stays unlocked (orange) |

Checks done without a device:
- ih8sn bundles its own copy of bionic's system-properties code (imported 2024). Bionic's
  property-area layout didn't change between lineage-23.0 and lineage-24.0 (only memory
  ordering and an appcompat-override environment switch), so that copy should still work on Android 17.
- FP4 declares `PRODUCT_SHIPPING_API_LEVEL := 30` (launched on Android 11). /e/OS gives FP5 and
  newer devices `FIRST_API_LEVEL=32` in ih8sn so that they look like pre-Android 13 launches. FP4 already is
  one, so the default config is right.
- From now on every build log prints `>> integrity:` lines (ih8sn binary/config/rc and microG present).

Not verifiable from here: whether FP4's KeyMint/TEE (TheMuppets lineage-24.0 blobs, 15.20.0) does
hardware key attestation on Android 17, and Google's server-side verdict.

## Owner test (after the first a17 boot; same steps on a16 for a baseline)

1. Build log: all `>> integrity:` lines say present, and `ih8sn.conf` shows the three lines above.
2. On the phone (adb, bootloader unlocked):
   ```
   adb shell getprop ro.debuggable        # expect 0 after boot (ih8sn)
   adb shell getprop ro.build.tags        # expect release-keys
   adb shell getprop ro.build.type        # expect user
   adb shell getprop ro.boot.verifiedbootstate   # orange (unlocked): expected, not a bug
   ```
3. microG self-check: Settings → System → App compatibility (microG) → Self-Check: every box ticked.
   In microG settings, sign in with a Google account and enable Google device registration and
   Cloud Messaging.
4. Install "Play Integrity API Checker" from App Lounge and run it. Record BASIC / DEVICE / STRONG.
5. Record the result in `KNOWN_ISSUES.md` (feature-parity table, "Play Integrity BASIC" row), with
   the microG version (Settings → Apps → microG Services → version). No raw logs.

## If BASIC fails on a17 but passes on a16

Change one thing per build:
1. The microG version: compare a16 and a17 builds of the same date (same prebuilts → same version
   expected; if they differ, that's the first suspect).
2. ih8sn not running: step 2 values unchanged → check `adb shell dmesg | grep ih8sn` (redact
   serials before quoting) and the sepolicy domain (`ih8sn.rc` runs it as `su`, falling back to `sysinit`).
3. `BUILD_TYPE=user` in `build.sh` instead of `userdebug` (ih8sn masks the props but not every
   userdebug difference). Note that vendor/eos turns ih8sn **off** by default on user builds;
   `remote-build.sh` still forces it on through `INCLUDE_IH8SN=true`.
4. The frameworks/base hooks: `adb logcat -s SafetyNetHooks` while running the checker; a
   "Failed to fake Build.*" line means Android 17 changed the `Build` fields.

Owners have reported BASIC regressing intermittently on /e/OS through 2026 with no confirmed root
cause (AGENT_PLAN §8), so re-test BASIC on every build.
