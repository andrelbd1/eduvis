# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8.3-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt --no-cache-dir

CMD python run.py