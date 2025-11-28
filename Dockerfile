# dockerfile for the pipeline

FROM python:3.13

WORKDIR /pipeline

COPY /pipline/* .

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
