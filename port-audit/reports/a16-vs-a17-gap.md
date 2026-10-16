# a16 /e/OS patches not (yet) on a17

Generated 2026-10-16 from the two port_audit runs (a16 on lineage-23.0 vs lineage-24.0;
a17 vs lineage-24.0). A commit counts as *needed* if it is on /e/OS a16, is not already in
lineage-24.0 (same subject) and is not CI plumbing; *present on a17* matches by subject only, so
squashed or reworded ports show as missing (likely for BlissLauncher3, rebuilt on a17).

| repo | a16 /e/ commits still needed on 24.0 | present on a17 (by subject) | missing |
|---|---|---|---|
| packages/apps/Launcher3 | 324 | 8 | 316 |
| frameworks/base | 91 | 34 | 57 |
| packages/apps/Settings | 42 | 0 | 42 |
| packages/apps/SetupWizard | 33 | 0 | 33 |
| vendor/lineage | 69 | 36 | 33 |
| frameworks/libs/systemui | 25 | 0 | 25 |
| packages/modules/Permission | 13 | 0 | 13 |
| packages/apps/ThemePicker | 5 | 0 | 5 |
| packages/modules/DnsResolver | 5 | 0 | 5 |
| packages/apps/LineageParts | 15 | 11 | 4 |
| packages/modules/Connectivity | 4 | 0 | 4 |
| packages/apps/WallpaperPicker2 | 3 | 0 | 3 |
| packages/overlays/Lineage | 3 | 0 | 3 |
| packages/apps/Contacts | 12 | 10 | 2 |
| packages/apps/FMRadio | 2 | 0 | 2 |
| packages/apps/SettingsIntelligence | 2 | 0 | 2 |
| packages/services/Telephony | 2 | 0 | 2 |
| vendor/qcom/opensource/commonsys/fm | 2 | 0 | 2 |
| packages/apps/Dialer | 4 | 3 | 1 |
| packages/apps/DocumentsUI | 3 | 2 | 1 |
| system/core | 1 | 0 | 1 |
| android | 3 | n/a (not forked on a17) | 0 |
| bootable/deprecated-ota | 2 | 2 | 0 |
| bootable/recovery | 5 | 5 | 0 |
| build/release | 4 | n/a (not forked on a17) | 0 |
| build/soong | 4 | 4 | 0 |
| device/lineage/sepolicy | 8 | 8 | 0 |
| external/dng_sdk | 0 | n/a (not forked on a17) | 0 |
| external/libopenapv | 2 | n/a (not forked on a17) | 0 |
| external/libpng | 1 | n/a (not forked on a17) | 0 |
| external/sqlite | 1 | n/a (not forked on a17) | 0 |
| frameworks/av | 4 | n/a (not forked on a17) | 0 |
| frameworks/native | 3 | n/a (not forked on a17) | 0 |
| frameworks/opt/vcard | 2 | 2 | 0 |
| hardware/qcom-caf/thermal | 0 | n/a (not forked on a17) | 0 |
| hardware/st/nfc | 0 | n/a (not forked on a17) | 0 |
| lineage-sdk | 5 | 5 | 0 |
| packages/apps/Backgrounds | 6 | 6 | 0 |
| packages/apps/CertInstaller | 1 | n/a (not forked on a17) | 0 |
| packages/apps/EmergencyInfo | 2 | 2 | 0 |
| packages/apps/Gallery2 | 3 | 3 | 0 |
| packages/apps/ImsServiceEntitlement | 2 | 2 | 0 |
| packages/apps/KeyChain | 1 | n/a (not forked on a17) | 0 |
| packages/apps/Updater | 45 | 45 | 0 |
| packages/inputmethods/LatinIME | 14 | 14 | 0 |
| packages/modules/Bluetooth | 4 | n/a (not forked on a17) | 0 |
| packages/modules/Nfc | 3 | n/a (not forked on a17) | 0 |
| packages/modules/Profiling | 1 | n/a (not forked on a17) | 0 |
| packages/modules/Virtualization | 1 | n/a (not forked on a17) | 0 |
| packages/modules/adb | 3 | n/a (not forked on a17) | 0 |
| packages/providers/ContactsProvider | 1 | n/a (not forked on a17) | 0 |
| packages/providers/MediaProvider | 2 | n/a (not forked on a17) | 0 |
| packages/providers/TelephonyProvider | 1 | n/a (not forked on a17) | 0 |
| packages/services/Telecomm | 2 | n/a (not forked on a17) | 0 |
| system/apex | 1 | n/a (not forked on a17) | 0 |
| vendor/apn | 25 | 25 | 0 |


