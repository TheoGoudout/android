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
- Permission "Android Auto as user app 2/2": needs frameworks/base 1/2 (conflicts there).
- Contacts "Default to phone-only if no account": the activity it patched is gone in AOSP 17
  (CP2 default-account APIs). Needs a fresh design check on a device.
- Dialer call recording default: already the LineageOS 24.0 default.
- overlays/Lineage icon-pack/shape overlays: LineageOS 24.0 dropped icon packs and shapes; nothing on
  a17 references them.

### packages/apps/Settings (33 patches, hand-ported)
/e/OS's `a17` Settings branch has no /e/OS changes yet. All 42 a16 commits were walked in order on
top of /e/OS `a17`: 33 carried (incl. the /e/ theming: palette, round /e/ homepage icons) (13 needed manual resolution, each noted in its commit message
under `[a17: …]`), 3 security fixes already in a17, 7 skipped:
- DNS churn (add Quad9 / revert / reapply Cloudflare / revert…). Its net effect is carried as
  "Replace cloudfare with quadnine as dns provider".
- "Add license"
- "fix security screen in setup wizard being cut in potrait mode of tablet" (tablet-only; code rewritten)

What a17 changed and how it was handled:
- The home page is now grouped in `PreferenceCategory` blocks. Updater gets its own top category;
  Accounts moves into the top `top_level_account_category`; Advanced Privacy, Parental control and
  Find my device sit in `top_level_security_privacy_category` next to Security/Privacy; the
  injected Backup tile gets `group_key` + order there.
- Some screens are Kotlin "catalyst" screens now (version, legal). /e/ titles/entries are added
  in both the XML and the Kotlin screen.
- "Remove google animations": the four navigation-mode lottie files are kept because a17 code
  still loads them.

Static checks (no compiler available here): every changed XML parses, every resource and
`com.android.settings.*` class referenced by added lines resolves, no conflict markers. Expect
the first a17 build to be the real test. To build without it, set `PATCH_EXCLUDE="packages/apps/Settings"`
in `build.sh` (works for any project path).

### frameworks/base (3 patches, on top of /e/OS a17)
/e/OS already carries 36 commits on a17 (signature spoofing, fake location, parental control
hooks, e colors…). Of the 57 a16 commits missing there:
- added: `config_deviceKeyHandler` (empty string) so the DeviceKeyHandler role that
  PermissionController now carries has a resource to resolve (on a16 the name was never
  declared). Device overlays set it.
- carried: **Hide From microG** (AppsFilter + `HIDE_MICROG_PACKAGES_FOR_PACKAGE` system setting;
  validator conflict resolved), the **USB lockdown** security fix (hand-ported; a17 still
  re-enables USB data for any user), SafetyNetHooks dockmanager Build.TYPE.
- already in a17: BAL bypass via CDM, LocalImageResolver, suspend restrictions, clipboard per-user.
- **not carried, needs a re-implementation:** Android Auto as user app (1/2) and "Allow to install
  Google signed Android Auto APK". Android 17 deleted `PermissionManagerServiceImpl` (pre-UPS
  permission code), so the privileged-permission grant has to move to the Kotlin permission service
  (`services/permission/.../AppIdPermissionPolicy.kt` / `PermissionService.kt`). Tracked in
  KNOWN_ISSUES.md.
- left to /e/OS: ~25 SystemUI light/dark/QS theming commits (Android 17 SystemUI redesign),
  UDFPS/Richtap/dock-width tweaks (not FP4 hardware), autofill UI tweaks, build-fix noise.

Tested with a sparse worktree of e/os frameworks/base a17: applies with `git am`.

### vendor/eos + vendor/lineage: "Disable private space" (re-implemented)
The a16 commit set `android.multiuser.enable_private_space_features` DISABLED. That flag no
longer exists in Android 17 (private space shipped), so:
- vendor/eos: framework overlay `config_user_types.xml` disables the
  `android.os.usertype.profile.PRIVATE` user type. With `block_private_space_creation` ENABLED
  (every AOSP release config), `UserManager.canAddPrivateProfile()` returns false and Settings
  stops offering it.
- vendor/lineage: `com.android.launcher3/enable_private_space` DISABLED in the `cp2a` value set.

Other a16 vendor/lineage commits not on a17: version/security-string bumps (a17 has its own),
MTK APN hookup (moved to vendor/eos on a17), BlissLauncher overlay rename (already on a17),
help-URL removal (file gone on a17), "Revert settings card layout" (`homepage_revamp` flag gone
in Android 17), "stop accepting the partner release type" (not carried: release-type policy
belongs to /e/OS's own a17 versioning).

### Security fixes /e/OS self-carried on a16 that LineageOS 24.0 still lacks
Checked 2026-10-16 against lineage-24.0 (frameworks/av tip 2026-10-04): the vulnerable code is
still there, and /e/OS does not fork these repos on a17.

| project | patch |
|---|---|
| frameworks/av | [media] Fix heap out-of-bounds write in MatroskaSource::read |
| packages/services/Telecomm | Check caller in CSW#queryRemoteConnectionServices |

The other a16 self-carries are already in 24.0: AudioAttributes unmarshalling, A2DP Opus, both
Nfc fixes (identical code), SDP server overflow, adb TLS use-after-free, MediaProvider ignorable
codepoints (equivalent fix present). "SDP record creation concurrency" was rewritten upstream and
counts as likely covered (not proven).

**Upstream:** each of these is a candidate merge request against the matching `e/os/<repo>` `a17`
branch (they apply cleanly there). See STATUS.md.
