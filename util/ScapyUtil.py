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
        name = cls.__name__
        if cls in layer_url:
            url = layer_url[cls]
        else:
            url = "https://en.wikipedia.org/wiki/" + name
        html = '<a href="' + url + '" target="_blank">' + name + '</a>'
        w.set_html(html)

# get scapy expr of pkt config: Ehter(src="2", type=1)/IP()
# list_pkt_repr: [[class_name, {file_name:filed_val, ...}], ...]
def get_repr_str(list_pkt_repr):
    list_pkt_str = []
    for (cls, map) in list_pkt_repr:
        list_field_str = []
        for (k,v) in map.items():
            list_field_str.append(k + "=" + v)
        list_pkt_str.append(cls + "(" + ",".join(list_field_str) + ")")
    return "/".join(list_pkt_str)

def pkt_to_repr(self, pkt):
    list = []
    while not isinstance(pkt, NoPayload):
        for (k,v) in pkt.fields.items():
            if type(v) == FlagValue:
                pkt.fields[k] = v.value
        list.append([type(pkt).__name__, repr(pkt.fields)])
        pkt = pkt.payload
    return list
    
