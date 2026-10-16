# /e/OS a17: commits carried on top of lineage-24.0

(Run with --old = --new = lineage-24.0, so "e commits" = what /e/OS has already ported to a17. "Conflicts" here only mean a commit was not written on top of lineage-24.0 (repos tracked on `main`/`develop`, or history merged in from older branches); they are not port work.)

- forked repos audited: 39
- /e/OS commits on top of lineage-24.0: 299
- already upstream in lineage-24.0 (dropped): 0
- apply cleanly: 229
- conflict (manual port): 70

| path | status | e commits | upstream | clean | conflicts |
|---|---|---|---|---|---|
| packages/apps/Updater | ok | 49 | 0 | 7 | 42 |
| packages/apps/Launcher3 | ok | 44 | 0 | 28 | 16 |
| packages/inputmethods/LatinIME | ok | 15 | 0 | 9 | 6 |
| vendor/apn | ok | 26 | 0 | 22 | 4 |
| packages/apps/Backgrounds | ok | 7 | 0 | 5 | 2 |
| bootable/deprecated-ota | ok | 3 | 0 | 3 | 0 |
| bootable/recovery | ok | 6 | 0 | 6 | 0 |
| build/soong | ok | 5 | 0 | 5 | 0 |
| device/lineage/sepolicy | ok | 9 | 0 | 9 | 0 |
| external/ih8sn | eos-only | 0 | 0 | 0 | 0 |
| external/prebuiltapks | eos-only | 0 | 0 | 0 | 0 |
| external/svox | eos-only | 0 | 0 | 0 | 0 |
| frameworks/base | ok | 36 | 0 | 36 | 0 |
| frameworks/libs/systemui | ok | 1 | 0 | 1 | 0 |
| frameworks/opt/vcard | ok | 3 | 0 | 3 | 0 |
| lineage-sdk | ok | 6 | 0 | 6 | 0 |
| packages/apps/Contacts | ok | 11 | 0 | 11 | 0 |
| packages/apps/Dialer | ok | 4 | 0 | 4 | 0 |
| packages/apps/DocumentsUI | ok | 3 | 0 | 3 | 0 |
| packages/apps/EmergencyInfo | ok | 3 | 0 | 3 | 0 |
| packages/apps/FMRadio | ok | 1 | 0 | 1 | 0 |
| packages/apps/Gallery2 | ok | 4 | 0 | 4 | 0 |
| packages/apps/ImsServiceEntitlement | ok | 3 | 0 | 3 | 0 |
| packages/apps/LineageParts | ok | 12 | 0 | 12 | 0 |
| packages/apps/Settings | ok | 1 | 0 | 1 | 0 |
| packages/apps/SettingsIntelligence | ok | 1 | 0 | 1 | 0 |
| packages/apps/SetupWizard | ok | 1 | 0 | 1 | 0 |
| packages/apps/ThemePicker | ok | 1 | 0 | 1 | 0 |
| packages/apps/WallpaperPicker2 | ok | 1 | 0 | 1 | 0 |
| packages/apps/elib | eos-only | 0 | 0 | 0 | 0 |
| packages/modules/Connectivity | ok | 1 | 0 | 1 | 0 |
| packages/modules/DnsResolver | ok | 1 | 0 | 1 | 0 |
| packages/modules/Permission | ok | 1 | 0 | 1 | 0 |
| packages/overlays/Lineage | ok | 1 | 0 | 1 | 0 |
| packages/services/Telephony | ok | 1 | 0 | 1 | 0 |
| system/core | ok | 1 | 0 | 1 | 0 |
| vendor/eos | eos-only | 0 | 0 | 0 | 0 |
| vendor/lineage | ok | 36 | 0 | 36 | 0 |
| vendor/qcom/opensource/commonsys/fm | ok | 1 | 0 | 1 | 0 |

## Conflicting commits

### packages/apps/Backgrounds
- 082352b7b545 Add phone wallpapers  [res/values/arrays.xml]
- b81ff2590c2d Update wallpapers  [res_phone/values/arrays.xml]

