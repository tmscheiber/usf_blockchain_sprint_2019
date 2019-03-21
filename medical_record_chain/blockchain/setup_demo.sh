#!/bin/sh

export FLASK_APP="medical_record_chain.py"
export APP_SETTINGS="demo"
export SECRET="dev_secret"
export DATABASE_URL="postgresql://localhost:5232/medical_record_db"