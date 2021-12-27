#!/bin/sh

# timeout --foreground 300
qemu-system-x86_64 -s \
    -no-reboot \
	-m 64M \
	-kernel bzImage \
	-nographic \
	-append "console=ttyS0 init='/init' acpi=noirq quiet" \
    -initrd initramfs.cpio.gz \
    -net nic \
	-monitor /dev/null