### packages/apps/Launcher3 (316 missing on a17)
- fix: restore the murena green on notification badges
- Revert "Merge branch '9400-a16-badge-placement' into 'v4.3-a16'"
- Revert "Merge branch '9400-a16-dot-density-headroom' into 'v4.3-a16'"
- fix: floor the notification dot at an absolute minimum size
- fix: make the notification badge/icon ratio constant across densities
- fix: report the real rendered workspace cell content height
- spec: define the notification badge's use cases in Gherkin
- test: cover tablet-mode badge sizing and corner-anchor
- test: apply jonathanklee's style comments on DotRendererTest
- fix: address rhandros/jonathanklee review follow-ups on the badge fix
- test: sweep the badge corner-anchor regression across display sizes
- fix(a16): drop duplicate notification_dot_bg definition
- fix: guarantee enough top padding for the notification dot
- refactor: drop unused themeManager param from createDotRenderer
- chore: bump libs_systemui to the badge geometry fix
- test: pixel-test the notification badge and run tests in CI
- fix: compute the widget panel span from the live orientation
- fix: restore the murena green on notification badges
- fix: anchor the notification dot on the real icon mask
- Blisslauncher: Properly rearraneg hotseat if some app doesnt restore
- Bump version to 3.1.3
- fix!: Update class name for app lounge
- Update jars
- blisslauncher: Set wallapaper offsets from main thread and early
- Reorder apps after setup restore
- feat: Fix widget restore after backup
- Launcher3: prevent duplicate icon during restore
- Update backup scheme
- blissinput: Fix search key not working
- Fix blur drawable recycled bitmap crash
- Add serialization plugin for Soong builds
- add missing okio dependency
- feat: Defer onLoadAllAppsEnd if launcherModel is null atm
- Hide all apps in tasksbar
- (fix): Avoid negative hotseat space scenario on configuration change
- Use correct icon overlap factor
- Fix tablet/phone hotseat padding
- feat: Fix random widget spancount issue
- feat: Use eSwitch for settings
- bliss: Fix nav bar on tablet & phone
- feat: Don't allow adding webapk early setup
- (fix): Revert back to AOSP icon push mechanism
- (fix): Remove duplicate pushIconByRow
- feat: add murena qwant search
- feat: Disable blurring in dock
- fix!: Add missing return in transpose mapPresenterToModel
- feat: Adjust no hint gesture hotseat height
- feat: fix hotseat padding on tablet
- feat: Fix null exception on apk update
- feat: Fix hotseat paddings on phones
- feat: hide parent app badges from shortcuts
- feat: Readd navbar color for phones
- feat: Set blur radius for dock to 2
- fix!: Copy bitmap before applying to canvas
- fix: Nudge down hotseat correctly when no-hint gesture in use
- fix!: Resolve getWriter args in BaseLauncherBinder
- Revert "Use the number of shown hotseat icons instead of database items to store into the DB"
- feat: align taskbar on orientation change
- fix: null-check widgetFragment before cast
- feat: Fix crash in emulator
- fix: Ensure dock bounds are aligned on phone
- fix!: Ensure at or above window insets on minus-one
- fix: Properly pick width for app suggestions
- fix: Resolve determination of next empty space in landscape
- fix!: Update class name for app lounge
- fix!: Use iconSizePx to render part of widget, to determine real height
- fix: Update class and packageName for hotseat gallery
- feat: Set hotseat icons to 8
- feat: Set icon scale to upto 1.4f dynamically
- fix: Improve handling of hotseat size handling on tablets
- fix: Use correct iconSize when updating
- fix: De-jank blurring on DPI change
- fix: Properly handle tablet notification icons [2/2]
- fix: Add vertical margin to match mockup
- fix: Reduce horizontal margin in landscape
- fix: Ensure widget list is mutable
- fix: Improve translation reliability
- feat: Readd widget resizing, relayout staggered view post-resize
- fix: Prioritize first-load of model
- fix: Make gestural properly layout dock icons too
- chore: Use `context.getResources()` in updateHotseatSizes
- fix: Properly determine home screen using isInLauncher too
- feat: Animate navigation buttons to center them on home
- feat: Allow any number of hotseat icons, move nav below dock
- feat: Enable hotseat centering for all
- feat: Disable navbar translation with taskbar
- feat: Disable morph for all
- fix: Upscale icons to 1.6x and improve hotseat spacing
- feat: Welcome upto 9 hotseat icons
- fix: Increase icon size before DPI selection
- chore: Address CR
- fix: Add margin to hotseat, prevent clipping
- fix: Readjust hotseat paddings for latest CL
- fix: Recalculate wallpaper offset on rotate
- feat: Use workspace insets on minus one
- fix: Improve height calculation for spanCount = 1
- fix: Make wallpaper offsets revert to 0 if height is same
- fix: Improve hotseat size on verticalBar
- fix: Fix UX on rotated phone layouts
- feat: Add horizontal padding to minus one in landscape & dynamic height
- feat: StaggeredGridLayout for tablet and landscape on minus one
- fix: Add translations in cellLayout for centering dock
- Revert "fix: Apply center vertical padding to folders as well"
- feat: Re-enable transition and disable centering for non gestural mode
- fix: Workaround taskbar-hotseat animation mis-align
- feat: Increase iconSize for tablet by 1.25f
- feat: Fix hotseat spacing, update default hotseat
- feat: Make tablets follow 4_by_6 grid
- feat: Enable transpose cell mapping for all
- feat: Improve cellLayout paddings for tablet
- feat: Properly apply translation for centered dock
- fix: Tons of fixes
- fix: Resolve multiple NPEs when folder in taskbar
- feat: Fix hotseat & taskbar item positions, remove all apps
- fix: Zero out portrait padding for tablet
- fix: Improve dock paddings in VerticalBarLayout
- fix: Tune hotseat paddings in no-hint gestural mode
- fix: Fix landscape grid dimensions in LoaderCursor
- fix: Use DeviceProfile instead for PageIndicator insets
- fix: Improve positioning of hotseat icons
- fix: Stop wobbling layouts on orientation changed
- chore: Change setting name as per CR of base
- fix: Reduce navigation bar height from launcher_dock_width
- fix: Rework hotseat size and paddings
- fix: Properly pad upside-down orientation for nav height
- fix: Properly handle rows and columns on commit with Transpose mapper
- feat: Fade out dock blur on scroll to minus one
- feat: Improve translation of dock in verticalbar
- feat: Add setting to communicate dock width
- feat: Blur the dock again!
- fix: Make blurring "continuous" in dock
- fix: Properly track minus one progress and indicator translation
- feat: Add flag to force-show workspace labels
- feat: Introduce grid transpose and dimension swapping
- fix: Redo Workspace and CellLayout paddings
- fix: NPE on Launcher inflate in landscape
- chore: @SuppressLint("NewApi") for setPageIndicatorInset
- feat: Fix position of page indicator
- Revert "fix hotseat size for tablet"
- fix hotseat size for tablet
- fix: Restore workspace when we leave seachContainer
- Fix crash when using thirdparty launcher
- (fix) Hide/show current page and hotseat on swipeSearchContainer
- Use const var for workspace widget page
- Re-apply state for widget page
- feat: Don't close folder on wiggle
- Allow all chars for swipe down search
- Import weblate translations from a15
- Fix widget panel crash
- Fix runtime exception and page indicator color
- (fix) Update workspace item hide logic
- fix: Update click receivers for two-pane widget picker as well
- feat: Disable blurring in dock
- feat: Drop retrofit, kio and gson
- feat: adjust dot size according to density
- Fix hotseat padding
- bliss: Fix folder crash
- feat: Don't close opened folder
- feat: Change page move offset
- feat: Avoid calling loadsuggestions continuously for app suspend
- feat: Close widget add view after adding
- launcher: Dont allow 3rd party apps to place widgets on homescreen
- feat: Check for null case
- blisslauncher: Fix abstract crash as seen on sentry
- feat: Check for widgets before rebind
- feat: Use correct context
- feat: set default widget left/right padding
- feat: Remove adding extra space on hotseat
- feat: add a default padding for widget
- feat: Use fixed corner radius value
- feat: add suggestions bottom padding
- feat: Use Bliss1 padding
- feat: Fix widgets padding
- feat: Remove pwa if doesn't exists in db
- widgets: Properly update widget options
- feat: Use existing dbhelper
- feat: Fix item id after migration
- fix(notificiation): Add wrapper component in the list of listener too
- Extract show notificaton count to a string so that it can be translated
- theme settings page according to our palette
- feat: Use a transparent wall for live
- feat: Adjust widgetcontainer padding
- test blur
- feat(widget): Remove shortcuts from widget list
- change the way how we init
- fix(drag): Fix icon getting stuck
- feat(widget): Use launcher to handle activity result also remove internal api usage
- fix(folder): Concurrent exception
- feat: Remove rotation for phones
- feat: Use correct userid for user profiles
- fix(worksspace): Fix Indicators not updating
- feat: Reload suggestions with fresh data
- feat: Fix hotseat visibility
- feat: Sort widget list
- icon drag test
- remove screenshot button from quickstep overview actions
- fix(widget): Remove widgets not present in db
- fix(widget): Close all views when widget is selected
- fix(folder): folder uninstall clear animation
- feat(widget): Clean widget screen
- feat: Allow scrolling in widget remove page
- feat: Do not allow empty first screen
- feat: Move remove widget for translation
- fix(appUsageStats): Sort apps properly and filter them
- fix(folder): Have equal size folder
- fix(reorder): Fix bug with reorder while taking icons out of folder
- fix(pwa): fix app lounge getting unresponsive
- fix(widget): Properly fetch insets
- fix(pwa): Fix icons not rearranging on pwa removal
- fix(widget): Host not listening on initial boot
- fix(widget): Fix unrepsonsive widgets at time
- fix(widget) : Fix configured widget being cancelled yet appearing in removed list
- fix(widget) : Properly account for -1 page so touch are intercepted correctly
- fix(folder): revert back to old opened folder color
- fix(rearrange): Remove delayed timing to rearrange
- fix(folder): Make folder animation bit better
- fix(blur) : Add wallpaper scroll to layouts
- fix(dock): properly space in gesture mode
- fix(cell): icons not rearranging properly
- fix(reorder): fix animation of last item
- fix: folder background and preview colors
- fix: add more null checks
- fix: multiply non gesture mode dock spacing by 1.5f
- fix: dont specify width let layout decide one
- fix: Simpily -1 widget screen scroll logic
- fix: suggestion layout padding and resources crash
- fix: Fix widgetInfo being null and crashing the launcher
- fix: center hotseat icons again
- fix: set bubble text view center vertically
- fix: padding in apps suggestion
- chore: blur and opacity improvements
- feat(widget) : Properly sets insets and utilise full screen
- feat: adjust suggestions icons position aswelll
- feat: adjust grid margin and padding
- feat(notification): Add support for notification dot shadow
- fix: unhide notification dot on drag close
- fix(notifications): Fix notification dots not working after migration
- AppUsageStats: Properly check for permission
- (feat) widgets: properly migrate widget host
- Folder: Dont mark folder as unmovable when its grid folder
- (feat) widgets: properly hides resize container
- (feat) Hotseat: Auto reorder hotseat icons
- feat: Fix new weather app migration
- [tmp] animation: remove staggered animation
- chore: some fixes
- redorder fixes
- chore: misc changes
- fix: handle fast and long touch properly
- fix(icons): decrease page move offset and set initial page
- fix(wobble): enable touch listener in folder too
- fix: hide education tips in single layer mode
- fix: decrease max folder creation radius
- feat(wobble): enable drag on normal touch
- fix: folder default naming and click handling
- fix: increase size of page indicator dots
- feat(grid): implementation of ios reorder logic
- fix(multimode): misc fixes for drawer mode
- refactor: add sentry integration and replace logging with Timber
- feat(idp): increase icon size by a factor of 1.3
- refactor: use LauncherPrefs for custom preferences
- feat(widgets): implement resize/remove on -1 page
- feat(gardening): enable gardening for single layer
- fix: wobble inside grid folder
- chore: don't animate app icons when reordering
- feat(db): add widget migration
- chore(hotseat): center hotseat icons
- fix(qsb): remove padding only from -1 screen
- chore: replace logging with a custom logger
- fix: hide contextual menu from homescreen
- feat(icon): add new adaptive app icon
- fix(workspace): remove shadow from app & folder names
- fix: do not draw blur over hotseat if in preview
- feat(animation): disable spring icon animation in single layer mode
- chore(flags): set ENABLE_ICON_LABEL_AUTO_SCALING to false and NOTIFY_CRASHES to true
- fix: don't show all apps animation swipe
- fix(folder): improve folder animations and give default name
- feat(db): support for database migration
- feat(search): add swipe down search layout and methods
- feat(badges): hide parent app badges from shortcuts
- chore: cleanup lineage defaults from workspaces
- feat(wobble): add wobble animations to apps and folders
- feat(badges): show notification count in app badges
- feat(status bar): hide status bar on widgets page
- feat(pwa): allow applounge to place shortcuts directly
- feat: implementation for grid folder
- Remove hotseat bottom space
- chore: reference colors and styles from elib
- feat(blur): add all related utils, layouts and apply on default widgets
- feat(navbar): add opacity animation for widgets page
- feat: force alias selected apps through array
- fix(home): default page and hotseat coming back
- feat(widgets): use QSB view for widgets screen
- feat(workspace): hide scrim shadow layer on launcher root view
- feat(workspace): set font style to normal and decrease font spacing b/w icon
- feat: hide some apps from placing on homescreen
- feat(settings): hide option to disable new app icons on homescreen on non drawer
- feat(drawer): disable app drawer gesture on single layer mode
- feat(hotseat): copy default config to drawer mode table too
- feat(shortcuts): query deepshortcuts from both tables instead of workspace
- feat(widgets): do not remove widgets if available in either table
- Keep margin same as cell spacing
- feat(multimode): Add initial no Drawer Mode
- feat(multimode): add all monitor callbacks
- Use buildconfig generated for studio
- Fix accessing resources for studio build
- Always show page indictor dots
- Disable unsupported app grid
- chore: add spotless formatting tasks for bliss
- feat: add incrementing versionCode
- Change app icon and name
- Update jars based on December security patch
- Init support for android studio
- bliss: add LICENSE
- BL3: add libs_systemui submodule
- Revert "Trebuchet: Use HiddenAppsFilter for all apps list"
- Launcher3: Drop injectPress in favor of newly added onKeyEvent method

