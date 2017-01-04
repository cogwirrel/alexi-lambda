#!/bin/bash

# Install dependencies if we haven't already
if [ -e src/lib/.installed ]; then
    echo "Already installed dependencies."
else
    pushd src/lib

    # List dependencies here as pip commands!
    pip install arrow -t .

    touch .installed

    popd
fi

mkdir -p output
rm output/lambda_code.zip
chmod 777 src/*.py
pushd src
zip -r ../output/lambda_code.zip *
popd