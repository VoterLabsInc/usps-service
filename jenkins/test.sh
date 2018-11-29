#! /bin/bash

TEMP_DIR=$(cat ~/temp/.venv)
source $TEMP_DIR/bin/activate
python -m nose ./test