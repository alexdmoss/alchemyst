#!/usr/bin/env bash
set -Eeuo pipefail

if [[ -z "${GCP_PROJECT_ID}" ]]; then
  echo "-> [ERROR] You must export GCP_PROJECT_ID"
  exit 1
fi

function run() {

  export DATA_STORE_NAMESPACE=Alchemyst
  export DATA_STORE_PROJECT=${GCP_PROJECT_ID}
  export FLASK_APP=alchemyst
  export FLASK_DEBUG=1
  export USE_MOCKS=False

  pipenv run flask run

}

function run-wsgi() {

  pushd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null

  export DATA_STORE_NAMESPACE=Alchemyst
  export DATA_STORE_PROJECT=${GCP_PROJECT_ID}
  export FLASK_APP=alchemyst
  ### Needed if we go above 1 worker - see README
  # export prometheus_multiproc_dir=/tmp
  # export METRICS_PORT=9120

  pipenv run gunicorn --log-config=logging.conf --config=gunicorn_config.py alchemyst:app

}

if [[ "${1:-}" == "--wsgi" ]]; then
  run_wsgi "${@:-}"
else
  run "${@:-}"
fi
