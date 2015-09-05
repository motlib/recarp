#!/bin/bash

VENV_DIR=venv

# create a 
if [ ! -d ./${VENV_DIR} ]
then
    virtualenv -p python3 ${VENV_DIR}
fi

. ./${VENV_DIR}/bin/activate

pip install -r requirements.txt
