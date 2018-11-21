#! /bin/bash

rm -rf ~/temp
mkdir -p ~/temp
TEMP_DIR=$(mktemp -d -p ~/temp/)
echo $TEMP_DIR > ~/temp/.venv
virtualenv -p python3 $TEMP_DIR
source $TEMP_DIR/bin/activate
pip install -r requirements.txt