### frameworks/base (57 missing on a17)
- [25Q2] Mitigate BAL bypass via Companion Device Manager
- [LocalImageResolver] Fix security check bypass
- Security bug fix: Prevent USB data changes for non-owner users during lockdown mode.
- Fix FGS mode in test
- DO NOT MERGE: [ClipboardService] Check notification setting for given user
- Fix entryadapter usage
- DO NOT MERGE: Enforce suspend restrictions in startOp and noteOp paths
- Remove multi user flag reference
- fix: dismiss autofill string and remove string changes from fill dialog
- fix: long pressing notifications crashing SystemUI
- Update legacy autofill bottomsheet
- fix color of emphasized notification
- Revert "biometrics: Introduce node handling for onPress events"
- feat: Introduce Hide From Microg feature
- SettingsLib: Theme according to our palette
- SystemUI: Theme according to our palette
- Theme system components according to our palette
- Add missing import
- Fix build issues after cherrypick in NMSTest (pt 2)
- Fix build issues after cherrypick in NMSTest
- Revert^2 "Fix build failure in release branch"
- Revert "Fix build failure in release branch"
- Revert "Ignore pinned Windows"
- Fix build failure in release branch
- Allow to install Google signed Android Auto APK
- fix light mode 3 button navigation
- SystemUI: apply light/dark theme to shade header elements
- Don't create dynamic overlay
- SystemUI: Fix QS page indicator position
- Revert^2 "SystemUI: Remove nav bar background in QS customizer"
- SystemUI: Recreate overlays anyway
- SystemUI: Re-evaluate system theme on UI mode change
- SystemUI: Fix QS customizer background color
- SystemUI: Fix QS customizer corner radius
- SystemUI: Remove visibility check in setting QSCarrier color
- SystemUI: BatteryMeterView: Set white tint in darkmode
- SystemUI: QSCustomizer: Fix QS tile reset text color
- SystemUI: Remove qs actions footer background
- SystemUI: Prevent systemui crash when reinflating QS
- SystemUI: Follow light/dark theme in power menu
- SystemUI: Follow light/dark theme in SplitShade Header
- SystemUI: Re-inflate QS and SB when CONFIG_SCREEN_LAYOUT
- SystemUI: Calculate paged QS tiles height properly
- SystemUI: Fix QS header clock color
- SystemUI: Add dual-tone light and dark themes for QS
- SystemUI: Initialize QS tiles in inactive state
- SystemUI: Follow light/dark theme in quick settings
- Revert "Do not re-inflate QS and SB when CONFIG_UI_MODE"
- SystemUI: Make QS panel change on UI mode changes
- UdfpsController: Move HBM enable to dispatchOnUiReady()
- UdfpsController: Move writeToUdfpsNode to background executor
- biometrics: Introduce node handling for onPress events
- biometrics: Skip unconfigureDisplay if mOnFingerDown
- SNHooks: Set Build.TYPE to userdebug for dockmanager
- PhoneStatusBarView: Pad statusbar with Launcher3 dock width
- base: Add minimal support for Richtap vibrations
- Android Auto: Support Android Auto as user app 1/2

