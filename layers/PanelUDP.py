from scapy.all import *
from flexx import flx
from layers.LayerBase import *

class LayerUDP(LayerBase):
	src = flx.StringProp(settable=True)
	dst = flx.StringProp(settable=True)
	len = flx.StringProp(settable=True)
	cksum = flx.StringProp(settable=True)
	def init(self):
		super().init()
		with self._cont:
			flx.Label(text="UDP", flex=2)
			self.txt_src = flx.LineEdit(text=lambda: self.src, flex=10)
			flx.Label(text="->" ,flex=1)
			self.txt_dst = flx.LineEdit(text=lambda: self.dst ,flex=10)
		
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		with self.root.pnl_root:
		    pnl = PanelUDP(self, flex=1)
		self.root.show_panel(pnl)
	
	@flx.reaction('txt_src.text', 'txt_dst.text')
	def on_update(self, *events):
		self.set_src(self.txt_src.text.strip())
		self.set_dst(self.txt_dst.text.strip())
		self.pkt_update()

	def pkt_load(self, pkt):
		super().pkt_load(pkt)
		if pkt:
			self.set_src(str(self.pkt.fields.get('sport',"")))
			self.set_dst(str(self.pkt.fields.get('dport',"")))
			self.set_len(str(self.pkt.fields.get('len',"")))
			self.set_cksum(str(self.pkt.fields.get('chsum',"")))

	@flx.action
	def pkt_update(self):
		self.set_pkt_int('sport', 'src')
		self.set_pkt_int('dport', 'dst')
		self.set_pkt_int('len')
		self.set_pkt_int('chksum', 'cksum')
		super().pkt_update()

class PanelUDP(PanelLayer):
	def init(self, parent):
		super().init(parent)
		with self._form:
			self.txt_src = flx.LineEdit(title="Source", text=lambda: self._parent.src)
			self.txt_dst = flx.LineEdit(title="Destination", text=lambda: self._parent.dst)
			self.txt_len = flx.LineEdit(title="Length", text=lambda: self._parent.len)
			self.txt_cksum = flx.LineEdit(title="Checksum", text=lambda: self._parent.cksum)

	@flx.reaction('txt_src.text', 'txt_dst.text', 'txt_len.text', 'txt_cksum.text')
	def on_update(self, *events):
		self._parent.set_src(self.txt_src.text.strip())
		self._parent.set_dst(self.txt_dst.text.strip())
		self._parent.set_len(self.txt_len.text.strip())
		self._parent.set_cksum(self.txt_cksum.text.strip())
		super().on_update()
		