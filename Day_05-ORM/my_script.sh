#!/bin/bash

#launch postgresql Docker container
docker-compose up -d

# Create and activate Venv
python3 -m venv django_venv
source django_venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirement.txt

# Launch the Django server
python3 manage.py runserver
