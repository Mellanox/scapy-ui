from scapy.all import *
from flexx import flx
from layers.LayerBasic import *

dot1q_descs = {
    "vlan":FieldDesc("VLAN", int),
    "priority":FieldDesc("Priority", int),
    "id":FieldDesc("CFI", int),
    "type":FieldDesc("Type", int)
}

class LayerDot1Q(LayerBasic):
    def init(self):
        super().init(dot1q_descs)
        with self._cont:
            ScapyTextField(self, "vlan", 10)
            flx.Label(text="Type" ,flex=1, css_class="center")
            ScapyTextField(self, "type", 10)        