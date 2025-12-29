#!/bin/bash

# [ Env ]
cd ..
python3 -m venv django_venv
source django_venv/bin/activate
pip install --upgrade pip
pip install -r requirement.txt

# [ Nigration ]
python manage.py makemigrations ex05
python manage.py migrate ex05
python manage.py showmigrations ex05
