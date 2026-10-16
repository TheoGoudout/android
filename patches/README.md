# Patch series

`remote-build.sh` applies `patches/<target>/<project path>/*.patch` with `git am -3` right after
`repo sync` (via `apply-patches.sh`) and undoes them before the next sync. A patch whose subject
the project already has is skipped, so a series retires itself as /e/OS or LineageOS merge the
same commit. A patch that no longer applies fails the build at that point. Refresh it with
`tools/port_series.py` (or by hand) and push.

Every patch keeps its original author and a `(cherry picked from commit …)` trailer pointing at
the /e/OS a16 commit. Hand-ported ones say what changed in the message.

Checked on 2026-10-16: the whole a17 set applies to fresh checkouts of /e/OS `a17` and LineageOS
`lineage-24.0` (FP4 tree). That is textual only: nothing has been compiled yet.

## a17

### device/fairphone/FP4 (LineageOS lineage-24.0 tree)
From /e/OS's own FP4 fork `e/devices/android_device_fairphone_FP4` @ `a16`, which has no `a17`
branch. /e/OS's fork also imports Fairphone's proprietary camera (FPCamera) from a private blob
set. That part is out of scope, so we stay on LineageOS's tree + TheMuppets blobs and carry only:

| patch | why |
|---|---|
| Disable adoptable storage | /e/OS policy, "not known to be working reliably" |
| Enable prioritize update process / Move Updater overlay to RRO | /e/OS Updater default |
| CarrierConfig: re-initialize from stock 15.17.2 + sort script + more overrides | /e/OS carrier configs (VoLTE/VoWiFi) |
| Switch to Murena Bootanimation | uses `TARGET_USES_MURENA_BOOTANIMATION`, present in a17 vendor/lineage |
| audio: Fix low earpiece audio | v4.3.x FP4 earpiece fix (aw882xx rx volume) |
| Revert "Remove direct flag for VOIP RX", Disable Stereo for VoIP | /e/OS FP4 VoIP audio fixes ("chipmunk" voice) |

Deliberately **not** carried: FPCamera/eCamera and their props/sepolicy/backup agent, diag_mdlog,
perf/power-HAL switches, abl pin, widevine revert, and the FCM-level/soong-bool/tinyxml2 reverts
(those only make sense with /e/OS's older 23.0 blobs, while lineage-24.0 ships 15.20.0 blobs).

### /e/OS forks whose a17 branch has no /e/OS changes yet
Replayed from /e/OS `a16` onto /e/OS `a17` (functional changes only; palette/theming commits
are left to /e/OS because they collide with the Material 3 Expressive redesign).

| project | patches | note |
|---|---|---|
| system/core | Spoof yellow verified boot state to green | Phase 2 relevant (only affects relocked custom-key boots; unlocked stays orange) |
| packages/modules/Connectivity | Replace google dns with quadnine dns | tethering DNS / connectivity probes → Quad9 |
| packages/services/Telephony | Use quad9.net for http | |
| packages/modules/Permission | RuntimePermissionsUpgradeController accepts null PermGroups | crash fix |
| packages/apps/ThemePicker | launcher-settings permissions for `foundation.e.blisslauncher` | ThemePicker ↔ BlissLauncher |
| packages/apps/Contacts | "Add account" opens AccountManager, not Google-only | hand-ported: `ContactEditorAccountsChangedActivity` was removed upstream |
| packages/apps/FMRadio, vendor/qcom/opensource/commonsys/fm | new app icon | resource-only |

Not carried, with reason:
- Permission "Add a role for deviceKeyHandler": needs `config_deviceKeyHandler` from an unported
  frameworks/base commit. Port together with frameworks/base.
- Permission "Android Auto as user app 2/2": needs frameworks/base 1/2 (conflicts there).
- Contacts "Default to phone-only if no account": the activity it patched is gone in AOSP 17
  (CP2 default-account APIs). Needs a fresh design check on a device.
- Dialer call recording default: already the LineageOS 24.0 default.
- overlays/Lineage icon-pack/shape overlays: LineageOS 24.0 dropped icon packs and shapes; nothing on
  a17 references them.

**Upstream:** each of these is a candidate merge request against the matching `e/os/<repo>` `a17`
branch (they apply cleanly there). See STATUS.md.
