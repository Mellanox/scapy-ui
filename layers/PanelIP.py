from scapy.all import *
from flexx import flx
import configparser
import os

def txt_set(txt, pkt, name):
	txt.set_text(pkt.fields.get(name, ""))
		
def pkt_set(txt, pkt, name):
	if len(txt.text):
		# pkt.fields[name] = txt.text
		pkt.setfieldval(name, txt.text)
	else:
		pkt.fields.pop(name, None)


class LayerIP(flx.PyWidget):
	src = flx.StringProp("1", settable=True)
	dst = flx.StringProp("2", settable=True)
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
		self.set_src(self.pkt.src)
		self.set_dst(self.pkt.dst)
	
	def pkt_update(self):
		self.pkt.src = self.src
		self.pkt.dst = self.dst
		self.set_scapy(repr(self.pkt))
		self.set_hex(hexdump(self.pkt, dump=True))

class PanelIP(flx.PyWidget):
	def init(self, parent):
		self._parent = parent
		with flx.VBox():
			flx.Label(text = parent.pkt.__class__.__name__, css_class="title")
			with flx.FormLayout(flex=2):
				self.txt_src = flx.LineEdit(title="Source", text=lambda: self._parent.src)
				self.txt_dst = flx.LineEdit(title="Destination", text=lambda: self._parent.dst)
			flx.Label()
			self.lbl_scapy = flx.Label(text=lambda: self._parent.scapy)
			flx.Label()
			self.lbl_hex = flx.Label(text=lambda: self._parent.hex)
			flx.Label()
			self.btn_save = flx.Button(title="", text='Back')

	@flx.reaction('btn_save.pointer_click')
	def on_save(self, *events):
		self.root.show_tx()

	@flx.reaction('txt_src.text', 'txt_dst.text')
	def on_update(self, *events):
		self._parent.set_src(self.txt_src.text.strip())
		self._parent.set_dst(self.txt_dst.text.strip())
		self._parent.pkt_update()
		