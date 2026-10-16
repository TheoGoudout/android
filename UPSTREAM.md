# Upstreaming plan

Goal: every patch in `patches/a17/` should end up upstream, so this project stops carrying it.
`apply-patches.sh` skips a patch as soon as the target branch has a commit with the same subject,
so merged MRs retire themselves automatically.

The owner opens the MRs (GitLab account on gitlab.e.foundation; GitHub/Gerrit for LineageOS).
For each one: fork the repo, create a branch from the target, `git am` the patch files listed,
push, open the MR with the text below. Patches keep their original authors.

## To /e/OS (gitlab.e.foundation, target branch `a17`)

| repo | patches (`patches/a17/…`) | MR title | notes for reviewers |
|---|---|---|---|
| e/os/android_packages_apps_Settings | `packages/apps/Settings/*` (32) | "a17: port /e/OS Settings changes from a16" | Biggest one. 13 commits needed Android 17 adaptations, each explained in its `[a17: …]` note. Consider splitting: (1) home-page entries (Updater, Accounts, Advanced Privacy, Parental control, Find my device, Backup); (2) dev options + telemetry/Sentry; (3) wording/branding; (4) Quad9 private DNS. |
| e/os/android_frameworks_base | `frameworks/base/0001` | "a17: Prevent USB data changes for non-owner users during lockdown mode" | Security fix /e/OS carried on a16, still missing on a17. |
| e/os/android_frameworks_base | `frameworks/base/0002`, `0003` | "a17: Hide From microG; SNHooks dockmanager" | Clean ports, one validator-list conflict resolved. |
| e/os/android_vendor_eos | `vendor/eos/0001` | "a17: disable private space via config_user_types" | Re-implementation: a16 flag removed in Android 17. |
| e/os/android_vendor_lineage | `vendor/lineage/0001` | "a17: disable launcher private space flag (cp2a)" | Pairs with the vendor/eos MR. |
| e/os/android_system_core | `system/core/*` | "a17: Spoof yellow verified boot state to green" | Clean cherry-pick from a16. |
| e/os/android_packages_modules_Connectivity | `packages/modules/Connectivity/*` | "a17: Quad9 instead of Google DNS" | Clean. |
| e/os/android_packages_services_Telephony | `packages/services/Telephony/*` | "a17: Use quad9.net for http" | Clean. |
| e/os/android_packages_modules_Permission | `packages/modules/Permission/*` | "a17: accept null PermGroups in RuntimePermissionsUpgradeController" | Clean crash fix. |
| e/os/android_packages_apps_ThemePicker | `packages/apps/ThemePicker/*` | "a17: launcher settings permissions for BlissLauncher" | Adapted: requests both package names' permissions (a17 BlissLauncher branches differ). |
| e/os/android_packages_apps_Contacts | `packages/apps/Contacts/*` | "a17: open AccountManager on 'add account'" | Hand-ported; the a16 activity no longer exists. |
| e/os/android_packages_apps_FMRadio, e/os/android_vendor_qcom_opensource_fm-commonsys | `…/FMRadio/*`, `…/fm/*` | "a17: new app icon" | Resource-only. |

Not for /e/OS: `frameworks/av` and `packages/services/Telecomm` (LineageOS repos on a17, see below),
and `device/fairphone/FP4` (see below).

## To LineageOS (lineage-24.0)

Security fixes that /e/OS self-carried on a16 and that lineage-24.0 (tip checked 2026-10-16) still lacks.
These are AOSP fixes, so the right outcome is LineageOS picking them up (Gerrit: review.lineageos.org,
or report to the LineageOS team so they merge the ASB change):

| project | patch | upstream reference |
|---|---|---|
| LineageOS/android_frameworks_av | `frameworks/av/0001` "[media] Fix heap out-of-bounds write in MatroskaSource::read" | AOSP commit carried by /e/OS a16 (2026-04-08) |
| LineageOS/android_packages_services_Telecomm | `packages/services/Telecomm/0001` "Check caller in CSW#queryRemoteConnectionServices" | AOSP commit carried by /e/OS a16 (2026-05-07) |

Before reporting, re-check lineage-24.0: they may already have landed under another subject.

## FP4 device tree

`patches/a17/device/fairphone/FP4/*` come from /e/OS's own FP4 fork (`e/devices/android_device_fairphone_FP4`,
branch `a16`, no `a17` yet). Ask /e/OS to create an `a17` branch of that fork based on
LineageOS `lineage-24.0` and propose these 10 patches there. The audio fixes (earpiece volume,
VoIP direct flag, VoIP stereo) could also be offered to LineageOS's FP4 tree, since they fix
hardware behaviour for everyone.

## Status

| MR | opened | merged |
|---|---|---|
| (none yet) | | |
