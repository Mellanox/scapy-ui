# scapy-ui
Scapy UI

A web based Scapy GUI, major features:

- Edit packet and send
- Load/Save packet templates
- Browse packet detail and hex
- Packet sniffer and dump
- Load and browse pcap file

Requirements:

- yum install python3-devel
- pip3 install scapy flexx psutil

Start:

- sudo ./scapy-ui.py --app

Setup a remote server:

- sudo ./scapy-ui.py --flexx-hostname=`hostname` --flexx-port=49190
- http://{hostname}:49190/ScapyUI/

TBD:

- Generate field from Scapy fields descriptors.
- Better/more protocol editor
