from scapy.all import *
from flexx import flx

class LayerBase(flx.PyWidget):
	scapy = flx.StringProp(settable=True)
	hex = flx.StringProp(settable=True)
	def init(self, pkt):
		self.pkt = pkt
		with flx.HBox():
			self._cont = flx.HBox(flex=1)
			self.btn_detail = flx.Button(text="...")
		
	def pkt_update(self):
		self.set_scapy(self.pkt.show(dump=True))
		self.set_hex(hexdump(self.pkt, dump=True))
		# tell tx panel to update


class PanelLayer(flx.PyWidget):
	def init(self, parent):
		self._parent = parent
		with flx.VBox():
			flx.Label(text = parent.pkt.__class__.__name__, css_class="title", flex=1)
			self._form = flx.FormLayout(flex=10)
			flx.Label(flex=1)
			self.lbl_scapy = flx.MultiLineEdit(text=lambda: self._parent.scapy, flex=50)
			flx.Label(flex=1)
			self.lbl_hex = flx.Label(wrap=1, text=lambda: self._parent.hex, flex=5)
			flx.Label(flex=1)
			self.btn_save = flx.Button(title="", text='Apply', flex=1)

	@flx.reaction('btn_save.pointer_click')
	def on_save(self, *events):
		self.root.show_tx()

	def on_update(self, *events):
		self._parent.pkt_update()
		
		