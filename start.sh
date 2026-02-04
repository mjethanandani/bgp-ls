#!/bin/sh

cd /app/
rm -rf bin
cd draft
make clean
make
