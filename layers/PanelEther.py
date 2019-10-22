from scapy.all import *
from flexx import flx
from layers.LayerBase import *

class LayerEther(LayerBase):
	src = flx.StringProp(settable=True)
	dst = flx.StringProp(settable=True)
	type = flx.StringProp(settable=True)
	def init(self):
		super().init()
		with self._cont:
			flx.Label(text="Ether", flex=2)
			self.txt_src = flx.LineEdit(text=lambda: self.src, flex=10)
			flx.Label(text="->" ,flex=1)
			self.txt_dst = flx.LineEdit(text=lambda: self.dst ,flex=10)
		
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		with self.root.pnl_root:
		    pnl = PanelEther(self, flex=1)
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
	
	def pkt_update(self):
		if len(self.src):
			self.pkt.src = self.src
		if len(self.dst):
			self.pkt.dst = self.dst
		if len(self.type):
			self.pkt.type = int(self.type)
		super().pkt_update()

class PanelEther(PanelLayer):
	def init(self, parent):
		super().init(parent)
		with self._form:
			self.txt_src = flx.LineEdit(title="Source", text=lambda: self._parent.src)
			self.txt_dst = flx.LineEdit(title="Destination", text=lambda: self._parent.dst)
			self.txt_type = flx.LineEdit(title="Type", text=lambda: self._parent.type)

	@flx.reaction('txt_src.text', 'txt_dst.text', 'txt_type.text')
	def on_update(self, *events):
		self._parent.set_src(self.txt_src.text.strip())
		self._parent.set_dst(self.txt_dst.text.strip())
		self._parent.set_type(self.txt_type.text.strip())
		super().on_update()
		