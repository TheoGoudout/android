#!/usr/bin/env bash
# Runs on YOUR machine (any weak laptop is fine: it only talks to crave.io).
# First run:  ./build.sh setup     (once: creates the persistent workspace)
# Each build: ./build.sh build     (queues the build, streams the log)
#             ./build.sh pull      (downloads OTA zip + fastboot IMG zip)
set -eo pipefail

# ---- edit these -------------------------------------------------------------
LMANIFEST_URL="https://github.com/CHANGE_ME/eos_fp4_local_manifests"
# Pick ONE target:
#   a16 = real /e/OS 4.x on LineageOS 23.0 (Android 16) - what /e/OS ships for FP4 today
#   a17 = /e/OS on LineageOS 24.0 (Android 17) - /e/OS's work-in-progress port
# (a16.2 also exists but most of its forks are plain LineageOS 23.2 without /e/OS changes)
EOS_BRANCH="a16"
LMANIFEST_BRANCH="$EOS_BRANCH"  # branch of your local_manifests repo holding local_manifests/<branch>/eos_fp4.xml
DEVICE="FP4"
BUILD_TYPE="userdebug"
INCLUDE_IH8SN="true"        # /e/OS's prop-masking helper; only auto-enabled for community/official builds
# crave base project "LineageOS 23.2" (ID used by sounddrill31/crave_aosp_builder): an
# Android 16 base, valid for a16. For a17 ask crave (discord) for the LineageOS 24 project ID:
# crave's rules say to sync a ROM only on a base project of the same Android version.
# Keep the folder name stable: crave keys the persistent source+out/ on it.
PROJECT_ID="99"
WORKSPACE="/crave-devspaces/Lineage23"
# -----------------------------------------------------------------------------

HERE="$(cd "$(dirname "$0")" && pwd)"
command -v crave >/dev/null || { echo "Install crave first: curl -s https://raw.githubusercontent.com/accupara/crave/master/get_crave.sh | bash -s --"; exit 1; }

case "${1:-}" in
  setup)
    # Inside `crave devspace` (recommended) this creates a clone of the pre-synced LOS 23.2 tree.
    crave clone create --projectID "$PROJECT_ID" "$WORKSPACE"
    mkdir -p "$WORKSPACE/.repo/manifests"
    cp "$HERE/crave.yaml" "$WORKSPACE/.repo/manifests/crave.yaml"
    echo "Workspace ready at $WORKSPACE"
    ;;
  build)
    cd "$WORKSPACE"
    payload="$(base64 -w0 "$HERE/remote-build.sh")"
    # One build at a time per account (crave rule). Add --clean ONLY if the tree is truly broken.
    crave run --no-patch -- "echo $payload | base64 -d > /tmp/eos-remote-build.sh && \
      EOS_BRANCH='$EOS_BRANCH' DEVICE='$DEVICE' BUILD_TYPE='$BUILD_TYPE' INCLUDE_IH8SN='$INCLUDE_IH8SN' \
      LMANIFEST_URL='$LMANIFEST_URL' LMANIFEST_BRANCH='$LMANIFEST_BRANCH' \
      bash /tmp/eos-remote-build.sh"
    ;;
  pull)
    cd "$WORKSPACE"
    for f in eos-latest-ota.zip eos-latest-img.zip SHA256SUMS; do crave pull "out/target/product/$DEVICE/$f"; done
    echo "Downloaded into $WORKSPACE (check SHA256SUMS before flashing)"
    ;;
  log)
    cd "$WORKSPACE"; crave pull out/error.log && cat out/error.log
    ;;
  *)
    echo "usage: $0 {setup|build|pull|log}"; exit 1 ;;
esac
