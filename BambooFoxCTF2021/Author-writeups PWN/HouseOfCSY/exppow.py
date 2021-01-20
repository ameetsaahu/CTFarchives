#!/usr/bin/env python3
import hashlib
import sys



def solve_pow(prefix, difficulty):
    #prefix = sys.argv[1]
    #difficulty = int(sys.argv[2])
    print("[pow solver] prefix: "+prefix)
    print("[pow solver] difficulty: "+str(difficulty))
    zeros = '0' * difficulty

    def is_valid(digest):
        if sys.version_info.major == 2:
            digest = [ord(i) for i in digest]
        bits = ''.join(bin(i)[2:].zfill(8) for i in digest)
        return bits[:difficulty] == zeros
    i = 0
    while True:
        i += 1
        s = prefix + str(i)
        if is_valid(hashlib.sha256(s.encode()).digest()):
            return i
            exit(0)