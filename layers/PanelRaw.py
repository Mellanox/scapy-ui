from scapy.all import *
from flexx import flx
from layers.LayerBasic import *

raw_descs = {
    "load":FieldDesc("Raw", bytes, ("'abcd'","'a' * 10"))
}

class LayerRaw(LayerBasic):
    def init(self):
        super().init(raw_descs)
        with self._cont:
            ScapyTextField(self, "load", 21)
