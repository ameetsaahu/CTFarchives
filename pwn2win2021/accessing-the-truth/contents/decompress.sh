#!/bin/sh
mkdir -p initramfs
cd initramfs
cpio -vid < ../initramfs.cpio
cd ..
