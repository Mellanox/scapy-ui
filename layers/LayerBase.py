from scapy.all import *
from flexx import flx

class LayerBase(flx.PyWidget):
	scapy = flx.StringProp(settable=True)
	hex = flx.StringProp(settable=True)
	def init(self):
		with flx.HFix():
			self._cont = flx.HFix(flex=23)
			self.btn_detail = flx.Button(text="...", flex=1)
		
	def pkt_update(self):
		self.set_scapy(self.pkt.show(dump=True))
		self.set_hex(hexdump(self.pkt, dump=True))
		# tell tx panel to update
	
	def pkt_load(self, pkt):
		self.pkt = pkt
		if pkt:
			self.btn_detail.set_disabled(0)
		else:
			self.btn_detail.set_disabled(1)
	


class PanelLayer(flx.PyWidget):
	def init(self, parent):
		self._parent = parent
		with flx.VBox(flex=1, css_class="debug"):
			flx.Label(text = parent.pkt.__class__.__name__, css_class="title")
			with flx.VBox():
				self._form = flx.FormLayout()
			flx.Label()
			self.lbl_scapy = flx.MultiLineEdit(text=lambda: self._parent.scapy, flex=5)
			flx.Label()
			self.lbl_hex = flx.Label(wrap=1, text=lambda: self._parent.hex, flex=5)
			flx.Label()

	def on_update(self, *events):
		self._parent.pkt_update()
		
		