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
	def init(self):
		with flx.HBox():
			self.pkt = IP(src="1.2.3.4")
			flx.Label(text="Src")
			self.txt_src = flx.LineEdit()
			flx.Label(text="Dst")
			self.txt_dst = flx.LineEdit()
			self.btn_detail = flx.Button(text="...")
		self.refresh_pkt()
		
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		pkt_set(self.txt_src, self.pkt, 'src')
		pkt_set(self.txt_dst, self.pkt, 'dst')
		with self:
		    pnl = PanelIP(self)
		self.root.show_panel(pnl)
	
	def refresh_pkt(self):
		txt_set(self.txt_src, self.pkt, 'src')
		txt_set(self.txt_dst, self.pkt, 'dst')

class PanelIP(flx.PyWidget):
	def init(self, parent):
		self._parent = parent
		self.pkt = parent.pkt
		with flx.VBox():
			flx.Label(text = parent.pkt.__class__.__name__, css_class="title")
			with flx.FormLayout(flex=2):
				self.txt_src = flx.LineEdit(title="Source")
				txt_set(self.txt_src, self.pkt, 'src')
				self.txt_dst = flx.LineEdit(title="Destination")
				txt_set(self.txt_dst, self.pkt, 'dst')
			flx.Label()
			flx.Label(text = "Scapy:", css_class="title")
			self.lbl_scapy = flx.Label()
			flx.Label()
			flx.Label(text = "Hex:", css_class="title")
			self.lbl_hex = flx.Label()
			flx.Label()
			self.btn_save = flx.Button(title="", text='Back')

	@flx.reaction('btn_save.pointer_click')
	def on_save(self, *events):
		self._parent.refresh_pkt()
		self.root.show_tx()

	@flx.reaction
	def on_update(self, *events):
		# HOWTO bind src property?
		# HOWTO bind src property?
		pkt_set(self.txt_src, self.pkt, 'src')
		pkt_set(self.txt_dst, self.pkt, 'dst')
		self.lbl_scapy.set_text(repr(self.pkt))
		self.lbl_hex.set_text(hexdump(self.pkt, dump=True))
