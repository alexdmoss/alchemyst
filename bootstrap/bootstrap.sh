#!/usr/bin/env bash

if [[ -z $GCP_PROJECT_ID ]]; then
  echo "Enter Project ID (or export GCP_PROJECT_ID):"
  read -r GCP_PROJECT_ID
fi

if [[ $(gcloud iam service-accounts list --project="${GCP_PROJECT_ID}" --format="value(display_name)" | grep -c "alchemyst") -eq 0 ]]; then
  gcloud iam service-accounts create alchemyst \
    --display-name=alchemyst \
    --description="Workload Identity access to Datastore" \
    --project="${GCP_PROJECT_ID}"
fi

gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
  --member="serviceAccount:alchemyst@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
  --role=roles/datastore.user >/dev/null 

gcloud iam service-accounts add-iam-policy-binding \
  --project="${GCP_PROJECT_ID}" \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:${GCP_PROJECT_ID}.svc.id.goog[alchemyst/alchemyst]" \
  alchemyst@"${GCP_PROJECT_ID}".iam.gserviceaccount.com > /dev/null

echo "NB: You must also enable Datastore for the project"
