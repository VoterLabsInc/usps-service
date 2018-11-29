#! /bin/bash

# pip has a max path length of 126 characters which causes an issue with
# Jenkins whose paths are very long. To solve it, we store the virtual env
# in a temp directory instead.
rm -rf ~/temp
mkdir -p ~/temp
TEMP_DIR=$(mktemp -d -p ~/temp/)
echo $TEMP_DIR > ~/temp/.venv
virtualenv -p python3 $TEMP_DIR
source $TEMP_DIR/bin/activate
pip install -r test_requirements.txt
