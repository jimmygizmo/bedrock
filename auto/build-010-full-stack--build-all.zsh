#! /usr/bin/env zsh

# All /auto/* scripts must be run from the project root directory.

echo
echo "###############################    BUILD ALL    ################################"
date
echo "################################################################################"
echo

# Echo all subsequent commands before executing them
set -x

# Build the postgres container.
./auto/build-020-docker-build-tag--postgres.zsh

# Build the pgadmin container.
./auto/build-030-docker-build-tag--pgadmin.zsh

# Build the Bedrock FastAPI container.
./auto/build-040-docker-build-tag--bedrock.zsh

