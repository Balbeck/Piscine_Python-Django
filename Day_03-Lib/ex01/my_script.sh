#!/bin/bash

python3 -m venv local_lib/
source ./local_lib/bin/activate

# python3 -m pip install --log path.log --upgrade --force-reinstall  git+https://github.com/jaraco/path.py.git

python3 -m pip install --upgrade pip
python3 -m pip install --log path_install.log --upgrade --force-reinstall path.py

# $? code retour de last commande (0 succes)
if [ $? -eq 0 ]; then
    echo "Installation successful!"
    python3 -m pip --version
    python3 my_program.py
else
    echo "Installation failed. Check install.log for details."
    exit 1
fi

deactivate
