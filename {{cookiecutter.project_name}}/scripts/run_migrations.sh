#! /bin/bash

export FLASK_APP=src/main.py
flask db init
flask create-sequence autoid
flask db migrate
flask db upgrade
