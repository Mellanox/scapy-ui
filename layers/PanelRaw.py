from scapy.all import *
from flexx import flx
from layers.LayerBase import *

class LayerRaw(LayerBase):
	load = flx.StringProp(settable=True)
	def init(self):
		super().init()
		with self._cont:
			flx.Label(text="Raw", flex=2)
			self.txt_load = flx.LineEdit(text=lambda: self.load, flex=21)
		
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		with self.root.pnl_root:
		    pnl = PanelRaw(self, flex=1)
		self.root.show_panel(pnl)
	
	@flx.reaction('txt_load.text')
	def on_update(self, *events):
		self.set_load(self.txt_load.text.strip())
		self.pkt_update()

	def pkt_load(self, pkt):
		super().pkt_load(pkt)
		if pkt:
			self.set_load(self.pkt.fields.get('load',""))
	
	def pkt_update(self):
		if len(self.load):
			self.pkt.load = self.load
		super().pkt_update()

class PanelRaw(PanelLayer):
	def init(self, parent):
		super().init(parent)
		with self._form:
			self.txt_load = flx.MultiLineEdit(title="Source", text=lambda: self._parent.load)

	@flx.reaction('txt_load.text')
	def on_update(self, *events):
		self._parent.set_load(self.txt_load.text.strip())
		super().on_update()
		