### packages/apps/Settings (42 missing on a17)
- Move backup entry to top level settings
- [Settings] Strip URI grant flags in AppRestrictionsFragment
- [RESTRICT AUTOMERGE] Ensure remote device credential alias is used for action CONFIRM_REMOTE_DEVICE_CREDENTIAL.
- Update enable ANGLE warning message
- Revert^2 "[nfc] Fix string injection in default payment app selector"
- Allow to remove tint for homepage icons
- Replace cloudfare with quadnine as dns provider
- Reapply "Add Cloudflare DNS as a private DNS provider"
- Revert "Add Quad9 DNS as a private DNS provider"
- Theme app components according to our palette
- fix security screen in setup wizard being cut in potrait mode of tablet
- Change app icon to our custom icon
- Remove smart cleanup card
- Add license
- Change default highlight key which makes top entries visible in tablet
- Settings: add find my device entry in settings
- Port translations from Android 14
- Settings: sfps-google: Guard Google SFPS extension
- Settings: Add Google's custom sfps resumeEnroll()
- Settings: Add summary for disabled content-based refresh rate
- Settings: Change ping to quad9 dns
- Settings: add parental control changes
- Add a dedicated section in developer options for /e/OS related settings
- Improve wordings for automatic sync
- Update remove account dialog message to make it more clear
- Add Quad9 DNS as a private DNS provider
- Settings: add preference for sentry user id
- Revert "Add Cloudflare DNS as a private DNS provider"
- Settings: Remove google animations and links
- Write telemetry system settings
- Settings: top_level_settings: Move accounts entry to top
- Settings: Remove find my device from security settings summary
- Settings: Remove security settings placeholder
- 697-s-Recalculate_accountType_sorting
- Settings: Change updater summary for /e/OS version
- Settings: Notify users all their accounts will be removed and not just google
- Settings: mark eDrive as safe to be opened by accountManager
- Settings: Integrate Advanced Privacy into settings
- Settings: Switch to select prod or staging OTA server
- Settings: Move updater to top of settings main page
- Settings: Add /e/ legal
- Settings: res: Set proper title for system version

