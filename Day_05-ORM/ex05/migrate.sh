#!/bin/bash

# [ Env ]
cd ..
source django_venv/bin/activate

# [ Nigration ]
python manage.py makemigrations ex05
python manage.py migrate ex05
python manage.py showmigrations ex05
