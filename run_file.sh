#!/bin/sh

python3 profile_pic.py
python3 manage.py runserver 0.0.0.0:8045
cd mark_attendance
go run *.go