### packages/apps/SetupWizard (33 missing on a17)
- Only skip QR wifi setup when connected to the QR wifi
- Add translations for QR wifi strings
- Allow to connect wifi from QR
- Set language from provision QR
- Use DevicePolicyManager constants in ProvisioningQrParser
- Update restore activity action
- Skip theme, FMD and navigation settings if restore finished
- Revert "Revert setupwizard changes for backup app"
- Revert setupwizard changes for backup app
- Set BlissLauncher as default when moments is installed
- Launch restore when EAccount is available
- Move account setup after date & time
- fix restore intro restore button binding
- Move account check to helper class
- add translations for new strings
- Hide login/create if logged in
- Add restore page for backup app
- feat:4037: set e account setting early, before restore eBackup step
- Added signature-based checksum support.
- Fix welcome layout root id in sw600dp and tv
- Implemented MDM provisioning by QR code
- Theme app according to our palette
- Add license
- Adding the Find my device screen to FTW
- SetupWizard: Skip recovery update option
- Add parental control page
- Port translations from A14
- SetupWizard: Toggle oem unlocking toggle for Pixel 5 only
- SetupWizard: Turn off OEM unlocking during initial setup if bootloader is locked
- Replace lineage strings and logo with /e/
- SetupWizard: Enable wifi location
- SetupWizard: Disable LineageOS metrics
- SetupWizard: Add /e/ account manager page

