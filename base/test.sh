#!/bin/bash

set -o nounset
set -o errexit
set -o xtrace

TARGET="example-project"

# cd to same folder of script: https://stackoverflow.com/a/16349776/194586
cd "${0%/*}"

# cleanup from past runs
rm -rf "$TARGET"

# stamp out cookie cutter with no deps other than docker
make stockstamp

[ -d "$TARGET" ]

pushd "$TARGET"

# NOTE: this makefile is now the one from the project
make black-depfree

make test
