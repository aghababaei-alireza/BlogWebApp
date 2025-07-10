FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     libjpeg-dev \
#     zlib1g-dev \
#     && pip install --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ./core .