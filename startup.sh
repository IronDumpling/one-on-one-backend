#!/bin/bash

# Install necessary tools
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install --upgrade pip wheel
pip install Django Markdown django-filter djangorestframework djangorestframework-simplejwt api-view

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Deactivate virtual environment
deactivate
