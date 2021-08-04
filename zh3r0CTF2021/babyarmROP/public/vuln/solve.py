#!/usr/bin/env python3

from pwn import *

exe = ELF("vuln")
libc = ELF("./lib/libc.so.6")
ld = ELF("./lib/ld-linux-aarch64.so.1")

context.binary = exe


def conn():
    if args.LOCAL:
        return process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})
    else:
        return remote("addr", 1337)


def main():
    r = conn()

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