### packages/apps/Launcher3
- 1dbe9cca7358 Revert "Launcher3: Ability to toggle themed icons for all apps"  [src/com/android/launcher3/BubbleTextView.java]
- a7110c107381 Add workspace as drawer mode  [res/xml/launcher_preferences.xml, src/com/android/launcher3/LauncherPrefs.kt]
- c043046ce5b7 Disable workspace widgets in workspace-as-drawer mode  [src/com/android/launcher3/Launcher.java, src/com/android/launcher3/popup/WorkspaceLongPressOptions.kt, src/com/android/launcher3/util/KeyboardShortcutsDelegate.java]
- 84077d2bfcf7 Use Untitled as default folder name  [res/values-bs/lineage_strings.xml]
- c830b434a941 Auto arrange icons in workspace as drawer mode  [src/com/android/launcher3/model/LoaderTask.java, src/foundation/e/blisslauncher/WorkspaceAsDrawerSyncTask.kt]
- cdc2b0741286 Sort apps added in workspace as drawer mode  [src/foundation/e/blisslauncher/WorkspaceAsDrawerSyncTask.kt]
- a82cb7b10c20 Add sharp square for /e/  [res/values/e_strings.xml]
- 75b6a4c892f3 Restyle folders for /e/ and use 3x3  [src/com/android/launcher3/DeleteDropTarget.java, src/foundation/e/blisslauncher/WorkspaceAsDrawerPolicy.kt]
- 10688920c7d6 Blur folders using wallpaper  [res/values/colors.xml, res/values/styles.xml, src/com/android/launcher3/folder/Folder.java]
- 7859b23014dd Replace the -1 page with a widgets page  [res/values/colors.xml, res/values/e_strings.xml, src/com/android/launcher3/Hotseat.java, src/com/android/launcher3/widgetpicker/WidgetPickerActivity.kt ...]
- 625e84c7a5cc Hide few apps to the home screen used as the app drawer  [res/values/e_config.xml, src/foundation/e/blisslauncher/WorkspaceAsDrawerSyncTask.kt, src/foundation/e/blisslauncher/widgetspanel/WidgetsPanelSearchState.kt]
- 7c2e5e7a803d Add widgets pinned by apps to the widgets page  [res/values/e_strings.xml, src/com/android/launcher3/dragndrop/AddItemActivity.kt, src/com/android/launcher3/widgetpicker/WidgetPickerComposeWrapperImpl.kt, src/foundation/e/blisslauncher/widgetspanel/WidgetsPanelModel.kt ...]
- 5616c7f8c7e3 Revert "fixup! Launcher3: Ability to toggle themed icons for all apps"  [src/com/android/launcher3/BubbleTextView.java]
- a4daeccc6029 Use the BlissLauncher name and icon  [res/values/e_strings.xml]
- b3bcf29b16a0 Wobble the icons to move or uninstall apps  [res/values/colors.xml, src/com/android/launcher3/Launcher.java, src/com/android/launcher3/Workspace.java, src/foundation/e/blisslauncher/widgetspanel/SwipeSearch.kt]
- 3a0be9f14b35 Make room on a full page for a dropped app  [src/com/android/launcher3/CellLayout.java, src/com/android/launcher3/Workspace.java]

### packages/apps/Updater
- c7c653ae7cb4 Updater: Init android studio support  [app/Android.bp, app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/res_aosp/values/symbols.xml]
- d3906ff27c25 Updater: Update gradle deps  [app/build.gradle.kts, build.gradle.kts, gradle.properties, gradle/wrapper/gradle-wrapper.properties]
- 754beb6c03c4 Updater: Rebrand to /e/ OS  [app/src/main/java/org/lineageos/updater/UpdaterReceiver.java, app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/java/org/lineageos/updater/controller/UpdaterService.java]
- 5cd5471e2b0b Updater: Get /e/ release notes  [app/src/main/java/org/lineageos/updater/misc/Constants.java, app/src/main/java/org/lineageos/updater/misc/Utils.java, app/src/main/res/menu/menu_toolbar.xml, app/src/main/res/values/e_strings.xml ...]
- 94f5325a3bab Updater: Update the OTA url  [app/src/main/res/values/strings.xml]
- 23c3ba3bdbdd Updater: Allow OTA updates with different version number  [app/src/main/java/org/lineageos/updater/misc/Utils.java]
- 32fcd6ef7780 Updater: Use helper function for parsing version code  [app/src/main/java/org/lineageos/updater/misc/Utils.java]
- f68803009882 Updater: Check updates daily  [app/src/main/java/org/lineageos/updater/misc/Utils.java]
- 596c2099d35e Updater: Enable auto deletion of updates by default  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/controller/UpdaterService.java, app/src/main/java/org/lineageos/updater/misc/Utils.java]
- 0b1cf97aa2c4 Updater: Rework logic to check for new updates  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/UpdatesCheckReceiver.java, app/src/main/java/org/lineageos/updater/misc/Utils.java]
- f3494ca94539 Updater: Check in Settings if the device has to fetch updates from the staging OTA server  [app/src/main/java/org/lineageos/updater/misc/Utils.java, app/src/main/res/values/strings.xml]
- edfcb984637f Change displayed version value  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/UpdatesDbHelper.java, app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/java/org/lineageos/updater/misc/BuildInfoUtils.java ...]
- e4d16f9b6ab0 Updater: Change dialog text  [app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/res/values/e_strings.xml]
- cccd5d36383a Updater: UpdatesCheckReceiver: Migrate to setExactAndAllowWhileIdle  [app/privapp_whitelist_org.lineageos.updater.xml, app/src/main/java/org/lineageos/updater/UpdatesCheckReceiver.java]
- 28dbae17024b Updater: Add support for SystemUpdateManager status  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/UpdatesCheckReceiver.java, app/src/main/java/org/lineageos/updater/controller/UpdaterService.java, app/src/main/java/org/lineageos/updater/misc/Utils.java]
- 3bf2fafd5452 Change current version title to our brand name  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/res/values/e_strings.xml]
- 8353ecc3aa29 Updater: Dont crash and hide lower android version  [app/src/main/java/org/lineageos/updater/UpdatesDbHelper.java, app/src/main/java/org/lineageos/updater/controller/UpdaterService.java, app/src/main/java/org/lineageos/updater/misc/Utils.java, app/src/main/java/org/lineageos/updater/model/UpdateBase.java ...]
- 07260d53a477 Improvements in system page  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/res/layout/activity_updates.xml, app/src/main/res/values/e_strings.xml]
- 029b3eb1a5bf Updater: add additional intervals for debug  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/misc/Constants.java, app/src/main/java/org/lineageos/updater/misc/Utils.java, app/src/main/res/layout/preferences_dialog.xml ...]
- 85daeac0b5f8 Updater: Add network ConnectionStateMonitor  [app/Android.bp, app/src/main/java/org/lineageos/updater/UpdatesCheckReceiver.java, app/src/main/java/org/lineageos/updater/controller/UpdaterService.java, app/src/main/java/org/lineageos/updater/misc/Constants.java]
- 51584570c31d Updater: Allow A/B devices to override update priority  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/res/values/config.xml, app/src/main/res_aosp/values/symbols.xml]
- 91ad35ad52d6 Updater: Check for free space on install  [app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/java/org/lineageos/updater/misc/Utils.java, app/src/main/res/values/e_strings.xml]
- 5a31745f8002 Updater: Utils: Move battery level check  [app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/java/org/lineageos/updater/misc/Utils.java]
- 0017beead619 Updater: Update A/B devices on one go  [app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/java/org/lineageos/updater/controller/UpdaterService.java, app/src/main/res/values/strings.xml]
- 9b4ffc56158f Updater: Generate anon id for ota requests  [app/privapp_whitelist_org.lineageos.updater.xml, app/src/main/AndroidManifest.xml, app/src/main/java/org/lineageos/updater/UpdatesCheckReceiver.java, app/src/main/java/org/lineageos/updater/misc/Constants.java ...]
- 41b931154040 Updater: Improve UX for users taking version upgrades  [app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/java/org/lineageos/updater/model/UpdateBase.java, app/src/main/res/layout/update_item_view.xml]
- c8bab82fd936 Move our string modifications to e_strings.xml  [app/src/main/java/org/lineageos/updater/UpdaterReceiver.java, app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java, app/src/main/java/org/lineageos/updater/controller/UpdaterService.java ...]
- 5640a10f2ebd Update: add json validator  [app/src/main/java/org/lineageos/updater/UpdatesCheckReceiver.java, app/src/main/java/org/lineageos/updater/misc/Utils.java]
- 525ca2c4eb21 Make ui improvements in update list  [app/src/main/res/layout/activity_updates.xml, app/src/main/res/layout/update_item_view.xml]
- 32cde1706bcc Updater: /e/ changes for local update  [app/src/main/java/org/lineageos/updater/UpdateImporter.java]
- eefac43f5f80 Updater: add option to show all updates  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/misc/Constants.java, app/src/main/java/org/lineageos/updater/misc/Utils.java, app/src/main/res/layout/preferences_dialog.xml ...]
- a1853351ea57 Port translations from Android 14  [app/src/main/res/values-de/e_strings.xml, app/src/main/res/values-es/e_strings.xml, app/src/main/res/values-fr/e_strings.xml, app/src/main/res/values-is/e_strings.xml ...]
- 397467044331 Updater: Disable every update info and welcome dialog  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/UpdatesListAdapter.java]
- d8bb8db85530 Updater: Add permanent reboot notification & delete update  [app/src/main/java/org/lineageos/updater/UpdateImporter.java, app/src/main/java/org/lineageos/updater/UpdaterReceiver.java, app/src/main/java/org/lineageos/updater/UpdatesCheckReceiver.java, app/src/main/java/org/lineageos/updater/controller/UpdaterService.java ...]
- 1bc81a22ed0a Theme app according to our pallete  [app/Android.bp, app/build.gradle.kts, app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/res/layout/activity_updates.xml ...]
- 699130744d5a Updater: Hide update available when needed  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/res/layout/activity_updates.xml]
- c2a80998c61e Updater: Change preference to reset default value  [app/src/main/java/org/lineageos/updater/UpdatesActivity.java, app/src/main/java/org/lineageos/updater/controller/ABUpdateInstaller.java, app/src/main/java/org/lineageos/updater/misc/Constants.java, app/src/main/java/org/lineageos/updater/misc/Utils.java]
- af77237c0b78 Remove hardcoded android version  [app/src/main/java/org/lineageos/updater/misc/Utils.java, app/src/main/res/values/e_strings.xml]
- 9f40c1f9e25c Use custom tab intent for changelog  [app/Android.bp, app/build.gradle.kts, app/src/main/java/org/lineageos/updater/UpdatesActivity.java]
- b1101b4970ed Automatic translation import  [app/src/main/res/values-sc-rIT/strings.xml]
- 076eeb6ee50f Fix android version checks  [app/src/main/java/org/lineageos/updater/UpdateImporter.java, app/src/main/java/org/lineageos/updater/misc/BuildInfoUtils.java, app/src/main/java/org/lineageos/updater/misc/Constants.java, app/src/main/java/org/lineageos/updater/misc/Utils.java ...]
- 9d18b4063d36 Guard against missing SystemUpdateManager instance  [app/src/main/java/org/lineageos/updater/misc/Utils.java]

