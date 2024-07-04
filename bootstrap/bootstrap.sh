#!/usr/bin/env bash

if [[ -z $GCP_PROJECT_ID ]]; then
  echo "Enter Project ID (or export GCP_PROJECT_ID) where this app runs:"
  read -r GCP_PROJECT_ID
fi

if [[ -z $CI_PROJECT_ID ]]; then
  echo "Enter CI Project ID (or export CI _PROJECT_ID) where GCP SA lives:"
  read -r CI_PROJECT_ID
fi

if [[ $(gcloud iam service-accounts list --project="${GCP_PROJECT_ID}" --format="value(display_name)" | grep -c "alchemyst") -eq 0 ]]; then
  gcloud iam service-accounts create alchemyst \
    --display-name=alchemyst \
    --description="Runtime account for alchemyst.co.uk" \
    --project="${GCP_PROJECT_ID}"
fi

gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
  --member="serviceAccount:alchemyst@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
  --role=roles/datastore.user >/dev/null 

# Grant the serviceAccount.actAs permission to the runtime service account
gcloud iam service-accounts add-iam-policy-binding "alchemyst@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --member="serviceAccount:app-ci@$CI_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser" \
  --project="$GCP_PROJECT_ID"

echo "NB: You must also enable Datastore for the project"
