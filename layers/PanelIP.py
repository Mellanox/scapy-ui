from scapy.all import *
from flexx import flx
from layers.LayerBase import *

class LayerIP(LayerBase):
	src = flx.StringProp(settable=True)
	dst = flx.StringProp(settable=True)
	ttl = flx.StringProp(settable=True)
	def init(self):
		super().init()
		with self._cont:
			flx.Label(text="IPv4", flex=2)
			self.txt_src = flx.LineEdit(text=lambda: self.src, flex=10)
			flx.Label(text="->" ,flex=1)
			self.txt_dst = flx.LineEdit(text=lambda: self.dst ,flex=10)
		
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		with self.root.pnl_root:
		    pnl = PanelIP(self, flex=1)
		self.root.show_panel(pnl)
	
	@flx.reaction('txt_src.text', 'txt_dst.text')
	def on_update(self, *events):
		self.set_src(self.txt_src.text.strip())
		self.set_dst(self.txt_dst.text.strip())
		self.pkt_update()

	def pkt_load(self, pkt):
		super().pkt_load(pkt)
		if pkt:
			self.set_src(self.pkt.fields.get('src',""))
			self.set_dst(self.pkt.fields.get('dst',""))
			self.txt_src.set_disabled(0)
			self.txt_dst.set_disabled(0)
		else:
			self.txt_src.set_disabled(1)
			self.txt_dst.set_disabled(1)

	@flx.action
	def pkt_update(self):
		self.set_pkt_str("src")
		self.set_pkt_str("dst")
		self.set_pkt_int("ttl")
		super().pkt_update()

class PanelIP(PanelLayer):
	def init(self, parent):
		super().init(parent)
		with self._form:
			self.txt_src = flx.LineEdit(title="Source", text=lambda: self._parent.src)
			self.txt_dst = flx.LineEdit(title="Destination", text=lambda: self._parent.dst)
			self.txt_ttl = flx.LineEdit(title="TTL", text=lambda: self._parent.ttl)

	@flx.reaction('txt_src.text', 'txt_dst.text', 'txt_ttl.text')
	def on_update(self, *events):
		self._parent.set_src(self.txt_src.text.strip())
		self._parent.set_dst(self.txt_dst.text.strip())
		self._parent.set_ttl(self.txt_ttl.text.strip())
		super().on_update()
		