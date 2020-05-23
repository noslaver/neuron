FROM python:3-slim

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY neuron /app/neuron

ENTRYPOINT python -m neuron.server run-server ${MSGQUEUE_URL}