### vendor/lineage (33 missing on a17)
- Bump security string to 2026-10-01
- version: Bump to /e/OS v4.3.1
- version: Bump to /e/OS v4.3.1
- version: stop accepting the partner release type
- Bump security string to 2026-09
- version: Bump to /e/OS v4.3
- Bump security string to 2026-08
- version: Bump to /e/OS v4.2
- version: Bump to /e/OS v4.1.3
- version: Bump to /e/OS v4.1.2
- version: Bump to /e/OS v4.1.1
- Bump security string to July 2026
- version: Bump to /e/OS v4.1
- Bump security string to 2026-06-01
- Bump security string to 2026-05-01
- Bump security string to 2026-05-01
- version: Bump to /e/OS v4.0
- version: Bump to /e/OS v3.7.1
- version: Bump to /e/OS v3.7.1
- Bump Security string to 2026-04-01
- version: Bump to /e/OS v3.7
- version: Bump to /e/OS v3.6
- Bump to 2026-02-01 security string
- version: Bump to /e/OS v3.5
- version: Bump to /e/OS v3.4
- Bump to 2026-01-01 security string
- Disable private space
- vendor/lineage: Hookup TARGET_USES_MTK_APNS_CONF
- version: Bump to /e/OS v3.3
- vendor: Rename overlays to match BlissLauncher
- Revert settings card layout
- vendor: lineage: remove nfc and fingerprint help url
- vendor/lineage: Hookup TARGET_USES_MTK_APNS_CONF

