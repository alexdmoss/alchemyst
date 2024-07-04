#!/usr/bin/env bash
set -euoE pipefail

pushd "$(dirname "${BASH_SOURCE[0]}")/../terraform/" >/dev/null

terraform init -backend-config=bucket="${GCP_PROJECT_ID}"-apps-tfstate -backend-config=prefix="${APP_NAME}"

if [[ ${CI_SERVER:-} == "yes" ]]; then
    action="apply -auto-approve"
    FRONTEND_IMAGE_TAG=${FRONTEND_IMAGE_NAME}:${CI_COMMIT_SHA}-$(echo "${CI_COMMIT_TIMESTAMP}" | sed 's/[:+]/./g')
    BACKEND_IMAGE_TAG=${BACKEND_IMAGE_NAME}:${CI_COMMIT_SHA}-$(echo "${CI_COMMIT_TIMESTAMP}" | sed 's/[:+]/./g')
else
    action="plan"
    FRONTEND_IMAGE_TAG=${FRONTEND_IMAGE_NAME}:latest
    BACKEND_IMAGE_TAG=${BACKEND_IMAGE_NAME}:latest
fi

set -x
terraform ${action} \
    -var gcp_project_id="${GCP_PROJECT_ID}" \
    -var region="${REGION}" \
    -var domain="${DOMAIN}" \
    -var app_name="${APP_NAME}" \
    -var frontend_image_tag="${FRONTEND_IMAGE_TAG}" \
    -var frontend_port="${FRONTEND_PORT}" \
    -var backend_image_tag="${BACKEND_IMAGE_TAG}" \
    -var backend_port="${BACKEND_PORT}" \

popd >/dev/null
