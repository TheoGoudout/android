#!/usr/bin/env bash
# Runs ON THE CRAVE BUILD NODE (sent by build.sh through `crave run`).
# Reproduces the essential steps of /e/OS's docker builder (build-community.sh)
# for one device, without docker: re-init to the /e/OS manifest, sync,
# build target-files + otatools, sign with test keys, make the OTA zip and
# a fastboot image zip.
set -eo pipefail

EOS_BRANCH="${EOS_BRANCH:-a16}"            # /e/OS manifest branch or tag: a16 (LOS 23.0) or a17 (LOS 24.0)
DEVICE="${DEVICE:-FP4}"
BUILD_TYPE="${BUILD_TYPE:-userdebug}"
LMANIFEST_URL="${LMANIFEST_URL:?set LMANIFEST_URL to your public local_manifests repo}"
LMANIFEST_BRANCH="${LMANIFEST_BRANCH:-$EOS_BRANCH}"
RELEASE_TYPE="${RELEASE_TYPE:-UNOFFICIAL}"

echo ">> Re-initialising workspace on the /e/OS manifest (${EOS_BRANCH})"
rm -rf .repo/local_manifests
repo init -u https://gitlab.e.foundation/e/os/android.git -b "${EOS_BRANCH}" \
  --git-lfs --depth=1 -g "all,-darwin,-muppets,muppets_${DEVICE}"
tmp_lm="$(mktemp -d)"
git clone --depth 1 -b "${LMANIFEST_BRANCH}" "${LMANIFEST_URL}" "$tmp_lm"
mkdir -p .repo/local_manifests
cp "$tmp_lm/local_manifests/${EOS_BRANCH}/"*.xml .repo/local_manifests/
rm -rf "$tmp_lm"

# Undo the in-tree edit made below on the previous run so repo can update the project
# (the /e/OS builder does the same for vendor/lineage before every sync)
if [ -e vendor/lineage/.git ]; then git -C vendor/lineage reset -q --hard; fi

echo ">> Syncing (crave's resync script handles conflicts left by the base project)"
/opt/crave/resync.sh
repo forall -c 'git lfs pull' >/dev/null 2>&1 || echo ">> WARNING: some git-lfs pulls failed (A16 has one known broken, non-critical LFS object)"

# Same tweaks the /e/OS builder applies
export RELEASE_TYPE="${RELEASE_TYPE,,}"
sed -i "/\$(filter .*\$(LINEAGE_BUILDTYPE)/,+2d" vendor/lineage/config/common.mk || true
export BUILD_USERNAME="${BUILD_USERNAME:-eos-builder}"
export BUILD_HOSTNAME=crave
# vendor/eos only adds ih8sn when RELEASE_TYPE is community/official (INCLUDE_IH8SN ?= ...),
# so pass it explicitly for this UNOFFICIAL build. It is read from the environment like RELEASE_TYPE.
export INCLUDE_IH8SN="${INCLUDE_IH8SN:-true}"

set +e   # envsetup/breakfast are not written for errexit
source build/envsetup.sh
breakfast "${DEVICE}" "${BUILD_TYPE}" || { echo ">> breakfast failed"; exit 1; }
set -e

# Incremental by default: crave keeps out/ between runs. NEVER `make clean` here
# (crave rule, and it turns a ~30 min rebuild into a multi-hour one).
make installclean
mka target-files-package otatools

BUILD_NUMBER="$(date -u +%Y%m%d)"
TF_IN="$(find "$OUT/obj/PACKAGING/target_files_intermediates/" -name '*-target_files*.zip' -print -quit)"
[ -n "$TF_IN" ] || { echo ">> target-files zip not found"; exit 1; }
TF_SIGNED="$OUT/signed-target_files-${BUILD_NUMBER}.zip"
OTA_ZIP="$OUT/e-${EOS_BRANCH}-${BUILD_NUMBER}-${RELEASE_TYPE}-${DEVICE}.zip"
IMG_ZIP="$OUT/IMG-e-${EOS_BRANCH}-${BUILD_NUMBER}-${RELEASE_TYPE}-${DEVICE}.zip"
rm -f "$OUT"/signed-target_files-*.zip "$OUT"/e-*.zip "$OUT"/IMG-e-*.zip

echo ">> Signing with test keys (as the /e/OS community builder does when SIGN_BUILDS=false)"
sign_target_files_apks -t "+test-keys,-release-keys" "$TF_IN" "$TF_SIGNED"
ota_from_target_files "$TF_SIGNED" "$OTA_ZIP"
img_from_target_files "$TF_SIGNED" "$IMG_ZIP"
rm -f "$TF_SIGNED"

# Fixed-name hard links so `crave pull` needs no globs
ln -f "$OTA_ZIP" "$OUT/eos-latest-ota.zip"
ln -f "$IMG_ZIP" "$OUT/eos-latest-img.zip"
( cd "$OUT" && sha256sum eos-latest-ota.zip eos-latest-img.zip "$(basename "$OTA_ZIP")" "$(basename "$IMG_ZIP")" > SHA256SUMS )
echo ">> Done:"
ls -lh "$OTA_ZIP" "$IMG_ZIP" "$OUT/SHA256SUMS"
