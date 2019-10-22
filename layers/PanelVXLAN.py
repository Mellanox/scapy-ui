from scapy.all import *
from flexx import flx
from layers.LayerBase import *

class LayerVXLAN(LayerBase):
	vni = flx.StringProp(settable=True)
	flags = flx.StringProp(settable=True)
	def init(self):
		super().init()
		with self._cont:
			flx.Label(text="VXLAN", flex=2)
			flx.Label(text="VNI:", flex=1)
			self.txt_vni = flx.LineEdit(text=lambda: self.vni, flex=9)
			flx.Label(text="" ,flex=1)
			flx.Label(text="flags:" ,flex=1)
			self.txt_flags = flx.LineEdit(text=lambda: self.flags ,flex=9)
		
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		with self.root.pnl_root:
		    pnl = PanelVXLAN(self, flex=1)
		self.root.show_panel(pnl)
	
	@flx.reaction('txt_vni.text', 'txt_flags.text')
	def on_update(self, *events):
		self.set_vni(self.txt_vni.text.strip())
		self.set_flags(self.txt_flags.text.strip())
		self.pkt_update()

	def pkt_load(self, pkt):
		super().pkt_load(pkt)
		if pkt:
			self.set_vni(str(self.pkt.fields.get('vni',"")))
			self.set_flags(str(self.pkt.fields.get('flags',"")))
	
	def pkt_update(self):
		if len(self.vni):
			self.pkt.vni = int(self.vni)
		if len(self.flags):
			self.pkt.flags = int(self.flags)
		super().pkt_update()

class PanelVXLAN(PanelLayer):
	def init(self, parent):
		super().init(parent)
		with self._form:
			self.txt_vni = flx.LineEdit(title="VNI", text=lambda: self._parent.vni)
			self.txt_flags = flx.LineEdit(title="Flags", text=lambda: self._parent.flags)

	@flx.reaction('txt_vni.text', 'txt_flags.text')
	def on_update(self, *events):
		self._parent.set_vni(self.txt_vni.text.strip())
		self._parent.set_flags(self.txt_flags.text.strip())
		super().on_update()
		