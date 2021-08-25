#! /bin/sh

git clone https://github.com/WebKit/WebKit.git --depth=1
cd WebKit
patch -p1 < dfg.patch
Tools/Scripts/build-webkit --jsc-only --debug
cd WebKitBuild/Debug/bin

./jsc --useConcurrentJIT=false