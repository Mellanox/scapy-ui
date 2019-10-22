from scapy.all import *
from flexx import flx
from layers.LayerBase import *

raw_descs = {
	"load":FieldDesc("Raw")
}

class LayerRaw(LayerBase):
	def init(self):
		super().init(raw_descs)
		with self._cont:
			ScapyTextField(self, "load", 21)
