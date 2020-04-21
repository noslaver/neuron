FROM python:3-slim

COPY neuron /app/neuron
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT python -m neuron.server run-server ${MSGQUEUE_URL}
