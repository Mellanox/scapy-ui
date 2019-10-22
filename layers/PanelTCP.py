from scapy.all import *
from flexx import flx
from layers.LayerBase import *

tcp_descs = {
	"sport":FieldDesc("Source", int),
	"dport":FieldDesc("Destination", int),
	"len":FieldDesc("Length", int),
	"chksum":FieldDesc("Checksum", int)
}

class LayerTCP(LayerBase):
	def init(self):
		super().init(tcp_descs)
		with self._cont:
			ScapyTextField(self, "sport", 10)
			flx.Label(text="->" ,flex=1, css_class="center")
			ScapyTextField(self, "dport", 10)