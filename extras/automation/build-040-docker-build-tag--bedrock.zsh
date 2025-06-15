#! /usr/bin/env zsh

# TODO: /auto/ has moved and paths need updating. Entire /auto/ system is being upgraded. Coming soon!
# All /auto/* scripts must be run from the project root directory.

echo
echo "#############################    BUILD BEDROCK    ##############################"
date
echo "################################################################################"
echo

# Echo all subsequent commands before executing them
set -x

# Buildx option added (required on WSL) to get multiplatform (Linux) builds. It offers other powerful features.

docker buildx build --platform linux/amd64 -t AWS__USER__ID.dkr.ecr.us-west-2.amazonaws.com/AWS__REPO__NAME:bedrock-bedrock bedrock

