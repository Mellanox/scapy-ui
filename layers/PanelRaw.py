from scapy.all import *
from flexx import flx
from layers.LayerPanel import *

raw_descs = {
    "load":FieldDesc("Raw", bytes, ("'abcd'", "'a' * 10", 'bytes.fromhex("00 01 02 03")'), widget="MultiLineEdit")
}

class LayerRaw(PanelProtocolRow):
    def init(self):
        super().init(raw_descs)
        with self._cont:
            ScapyTextField(self, "load", 21)
