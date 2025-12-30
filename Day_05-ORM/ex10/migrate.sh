#!/bin/bash

# [ Env ]
cd ..
source django_venv/bin/activate

# [ Nigration ]
python manage.py makemigrations ex10
python manage.py migrate ex10
python manage.py showmigrations ex10
