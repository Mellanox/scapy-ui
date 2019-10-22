from scapy.all import *
from flexx import flx
import configparser
import os

class LayerIP(flx.PyWidget):
	src = flx.StringProp(settable=True)
	dst = flx.StringProp(settable=True)
	ttl = flx.StringProp(settable=True)
	scapy = flx.StringProp(settable=True)
	hex = flx.StringProp(settable=True)
	def init(self):
		self.pkt_load(IP(src='192.168.1.1'))
		with flx.HBox():
			flx.Label(text="Src")
			self.txt_src = flx.LineEdit(text=lambda: self.src)
			flx.Label(text="Dst")
			self.txt_dst = flx.LineEdit(text=lambda: self.dst)
			self.btn_detail = flx.Button(text="...")
		
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		with self.root:
		    pnl = PanelIP(self)
		self.root.show_panel(pnl)
	
	@flx.reaction('txt_src.text', 'txt_dst.text')
	def on_update(self, *events):
		self.set_src(self.txt_src.text.strip())
		self.set_dst(self.txt_dst.text.strip())
		self.pkt_update()

	def pkt_load(self, pkt):
		self.pkt = pkt
		self.set_src(self.pkt.fields.get('src',""))
		self.set_dst(self.pkt.fields.get('dst',""))
	
	def pkt_update(self):
		self.pkt.src = self.src
		self.pkt.dst = self.dst
		if len(self.ttl):
			self.pkt.ttl = int(self.ttl)
		self.set_scapy(self.pkt.show(dump=True))
		self.set_hex(hexdump(self.pkt, dump=True))

class PanelIP(flx.PyWidget):
	CSS = """
		.flx-PanelIP {min-height: 600px;}
	"""

	def init(self, parent):
		self._parent = parent
		with flx.VBox():
			flx.Label(text = parent.pkt.__class__.__name__, css_class="title", flex=1)
			with flx.FormLayout(flex=10):
				self.txt_src = flx.LineEdit(title="Source", text=lambda: self._parent.src)
				self.txt_dst = flx.LineEdit(title="Destination", text=lambda: self._parent.dst)
				self.txt_ttl = flx.LineEdit(title="TTL", text=lambda: self._parent.ttl)
			flx.Label(flex=1)
			self.lbl_scapy = flx.MultiLineEdit(text=lambda: self._parent.scapy, flex=50)
			flx.Label(flex=1)
			self.lbl_hex = flx.Label(wrap=1, text=lambda: self._parent.hex, flex=5)
			flx.Label(flex=1)
			self.btn_save = flx.Button(title="", text='Back', flex=1)

	@flx.reaction('btn_save.pointer_click')
	def on_save(self, *events):
		self.root.show_tx()

	@flx.reaction('txt_src.text', 'txt_dst.text', 'txt_ttl.text')
	def on_update(self, *events):
		self._parent.set_src(self.txt_src.text.strip())
		self._parent.set_dst(self.txt_dst.text.strip())
		self._parent.set_ttl(self.txt_ttl.text.strip())
		self._parent.pkt_update()
		