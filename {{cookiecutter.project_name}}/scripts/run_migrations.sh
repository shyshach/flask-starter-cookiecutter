#! /bin/bash

export FLASK_APP=src/main.py
flask db init
flask db migrate
flask db upgrade
