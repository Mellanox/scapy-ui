from scapy.all import *
from flexx import flx
from layers.LayerBase import *

class LayerRaw(LayerBase):
	raw = flx.StringProp(settable=True)
	def init(self):
		super().init()
		with self._cont:
			flx.Label(text="Raw", flex=2)
			self.txt_raw = flx.LineEdit(text=lambda: self.raw, flex=21)
		
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		with self.root.pnl_root:
		    pnl = PanelRaw(self, flex=1)
		self.root.show_panel(pnl)
	
	@flx.reaction('txt_raw.text')
	def on_update(self, *events):
		self.set_raw(self.txt_raw.text.strip())
		self.pkt_update()

	def pkt_load(self, pkt):
		super().pkt_load(pkt)
		if pkt:
			b = self.pkt.fields.get('load',bytes("",'utf8'))
			self.set_raw(b.decode())
	
	@flx.action
	def pkt_update(self):
		self.set_pkt_str('load','raw')
		super().pkt_update()

class PanelRaw(PanelLayer):
	def init(self, parent):
		super().init(parent)
		with self._form:
			self.txt_raw = flx.MultiLineEdit(title="Source", text=lambda: self._parent.raw)

	@flx.reaction('txt_raw.text')
	def on_update(self, *events):
		self._parent.set_raw(self.txt_raw.text.strip())
		super().on_update()
		