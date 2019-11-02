from scapy.all import *
from flexx import flx
from layers.LayerPanel import *

class Ipv6Desc(FieldDesc):
    def __init__(self, title):
        super().__init__(title)
        self.autocomp = ("::1","3ffe:ffff:0:f101::1","3ffe:ffff:0:f101::1/127")

ipv6_descs = {
    "version":FieldDesc("Version", int),
    "tc":FieldDesc("Traffic Class", int),
    "fl":FieldDesc("Flow Label", int),
    "plen":FieldDesc("Payload Length", int),
    "nh":FieldDesc("Next Header", int),
    "hlim":FieldDesc("Hop Limit", int),
    "src":Ipv6Desc("Source"),
    "dst":Ipv6Desc("Destination"),
}

class LayerIPv6(PanelProtocolRow):
    def init(self):
        super().init(ipv6_descs)
        with self._cont:
            ScapyTextField(self, "src", 10)
            flx.Label(text="->" ,flex=1, css_class="center")
            ScapyTextField(self, "dst", 10)

        