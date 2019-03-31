#!/bin/sh

export FLASK_APP="manage.py"
export APP_SETTINGS="development"
export SECRET="dev_secret"
export DATABASE_URL="postgresql://quincy:Quincy1000@localhost:5432/medical_record_db"
