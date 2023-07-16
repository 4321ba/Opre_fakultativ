#!/bin/sh
for f in tests/input/*
do
./test_one.sh `basename $f`
done
