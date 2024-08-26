#!/bin/bash

source /home/amuni/my_applications/fruit-info-ai/venv/bin/activate

celery -A fruit_info worker -l INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo