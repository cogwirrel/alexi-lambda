#!/bin/bash

echo "Deleting output"
rm -rf output/*

echo "Deleting libraries"
pushd src/lib
find . -maxdepth 1 -not -name 'setup.cfg' -not -name '.' -print0 | xargs -0 rm -rf
popd
