#! /usr/bin/env zsh

# TODO: /auto/ has moved and paths need updating. Entire /auto/ system is being upgraded. Coming soon!
# All /auto/* scripts must be run from the project root directory.

echo
echo "#############################    BUILD PGADMIN    ##############################"
date
echo "################################################################################"
echo

# Echo all subsequent commands before executing them
set -x

# Option --progress=plain provides more detail during development or troubleshooting.
# Notice we are not using buildx here. We do use buildx for the bedrock build. (Required to get correct img platform.)

docker build --progress=plain -t AWS__USER__ID.dkr.ecr.us-west-2.amazonaws.com/AWS__REPO__NAME:bedrock-pgadmin pgadmin

