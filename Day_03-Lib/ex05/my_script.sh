#!/bin/bash

# Create and activate Venv
python3 -m venv django_venv
source django_venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirement.txt

# Launch the Django server
cd Hello_World
python manage.py runserver
