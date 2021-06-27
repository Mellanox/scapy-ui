# Scapy UI

A web based Scapy GUI, major features:

- Edit packet and send
- Load/Save packet templates
- Browse packet detail and hex
- Packet sniffer and dump
- Load and browse pcap file

Requirements:

- yum install python3-devel

or

- apt-get install python3-dev

and

- pip3 install --no-cache-dir scapy flexx psutil

Start:

- sudo ./scapy-ui.py --app

Setup a remote server:

- sudo ./scapy-ui.py --flexx-hostname=`hostname` --flexx-port=49190
- http://{hostname}:49190/ScapyUI/

Build and Run From docker support:

- docker build -t scapy-ui .

- docker run -it --rm --network=host scapy-ui:latest


TBD:

- Generate field from Scapy fields descriptors.
- Better/more protocol editor
