from scapy.all import *
from flexx import flx
from layers.LayerBasic import *

icmp_descs = {
    "type":FieldDesc("Type", int, ("8 #send", "0 #resp")),
    "code":FieldDesc("Code", int),
    "chksum":FieldDesc("Checksum", int),
    "id":FieldDesc("Identifier", int),
    "seq":FieldDesc("Sequence #", int),
}

class LayerICMP(LayerBasic):
    def init(self):
        super().init(icmp_descs)
        with self._cont:
            ScapyTextField(self, "type", 10)
            flx.Label(text="Seq:" ,flex=1, css_class="center")
            ScapyTextField(self, "seq", 10)

mpls_descs = {
    "type":FieldDesc("Type", int, ("8 #send", "0 #resp")),
    "code":FieldDesc("Code", int),
    "chksum":FieldDesc("Checksum", int),
    "id":FieldDesc("Identifier", int),
    "seq":FieldDesc("Sequence #", int),
}

class LayerICMP(LayerBasic):
    def init(self):
        super().init(icmp_descs)
        with self._cont:
            ScapyTextField(self, "type", 10)
            flx.Label(text="Seq:" ,flex=1, css_class="center")
            ScapyTextField(self, "seq", 10)

arp_descs = {
    "hwtype":FieldDesc("HW Type", int),
    "ptype":FieldDesc("Ether Type", int),
    "hwlen":FieldDesc("HW Address Length", int),
    "plen":FieldDesc("Protocol Address Length", int),
    "op":FieldDesc("OP", int),
    "hwsrc":MacDesc("Source MAC"),
    "psrc":IpDesc("Source IP"),
    "hwdst":MacDesc("Destination MAC"),
    "pdst":IpDesc("Destination IP"),
}

class LayerARP(LayerBasic):
    def init(self):
        super().init(arp_descs)
        with self._cont:
            ScapyTextField(self, "psrc", 10)
            flx.Label(text="->" ,flex=1, css_class="center")
            ScapyTextField(self, "pdst", 10)

gre_descs = {
    "chksum_present":FieldDesc("Checksum Present", int),
    "routing_present":FieldDesc("Routing Present", int),
    "key_present":FieldDesc("HW Key Present", int),
    "seqnum_present":FieldDesc("Sequence # Present", int),
    "strict_route_source":FieldDesc("Strict Route Source", int),
    "recursion_control":FieldDesc("Recursion Control", int),
    "flags":FieldDesc("Flags", int),
    "version":FieldDesc("Version", int),
    "proto":FieldDesc("Protocol Type", int),
    "chksum":FieldDesc("Checksum", int),
    "offset":FieldDesc("Offset", int),
    "key":FieldDesc("Key", int),
    "seqence_number":FieldDesc("Sequence #", int),
}

class LayerGRE(LayerBasic):
    def init(self):
        super().init(gre_descs)
        with self._cont:
            ScapyTextField(self, "proto", 21)

                                