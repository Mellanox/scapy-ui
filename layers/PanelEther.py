from scapy.all import *
from flexx import flx
from layers.LayerBase import *

ether_descs = {
	"src":MacDesc("Source"),
	"dst":MacDesc("Destination"),
	"type":FieldDesc("Type", int)
}

class LayerEther(LayerBase):
	def init(self):
		super().init(ether_descs, PanelEther)
		with self._cont:
			ScapyTextField(self, "src", 10)
			flx.Label(text="->" ,flex=1, css_class="center")
			ScapyTextField(self, "dst", 10)

# Just a demo of how to customize detail panel
class PanelEther(PanelLayer):
	def init(self, parent):
		super().init(parent, ether_descs)
		with self._cont:
			ScapyTextField(self, "src")
			ScapyTextField(self, "dst")
			ScapyTextField(self, "type")

		