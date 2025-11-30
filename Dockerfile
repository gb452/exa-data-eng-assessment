# dockerfile for the pipeline

FROM python:3.13

WORKDIR /

COPY pipeline /pipeline

COPY requirements.txt /pipeline/requirements.txt

RUN pip install --no-cache-dir -r /pipeline/requirements.txt

WORKDIR /pipeline

CMD ["python", "-u", "start.py"]