#!/bin/bash
python3 manage.py collectstatic --noinput
python3 manage.py migrate 
gunicorn -w 4 --worker-class=gevent -b 127.0.0.1:5000 fruit_info.wsgi:application