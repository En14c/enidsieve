#!/bin/bash

COMMANDLINE_ARGS=("$@")
OPERATION=${COMMANDLINE_ARGS[0]}

function usage {
cat <<usagemessage
+++++++++++++++++++++++++++++
USAGE: ./manage.sh op

op:
  * [kill] kills service's container
  * [run]: runs service's container
  * [restart]: kill service's container then run the container.
  * [build]: build service's container image with latest working dir changes.
  * [deploy]: build service's container image with latest working dir changes and
    runs the service's container.
  * [unittests] run the unittests containr and them purge it.
+++++++++++++++++++++++++++++
usagemessage
}

function run_unit_tests {
   docker run --rm enid-sieve:latest pytest -v
}

function run_service_detached {
  # run container in detached state and publish container's port 80 to host's port 8000.
  docker run --name enidsieve -dp 8000:80 enid-sieve
}

function kill_service {
  docker kill enidsieve; docker container rm enidsieve;
}

function restart_service {
  kill_service
  run_service_detached
}

function purge_dangling_images {
  # after each build, there mightbe some residue from the intermediate containers,
  # that was created by docker during the container image building process, so we purge them
  # to save disk space.
  local DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
  if [ "$DANGLING_IMAGES" ]; then
    docker rmi $DANGLING_IMAGES
  fi
}

function build {
  kill_service
  docker build --force-rm -t enid-sieve .
  purge_dangling_images
}

function deploy {
  build
  run_service_detached
}

function main {
  case $OPERATION in
    kill)
      kill_service
      ;;
    run)
      run_service_detached
      ;;
    build)
      build
      ;;
    restart)
      restart_service
      ;;
    deploy)
      deploy
      ;;
    unittests)
      run_unit_tests
      ;;
    *)
      usage
      ;;
  esac
}

main