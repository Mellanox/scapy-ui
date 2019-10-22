from scapy.all import *
from flexx import flx
from layers.LayerBase import *

ip_descs = {
	"src":IpDesc("Source"),
	"dst":IpDesc("Destination"),
	"tos":FieldDesc("TOS", int),
	"len":FieldDesc("Length", int),
	"ids":FieldDesc("ID", int),
	"flags":FieldDesc("Flags", int),
	"frag":FieldDesc("Fragment", int),
	"ttl":FieldDesc("TTL", int),
	"chksum":FieldDesc("Checksum", int)
}

class LayerIP(LayerBase):
	def init(self):
		super().init(ip_descs)
		with self._cont:
			ScapyTextField(self, "src", 10)
			flx.Label(text="->" ,flex=1, css_class="center")
			ScapyTextField(self, "dst", 10)

		