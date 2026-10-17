# KNOWN ISSUES

Living list for the a17 (LineageOS 24.0) FP4 build. One row per symptom; newest first.
Never paste raw device logs here (public repo): quote only the relevant, redacted lines.

| # | Symptom | Build / date | Suspected repo | Status |
|---|---|---|---|---|
| 5 | /e/ Camera on FP4: privileged camera features (all lenses/modes) depend on the HAL seeing the app name | port | frameworks/av + FP4 tree + blob fixup | Ported (see patches/README "FP4 camera"). Verify on device: `adb shell getprop debug.camera.packagename` while /e/ Camera is open → `foundation.e.camera`; ultrawide and video stabilisation work. FPCamera (proprietary) not available |
| 1 | Android Auto cannot run as a user app (a16 feature) | port, no build yet | frameworks/base + Permission | Ported: grant re-implemented in the Kotlin `PermissionService` (`frameworks/base` 0025/0026, `Permission` 0004), /e/'s `AndroidAutoStub` already ships on a17. Verify on device: install Google's Android Auto over the stub, connect a car or the desktop head unit |
| 2 | SetupWizard has no /e/ pages on plain a17 | port | SetupWizard | Ported: `patches/a17/packages/apps/SetupWizard` (/e/OS bring-up squashed onto the rewritten a17 SUW). Verify on device: every page, the restore flow, 6-tap QR provisioning |
| 4 | Launcher shows plain notification dots, not count badges (a16 feature) | port | BlissLauncher3 | Ported: `patches/a17/packages/apps/Launcher3` (rebased from /e/OS bring-up a0a4e32c5e) |
| 3 | /e/ palette theming on Android 17 | port | many | Ported (Settings, SystemUI, SettingsLib, system, 6 apps, light/dark QS). Verify on device: Android 17 expressive surfaces may still show stock tones where no /e/ value existed |

## a16 → a17 feature-parity checklist (fill in after first a17 boot)

| Feature | a16 | a17 | Notes |
|---|---|---|---|
| Boots, SIM/data, calls, SMS | | | |
| VoLTE / VoWiFi | | | |
| Wi-Fi, Bluetooth, NFC, GPS | | | |
| Cameras (all lenses), flash | | | |
| Fingerprint | | | |
| Audio routing (speaker/earpiece/headset/BT); v4.3.1 distortion fix | | | |
| microG (self-check in Settings → System → App compatibility) | | | |
| App Lounge | | | |
| Advanced Privacy | | | |
| BlissLauncher3 | | | |
| Parental Control | | | |
| /e/ account (Murena cloud sync) | | | |
| OTA Updater (app opens; no official channel expected for UNOFFICIAL) | | | |
| Default apps set (Mail, Browser, Camera, etc.) | | | |
| ih8sn running, `/system/etc/ih8sn.conf` present | | | |
| Play Integrity BASIC (phase 2) | | | test steps: `PLAY_INTEGRITY.md` |
