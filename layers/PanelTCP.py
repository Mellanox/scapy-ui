from scapy.all import *
from flexx import flx
from layers.LayerPanel import *

tcp_descs = {
    "sport": PortDesc("Source Port"),
    "dport": PortDesc("Destination Port"),
    "seq": FieldDesc("Sequence #", int),
    "acl": FieldDesc("Acnolegement #", int),
    "dataofs": FieldDesc("Data Offset", int),
    "reserved": FieldDesc("Reserved", int),
    "flags": FieldDesc("Flags", int, ("1 #FIN", "2 #SYN", "4 #RST", "8 #PSH", "0x10 #ACK", "0x20 #URG")),
    "window": FieldDesc("Window", int),
    "chksum": FieldDesc("Checksum", int),
    "urgptr": FieldDesc("Urgent Pointer", int),
    "options": FieldDesc("Options", int,
        (
            "[('Experiment', (0xf989, 0xcafe, 0x0102, 0x0002))]",
            "[('NOP', 0), ('MSS', 2)]",
        )
    )
}

class LayerTCP(PanelProtocolRow):
    def init(self):
        super().init(tcp_descs)
        with self._cont:
            ScapyTextField(self, "sport", 10)
            flx.Label(text="->" ,flex=1, css_class="center")
            ScapyTextField(self, "dport", 10)