#! /usr/bin/env zsh

# TODO: /auto/ has moved and paths need updating. Entire /auto/ system is being upgraded. Coming soon!
# All /auto/* scripts must be run from the project root directory.

echo
echo "#############################    BUILD POSTGRES    #############################"
date
echo "################################################################################"
echo

# Echo all subsequent commands before executing them
set -x

echo "Adding group write permission to the dbvolume directory so Postgress can create /dbvolume/data structure."
echo "This requirement seems to have appeared when using this Postgres image on WSL Linux."
# TODO: UPDATE: This looks to no longer be required. Check again. The newer image we use now may have fixed the issue.

ls -alt ./dbvolume

# This equates to 777 permissiosn. Not ideal, but especially on Windows WSL; realistically it is hard to avoid.
chmod go+w ./dbvolume

ls -alt ./dbvolume

# Option --progress=plain provides more detail during development or troubleshooting.
# Notice we are not using buildx here.
# We do use buildx for the bedrock build. (Required to get an image for the correct (Linux) platform for that build.)

docker build --progress=plain -t AWS__USER__ID.dkr.ecr.us-west-2.amazonaws.com/AWS__REPO__NAME:bedrock-postgres postgres

