from scapy.all import *
from flexx import flx
from layers.LayerBase import *

ether_descs = {
	"src":FieldDesc("Source"),
	"dst":FieldDesc("Destination"),
	"type":FieldDesc("Type", int)
}

class LayerEther(LayerBase):
	def init(self):
		super().init(ether_descs, PanelEther)
		with self._cont:
			ScapyTextField(self, "src", 10)
			flx.Label(text="->" ,flex=1, css_class="center")
			ScapyTextField(self, "dst", 10)

class PanelEther(PanelLayer):
	def init(self, parent):
		super().init(ether_descs)
		ScapyTextField(self, "src")
		ScapyTextField(self, "dst")
		ScapyTextField(self, "type")

		