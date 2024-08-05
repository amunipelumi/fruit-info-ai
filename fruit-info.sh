#!/bin/bash
# activate environment
source /home/amuni/my_applications/fruit-info-ai/venv/bin/activate
# collect static
python3 manage.py collectstatic --noinput
# migrate just in case
python3 manage.py migrate 
# run gunicorn command
gunicorn -w 4 --worker-class=gevent -b 127.0.0.1:5000 fruit_info.wsgi:application