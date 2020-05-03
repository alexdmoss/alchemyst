#!/usr/bin/env bash
set -Eeuo pipefail

if [[ -z ${IMAGE_NAME:-} ]]; then
  IMAGE_NAME=alchemyst
fi 

SRC_DIR=alchemyst

function help() {
  echo -e "Usage: go <command>"
  echo -e
  echo -e "    help                 Print this help"
  echo -e "    run                  Run locally from source"
  echo -e "    test                 Run local unit tests and linting"
  echo -e "    deploy               Deploys app to Kubernetes. Designed to run in Drone CI"
  echo -e "    load-data            Load full dataset (upserts)"
  echo -e 
  exit 1
}

function run() {

  _console_msg "Running python:main ..." INFO true

  pushd "$(dirname $BASH_SOURCE[0])" > /dev/null

  export DATA_STORE_NAMESPACE=Alchemyst
  export DATA_STORE_PROJECT=moss-work
  export FLASK_APP=alchemyst
  export FLASK_DEBUG=0
  export USE_MOCKS=False

  pipenv run flask run

  popd > /dev/null
  
  _console_msg "Execution complete" INFO true

}

function run-wsgi() {

  _console_msg "Running python:main ..." INFO true

  pushd "$(dirname $BASH_SOURCE[0])" > /dev/null

  export DATA_STORE_NAMESPACE=Alchemyst
  export DATA_STORE_PROJECT=moss-work
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

  pushd "$(dirname $BASH_SOURCE[0])" > /dev/null

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

function deploy() {

  _assert_variables_set GCP_PROJECT_ID NAMESPACE

  pushd $(dirname $BASH_SOURCE[0])/k8s/ >/dev/null

  if [[ ${DRONE:-} == "true" ]]; then
    _assert_variables_set K8S_DEPLOYER_CREDS K8S_CLUSTER_NAME
    _console_msg "-> Authenticating with GCloud"
    echo "${K8S_DEPLOYER_CREDS}" | gcloud auth activate-service-account --key-file -
    region=$(gcloud container clusters list --project=${GCP_PROJECT_ID} --filter "NAME=${K8S_CLUSTER_NAME}" --format "value(zone)")
    _console_msg "-> Authenticating to cluster ${K8S_CLUSTER_NAME} in project ${GCP_PROJECT_ID} in ${region}"
    gcloud container clusters get-credentials ${K8S_CLUSTER_NAME} --project=${GCP_PROJECT_ID} --region=${region}
  fi

  _console_msg "Applying Kubernetes yaml"

  kustomize edit set image alchemyst=eu.gcr.io/${GCP_PROJECT_ID}/alchemyst:${DRONE_COMMIT_SHA}
  
  kustomize build . | kubectl apply -f -

  kubectl rollout status deploy/alchemyst -w -n ${NAMESPACE}

  popd >/dev/null

}

function load-data() {

  _console_msg "Running python:load_data ..." INFO true

  pushd "$(dirname $BASH_SOURCE[0])" > /dev/null

  export DATA_STORE_NAMESPACE=Alchemyst
  export DATA_STORE_PROJECT=moss-work

  _console_msg "Converting exported CSV to JSON ..."

  pipenv run python3 ./data_loader/convert_pdf_csv_to_json.py

  _console_msg "Loading JSON into Datastore ..."
  
  pipenv run python3 ./data_loader/load_data.py

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
    if [ ! -z ${PID:-} ]; then
        kill ${PID}
    fi
    exit 1
}

trap ctrl_c INT

if [[ ${1:-} =~ ^(help|run|run-wsgi|test|deploy|load-data)$ ]]; then
  COMMAND=${1}
  shift
  $COMMAND "$@"
else
  help
  exit 1
fi
