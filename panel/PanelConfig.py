from scapy.all import *
from flexx import flx
import configparser
import os


class ConfigItem(flx.PyWidget):
	def init(self, text):
		self.label = flx.Label(text = text, flex=1, css_class="item")

	@flx.reaction('label.pointer_click')
	def on_click(self, *events):
		self.root.pnl_config.load_config(self.label.text)

class PanelConfig(flx.PyWidget):
	def init(self):
		self.cfg_name = '.scapy-ui'
		self.lst_names = []
		with flx.VBox():
			self.lst_config = flx.GroupWidget(title="Recent:", flex=1, css_class="list")
			self.btn_load = flx.Button(text='Load Pcap...')
			self.btn_sniff = flx.Button(text='Sniff...')
		self.load_names()
		

	def load_names(self):
		for item in self.lst_names:
			item.set_parent(None)
			item = None
		self.lst_names[:] = []
		os.chdir(os.path.expanduser('~'))
		cf = configparser.ConfigParser()
		cf.read(self.cfg_name)
		if not cf.has_section('recent'):
			return
		with self.lst_config:
			for key in cf['recent']:
				item = ConfigItem(key)
				self.lst_names.append(item)

	def load_config(self, name):
		cf = configparser.ConfigParser()
		cf.read(self.cfg_name)
		config = cf['recent'][name]
		pkt = self.parse_scapy(config)
		if pkt != None:
			self.root.load_config(name, pkt) 
			
	def save_config(self, name, pkt):
		cf = configparser.ConfigParser()
		cf.read(self.cfg_name)
		config = self.scapy_dump(pkt)
		print(config)
		if not cf.has_section('recent'):
			cf.add_section('recent')
		cf['recent'][name] = config
		with open(self.cfg_name, "w") as f:
			cf.write(f)
		self.load_names()
	
	def del_config(self, name):
		cf = configparser.ConfigParser()
		cf.read(self.cfg_name)
		if not cf.has_section('recent'):
			return
		cf['recent'].pop(name, None)
		with open(self.cfg_name, "w") as f:
			cf.write(f)
		self.load_names()

	@flx.reaction('btn_load.pointer_click')
	def on_pcap_load(self, *events):
		self.root.show_rx()

	@flx.reaction('btn_sniff.pointer_click')
	def on_sniff(self, *events):
		self.root.show_rx()

	def scapy_dump(self, pkt):
		list = []
		while not isinstance(pkt, NoPayload):
			list.append([pkt.__class__.__name__, repr(pkt.fields)])
			pkt = pkt.payload
		return repr(list)
	
	def parse_scapy(self, str):
		list = eval(str)
		pkt = None
		for layer_config in list:
			layer = eval(layer_config[0]+"()")
			fields = eval(layer_config[1])
			layer.fields = fields
			if pkt == None:
				pkt = layer
			else:
				pkt.add_payload(layer)
		return pkt
