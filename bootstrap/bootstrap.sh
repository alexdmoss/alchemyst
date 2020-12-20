#!/usr/bin/env bash

if [[ -z $GCP_PROJECT_ID ]]; then
  echo "Enter Project ID (or export GCP_PROJECT_ID):"
  read -r GCP_PROJECT_ID
fi

gcloud iam service-accounts create alchemyst \
  --display-name=alchemyst \
  --description="Workload Identity access to Datastore" \
  --project=${GCP_PROJECT_ID}

gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
  --member="serviceAccount:alchemyst@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
  --role=roles/datastore.user
  
gcloud iam service-accounts add-iam-policy-binding \
  --project=${GCP_PROJECT_ID} \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:${GCP_PROJECT_ID}.svc.id.goog[alchemyst/alchemyst]" \
  alchemyst@${GCP_PROJECT_ID}.iam.gserviceaccount.com
