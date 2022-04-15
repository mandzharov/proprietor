FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/proprietor

COPY ./ .
RUN pip install --upgrade pip && pip install -r requirements.txt
