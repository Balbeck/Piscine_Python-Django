#!/bin/bash

# [ Env ]
cd ..
source django_venv/bin/activate

# [ Nigration ]
python manage.py makemigrations ex09
python manage.py migrate ex09
python manage.py showmigrations ex09
