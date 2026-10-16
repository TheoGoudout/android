# KNOWN ISSUES

Living list for the a17 (LineageOS 24.0) FP4 build. One row per symptom; newest first.
Never paste raw device logs here (public repo): quote only the relevant, redacted lines.

| # | Symptom | Build / date | Suspected repo | Status |
|---|---|---|---|---|
| 1 | Android Auto cannot run as a user app (a16 feature) | port, no build yet | frameworks/base (+ Permission 2/2) | Open: Android 17 removed PermissionManagerServiceImpl; the grant must be re-implemented in the Kotlin permission service. Not ported. |
| 2 | SetupWizard has no /e/ pages on plain a17 | port | SetupWizard | Workaround: `OPTIONAL_MANIFESTS="setupwizard-bringup"` (/e/OS WIP branch) |
| 4 | Launcher shows plain notification dots, not count badges (a16 feature) | port | BlissLauncher3 | /e/OS has it on `epic265-a17-bringup` (a0a4e32c5e "Show the notification count in a badge…"), not yet on `a17`; wait for /e/OS |
| 3 | /e/ palette theming missing in Settings/SystemUI/SettingsLib/apps | port | many | Left to /e/OS (Material 3 Expressive rewrite); cosmetic |

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
| Play Integrity BASIC (phase 2) | | | |
