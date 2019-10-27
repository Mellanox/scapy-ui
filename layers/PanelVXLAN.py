from scapy.all import *
from flexx import flx
from layers.LayerBasic import *

vxlan_descs = {
    "vni":FieldDesc("VNI", int),
    "flags":FieldDesc("Flags", int),
}

class LayerVXLAN(LayerBasic):
    def init(self):
        super().init(vxlan_descs)
        with self._cont:
            ScapyTextField(self, "vni", 10)
            flx.Label(text="Flags:" ,flex=1, css_class="center")
            ScapyTextField(self, "flags", 10)
            
        