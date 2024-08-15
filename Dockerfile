FROM python:3.10.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /fruit-info-ai

RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt-get install -y net-tools


COPY requirements.txt ./

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

COPY . ./