### packages/inputmethods/LatinIME
- b47359b28001 LatinIME: add elib  [java/Android.bp]
- c73962b9ccd6 LatinIME: Add icon on the keyboard to access STT feature  [java/res/layout/main_keyboard_frame.xml]
- b3051f02a154 LatinIME: Remove building broken tests  [build.gradle]
- 849640d8898e feat(stt): target the offline STT keyboard and drop premium gating  [java/src/com/android/inputmethod/latin/LatinIME.java]
- 01bbd64c7a48 Show mic on the strip when suggestions are disabled  [java/src/com/android/inputmethod/latin/LatinIME.java]
- 48437f7433c7 Rename the floating button to the STT button  [java/res/layout/main_keyboard_frame.xml, java/src/com/android/inputmethod/latin/LatinIME.java]

### vendor/apn
- b0e6b3f15547 Move our apn config from vendor_lineage  [DE.xml, FR.xml, US.xml]
- dec9ef4c87ac apns: Use the proper settings for SFR (MCC 208 with MNC 10)  [FR.xml]
- 2a5c6c614e97 FR: fix Free Mobile APN - add IPv4 protocol and hipri type for MMS  [FR.xml]
- a37eabc259f9 FR.xml: add type for SFR IMS  [FR.xml]

## Notes
- external/ih8sn: Repo has no LineageOS counterpart at this path: no rebase, only build-test it.
- packages/apps/elib: Repo has no LineageOS counterpart at this path: no rebase, only build-test it.
- external/prebuiltapks: Repo has no LineageOS counterpart at this path: no rebase, only build-test it.
- external/svox: Repo has no LineageOS counterpart at this path: no rebase, only build-test it.
- vendor/eos: Repo has no LineageOS counterpart at this path: no rebase, only build-test it.
