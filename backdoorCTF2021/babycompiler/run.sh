#!/bin/bash

export PATH=$PWD/kaitai-struct-compiler-0.10-SNAPSHOT/bin:$PATH

TMPDIR=$(mktemp -d)

cp run.py "${TMPDIR}/"

pushd "${TMPDIR}"

echo "Give link to your YAML"

read -r url

wget "$url" -O ./sample.ksy

kaitai-struct-compiler --ksc-exceptions -t python ./sample.ksy

echo "Give link to your file for Kaitai to parse"

read -r f

wget "$f" -O ./f

python3 run.py f

popd

rm -rf "${TMPDIR}"

