#! /usr/bin/env zsh

# All /auto/* scripts must be run from the project root directory.

# This script is a convenient shortcut for building the full stack of images from source.

echo
echo "################################    BUILD ALL    ###############################"
date
echo "################################################################################"
echo

# Echo all subsequent commands before executing them
set -x

# Run the full sequence of build steps, one container at a time.
./auto/build-010-full-stack--build-all.zsh

