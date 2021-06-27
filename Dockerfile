FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y procps

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python scapy-ui.py --flexx-hostname=$(hostname -I | cut -d' ' -f1) --flexx-port=49190