### frameworks/libs/systemui (25 missing on a17)
- Revert "Reapply "fix: center the badge on its first digit at the icon corner""
- Revert "Reapply "feat: expose the notification dot circle radius""
- Revert "fix: address a16 badge review follow-ups (numToNotation visibility)"
- Revert "fix: make the notification dot's badge/icon ratio density-independent"
- fix: make the notification dot's badge/icon ratio density-independent
- fix: address a16 badge review follow-ups (numToNotation visibility)
- Reapply "feat: expose the notification dot circle radius"
- Reapply "fix: center the badge on its first digit at the icon corner"
- Revert "fix: center the badge on its first digit at the icon corner"
- Revert "feat: expose the notification dot circle radius"
- feat: expose the notification dot circle radius
- fix: center the badge on its first digit at the icon corner
- Add license
- (fix): Render notificationBadges as intended
- fix: Return intended notification count
- fix: Revert badge size and position to pre-tablet [2/2]
- fix: DotRenderer: Tune further for tablet
- fix: Properly handle tablet notification icons [1/2]
- feat: adjust position of dots and add checks
- feat: adjust dot size accordingly
- DotRenderer: Add shadow to notification dots
- feat: convert badge to round rect when count > 99
- feat(icons): Add month icon support for calendar
- feat(dots): notification count support for launcher3 app badges
- bl3: make it buildable

