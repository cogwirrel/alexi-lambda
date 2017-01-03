#!/bin/bash

mkdir -p output
rm output/lambda_code.zip
chmod 777 src/*.py
pushd src
zip -r ../output/lambda_code.zip *
popd