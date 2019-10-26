from scapy.all import *
from flexx import flx

class FieldDesc():
	def __init__(self, title, type=str):
		self.title = title
		self.type = type
		
class ScapyTextField(flx.PyWidget):
	def init(self, parent, name, flex=1):
		self._parent = parent
		self.name = name
		self.desc = parent.descs[name]
		with parent._cont:
			self.w = flx.LineEdit(flex=flex, title=self.desc.title)
		self._parent.fields.append(self)
	
	def load_pkt(self, pkt):
		self.w.set_text(pkt.fields.get('src',""))
		
	@flx.reaction('w.user_text')
	def update_pkt(self, *events):
		text = events[-1]['new_value'].strip()
		if len(text):
			if self.desc.type == int:
				v = int(text)
				exec("self._parent.pkt.{} = {}".format(self.name, v))
			else:
				exec("self._parent.pkt.{} = '{}'".format(self.name, text))
		else:
			self._parent.pkt.fields.pop(self.name, None)
		self._parent.on_update()
	

class LayerBase(flx.PyWidget):
	scapy = flx.StringProp(settable=True)
	hex = flx.StringProp(settable=True)
	
	fields = []
	def init(self, descs={}, cls_detail=None):
		self.descs = descs
		self.cls_detail = cls_detail
		with flx.HFix():
			self.lbl_title = flx.Label(flex=2)
			self._cont = flx.HFix(flex=21)
			self.btn_detail = flx.Button(text="...", flex=1, disabled = not cls_detail)
			
	def on_update(self):
		self.root.pnl_tx.on_packet_update()
	
	@flx.action
	def pkt_load(self, pkt):
		self.pkt = pkt
		if not pkt:
			self.set_parent(None)
			return
		self.set_parent(self.root.pnl_tx.detl._root)
		self.lbl_title.set_text(pkt.__class__._name)
		for w in self.fields:
			w.load_pkt(pkt) 
			
	@flx.reaction('btn_detail.pointer_click')
	def on_detail(self, *events):
		with self.root.pnl_root:
		    pnl = self.cls_detail(self, flex=1)
		pnl.pkt_load(self.pkt)
		self.root.show_panel(pnl)

	# to be removed:	
	def set_pkt_int(self, fld, val = None):
		if val == None:
			val = fld
		cmd = """if len(self.{1}):
	self.pkt.{0} = int(self.{1})
else:
	self.pkt.fields.pop('{0}', None)"""
		cmd = cmd.format(fld, val)
		exec(cmd)

	def set_pkt_str(self, fld, val = None):
		if val == None:
			val = fld
		cmd = """if len(self.{1}):
	self.pkt.{0} = self.{1}
else:
	self.pkt.fields.pop('{0}', None)"""
		cmd = cmd.format(fld, val)
		exec(cmd)
		


class PanelLayer(flx.PyWidget):
	fields = []
	def init(self, descs={}):
		self.descs = descs
		with flx.VBox(flex=1):
			self.lbl_title = flx.Label(css_class="title")
			with flx.VBox():
				self._form = flx.FormLayout()
			self._cont = self._form
			flx.Label()
			self.lbl_scapy = flx.MultiLineEdit(flex=5)
			flx.Label()
			self.lbl_hex = flx.Label(wrap=1, flex=5)

	def pkt_load(self, pkt):
		self.pkt = pkt
		self.lbl_title.set_text(pkt.__class__._name)
		for w in self.fields:
			w.load_pkt(pkt) 
		
	def on_update(self):
		self.lbl_scapy.setText(self.pkt.show(dump=True))
		self.lbl_hex.setText(hexdump(self.pkt, dump=True))
		