#!/bin/bash
for file in in/*.out;
do
  echo "handle $file"
  python results-cyg.py $file
done
