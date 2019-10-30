#!/usr/bin/python3

from scapy.all import *
from flexx import flx, app

layer_url = {
    Ether: "https://en.wikipedia.org/wiki/Ethernet_frame",
    IP: "https://en.wikipedia.org/wiki/IPv4",
    ARP: "https://en.wikipedia.org/wiki/Address_Resolution_Protocol",
    UDP: "https://en.wikipedia.org/wiki/User_Datagram_Protocol",
    TCP: "https://en.wikipedia.org/wiki/Transmission_Control_Protocol",
    ICMP: "https://en.wikipedia.org/wiki/Ping_(networking_utility)",
    VXLAN: "https://tools.ietf.org/html/draft-ietf-nvo3-vxlan-gpe-04",
    GRE: "https://en.wikipedia.org/wiki/Generic_Routing_Encapsulation",
    Raw: "https://en.wikipedia.org/wiki/Ethernet_frame",
}

def link_layer(w, cls):
        name = cls._name
        if cls in layer_url:
            url = layer_url[cls]
        else:
            url = "https://en.wikipedia.org/wiki/" + name
        html = '<a href="' + url + '" target="_blank">' + name + '</a>'
        w.set_html(html)
