#!/usr/bin/env bash
set -Eeuo pipefail

if [[ -z ${IMAGE_NAME:-} ]]; then
  IMAGE_NAME=alchemyst
fi 


function help() {
  echo -e "Usage: go <command>"
  echo -e
  echo -e "    help                 Print this help"
  echo -e "    run                  Run locally from source"
  echo -e "    test                 Run local unit tests and linting"
  echo -e "    deploy               Deploys app to Kubernetes. Designed to run in Drone CI"
  echo -e "    bootstrap            Sets up accounts and loads full dataset (upserts)"
  echo -e 
  exit 1
}

function run() {

  _console_msg "Running python:main ..." INFO true

  _assert_variables_set GCP_PROJECT_ID

  pushd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null

  export DATA_STORE_NAMESPACE=Alchemyst
  export DATA_STORE_PROJECT=${GCP_PROJECT_ID}
  export FLASK_APP=alchemyst
  export FLASK_DEBUG=1
  export USE_MOCKS=False

  pipenv run flask run

  popd > /dev/null
  
  _console_msg "Execution complete" INFO true

}

function run-wsgi() {

  _assert_variables_set GCP_PROJECT_ID

  _console_msg "Running python:main ..." INFO true

  pushd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null

  export DATA_STORE_NAMESPACE=Alchemyst
  export DATA_STORE_PROJECT=${GCP_PROJECT_ID}
  export FLASK_APP=alchemyst
  ### Needed if we go above 1 worker - see README
  # export prometheus_multiproc_dir=/tmp
  # export METRICS_PORT=9120

  pipenv run gunicorn --log-config=logging.conf --config=gunicorn_config.py alchemyst:app

  popd > /dev/null
  
  _console_msg "Execution complete" INFO true

}


# NB: Dockerfile also runs these, so do not need to use in CI
function test() {

  pushd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null

  if [[ ${CI_JOB_TOKEN:-} != "" ]]; then
    pip install pipenv==2018.10.13
  fi

  pipenv install --dev

  _console_msg "Running flake8 ..." INFO true

  pipenv run flake8 .

  _console_msg "Running unit tests ..." INFO true
  
  pipenv run pytest -s -v
  
  _console_msg "Tests complete" INFO true

  popd > /dev/null

}


function deploy-frontend() {

  _assert_variables_set IMAGE_NAME

  pushd "$(dirname "${BASH_SOURCE[0]}")"/k8s/ >/dev/null

  _console_msg "Applying Kubernetes yaml"

  kustomize build base/ | envsubst "\$GCP_PROJECT_ID" | kubectl apply -f -
  
  cd frontend/
  kustomize edit set image alchemyst-frontend="${IMAGE_NAME}"
  kustomize build . | envsubst "\$GCP_PROJECT_ID" | kubectl apply -f -

  kubectl rollout status deploy/alchemyst-frontend -w -n alchemyst --timeout=120s

  popd >/dev/null

}

function deploy-backend() {

  _assert_variables_set IMAGE_NAME

  pushd "$(dirname "${BASH_SOURCE[0]}")"/k8s/ >/dev/null

  _console_msg "Applying Kubernetes yaml"

  kustomize build base/ | envsubst "\$GCP_PROJECT_ID" | kubectl apply -f -
  
  cd backend/
  kustomize edit set image alchemyst-backend="${IMAGE_NAME}"
  kustomize build . | envsubst "\$GCP_PROJECT_ID" | kubectl apply -f -

  kubectl rollout status deploy/alchemyst-backend -w -n alchemyst --timeout=60s

  popd >/dev/null

}

function bootstrap() {

  _assert_variables_set GCP_PROJECT_ID


  pushd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null

  export DATA_STORE_NAMESPACE=Alchemyst
  export DATA_STORE_PROJECT=${GCP_PROJECT_ID}

  _console_msg "Setting up permissions ..."
  ./bootstrap/bootstrap.sh

  _console_msg "Loading JSON into Datastore ..."  

  pipenv install --dev

  pipenv run python3 ./bootstrap/load_notes.py
  pipenv run python3 ./bootstrap/documents/load_document.py

  popd > /dev/null
  
  _console_msg "Execution complete" INFO true

}

function _assert_variables_set() {

  local error=0
  local varname
  
  for varname in "$@"; do
    if [[ -z "${!varname-}" ]]; then
      echo "${varname} must be set" >&2
      error=1
    fi
  done
  
  if [[ ${error} = 1 ]]; then
    exit 1
  fi

}

function _console_msg() {

  local msg=${1}
  local level=${2:-}
  local ts=${3:-}

  if [[ -z ${level} ]]; then level=INFO; fi
  if [[ -n ${ts} ]]; then ts=" [$(date +"%Y-%m-%d %H:%M")]"; fi

  echo ""

  if [[ ${level} == "ERROR" ]] || [[ ${level} == "CRIT" ]] || [[ ${level} == "FATAL" ]]; then
    (echo 2>&1)
    (echo >&2 "-> [${level}]${ts} ${msg}")
  else 
    (echo "-> [${level}]${ts} ${msg}")
  fi

  echo ""

}

function ctrl_c() {
    if [ -n "${PID:-}" ]; then
        kill "${PID}"
    fi
    exit 1
}

trap ctrl_c INT

if [[ ${1:-} =~ ^(help|run|run-wsgi|test|deploy-frontend|deploy-backend|bootstrap)$ ]]; then
  COMMAND=${1}
  shift
  $COMMAND "$@"
else
  help
fi
