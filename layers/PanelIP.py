from scapy.all import *
from flexx import flx
from layers.LayerPanel import *


ip_descs = {
    "src":IpDesc("Source"),
    "dst":IpDesc("Destination"),
    "tos":FieldDesc("TOS", int, ("#DSCP:6 << 2 + ECN:2", "# https://en.wikipedia.org/wiki/Type_of_service"), url="https://en.wikipedia.org/wiki/Type_of_service"),
    "len":FieldDesc("Length", int),
    "ids":FieldDesc("ID", int),
    "flags":FieldDesc("Flags", int, ("1 #Multiple Fragment", "2 #Don't Fragment")),
    "frag":FieldDesc("Fragment", int),
    "ttl":FieldDesc("TTL", int),
    "chksum":FieldDesc("Checksum", int)
}

class LayerIP(PanelProtocolRow):
    def init(self):
        super().init(ip_descs)
        with self._cont:
            ScapyTextField(self, "src", 10)
            flx.Label(text="->" ,flex=1, css_class="center")
            ScapyTextField(self, "dst", 10)

        