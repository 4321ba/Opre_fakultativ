#!/bin/sh
./mfq.py < tests/input/$1 | diff -s tests/expected/$1 -
