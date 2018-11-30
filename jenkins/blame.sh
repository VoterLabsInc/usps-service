#!/bin/bash
# Find the author of the currently checkout branch / commit and
# echos their slack tag so they can be shamed.
AUTHOR=$(git --no-pager show -s --format='%an <%ae>')
if [[ "$AUTHOR" == *"Joseph Collard"*  ]]; then
  echo "@josephmcollard"
  exit 0
fi

if [[ "$AUTHOR" == *"harri25j"* ]]; then
  echo "@harri25j"
  exit 0
fi

if [[ "$AUTHOR" == *"necarlson97"* ]]; then
  echo "@nilscarlson1997"
  exit 0
fi

if [[ "$AUTHOR" == *"Tom"* ]]; then
  echo "@tmlrnc"
  exit 0
fi

echo "$AUTHOR"