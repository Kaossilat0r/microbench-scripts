#!/bin/bash
for file in $1/*.out;
do
  echo "handle $file"
  python results-cyg.py $file
done
