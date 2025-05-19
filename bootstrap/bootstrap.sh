#!/usr/bin/env bash

if [[ -z $GCP_PROJECT_ID ]]; then
  echo "Enter Project ID (or export GCP_PROJECT_ID):"
  read -r GCP_PROJECT_ID
fi

export DATA_STORE_NAMESPACE=Alchemyst
export DATA_STORE_PROJECT=${GCP_PROJECT_ID}

pushd "$(dirname "${BASH_SOURCE[0]}")/../" > /dev/null || exit

echo "-> [INFO] Loading JSON into Datastore ..."  

uv sync --locked

uv run python3 ./bootstrap/load_notes.py
uv run python3 ./bootstrap/documents/load_document.py

popd > /dev/null || exit

echo "-> [INFO] Execution complete"
