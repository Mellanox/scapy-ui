# scapy-ui
Scapy UI

A web based Scapy GUI, major features:

- Edit packet and send
- Load/Save packet templates
- Browse packet detail and hex
- Packet sniffer and dump
- Load and browse pcap file

Requirements:

- pip3 install scapy flex psutil

Start:

- sudo -H ./scapy-ui.py --app

# to setup a remote server:
- sudo -H ./scapy-ui.py --flexx-host=<host> --flexx-port=8080
- http://<host>:8080/ScapyUI/

TBD:

- Generate field from Scapy fields descriptors.
- Better/more protocol editor