### packages/modules/Permission (13 missing on a17)
- Revert^2 "Ensure Gallery always shows as system fixed"
- Revert "Revert "Display the system gallery storage permission as..."
- Revert "Display the system gallery storage permission as system fixed"
- Revert "Ensure Gallery always shows as system fixed"
- Update RuntimePermissionsUpgradeController to accept null PermGroups
- Revert^2 "Ensure Gallery always shows as system fixed"
- Revert "Revert "Display the system gallery storage permission as..."
- Revert "Display the system gallery storage permission as system fixed"
- Revert "Ensure Gallery always shows as system fixed"
- Theme app according to our palette
- Add license
- PermissionController: Add a role for deviceKeyHandler
- Android Auto: Support Android Auto as user app 2/2

### packages/apps/ThemePicker (5 missing on a17)
- Theme components to match our palette
- ThemePicker: Adjust permission for changed packagename
- Specify we read and write launcher settings
- Add license
- ThemePicker: Remove wallpaper color selection

### packages/modules/DnsResolver (5 missing on a17)
- Add license
- shouldBlockRequest: Don't block if socket connect fails
- DnsResolver: Change socket name
- dnsresolver: Adapt for Unix socket
- dnsresolver: use dns blocker app to filter trackers

### packages/apps/LineageParts (4 missing on a17)
- Revert "LineageParts: Add new PreferenceCategory and RemotePreference for Hardware Switch"
- LineageParts: Add new PreferenceCategory and RemotePreference for Hardware Switch
- feat: rename "microG" into "App compatibility"
- Theme app according to our palette

### packages/modules/Connectivity (4 missing on a17)
- Replace google dns with quadnine dns
- Revert "Add Quad9 DNS as a private DNS provider"
- Add license
- Add Quad9 DNS as a private DNS provider

### packages/apps/WallpaperPicker2 (3 missing on a17)
- Change accent to match ours
- Theme app according to our palette
- Add license

### packages/overlays/Lineage (3 missing on a17)
- overlays: Add circle icon overlay
- overlays: rename overlays for blisslauncher
- Add license

### packages/apps/Contacts (2 missing on a17)
- Issue 1776: Default to phone-only if no account
- 709-s-Open_accountManager_onClick_add_account

### packages/apps/FMRadio (2 missing on a17)
- Update app icon according to new design
- Add license

### packages/apps/SettingsIntelligence (2 missing on a17)
- Theme app according to our pallete
- Add license

### packages/services/Telephony (2 missing on a17)
- Telephony: Use quad9.net for http
- Add license

### vendor/qcom/opensource/commonsys/fm (2 missing on a17)
- Update app icon according to new design
- Add license

### packages/apps/Dialer (1 missing on a17)
- dialer: callrecord: Enable call recording by default with VOICE_CALL as source

### packages/apps/DocumentsUI (1 missing on a17)
- Theme app according to our palette

### system/core (1 missing on a17)
- Spoof yellow verified boot state to green
