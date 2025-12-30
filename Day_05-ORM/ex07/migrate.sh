#!/bin/bash

# [ Env ]
cd ..
source django_venv/bin/activate

# [ Nigration ]
python manage.py makemigrations ex07
python manage.py migrate ex07
python manage.py showmigrations ex07
