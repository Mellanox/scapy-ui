from scapy.all import *
from flexx import flx


class ConfigItem(flx.PyWidget):
	def init(self, text):
		self.label = flx.Label(text = text, flex=1)

	@flx.reaction('label.pointer_click')
	def on_click(self, *events):
		self.root.pnl_config.on_config_load(self.label.text)

class PanelConfig(flx.PyWidget):
	def init(self):
		with flx.VBox():
			flx.Label(text = "Configurations:")
			with flx.VBox() as self.lst_config:
				self.pnl_tx = ConfigItem('ether')
				self.pnl_tx = ConfigItem('ipv4')
				self.pnl_tx = ConfigItem('ipv6')
				self.pnl_tx = ConfigItem('vxlan')
				self.pnl_tx = ConfigItem('vxlan-ali')
			flx.VBox(flex=1)
			self.btn_load = flx.Button(text='Load...')
			self.btn_sniff = flx.Button(text='Sniff...')

	# @flx.reaction('lst_config.children*.pointer_click')
	# @flx.action
	def on_config_load(self, name):
		config = self.load_config(name)
		pkt = self.parse_scapy(config)
		if pkt != None:
			self.root.show_tx(name, pkt) 

	@flx.reaction('btn_load.pointer_click')
	def on_pcap_load(self, *events):
		self.root.show_rx()

	@flx.reaction('btn_sniff.pointer_click')
	def on_sniff(self, *events):
		self.root.show_rx()

	def load_config(self, name):
		# TODO
		pkt = Ether() # /IP("1.2.3.4")/UDP(sport=123)
		print(pkt)
		config = self.scapy_dump(pkt)
		print(config)
		return config

	def save_config(self, name, pkt):
		config = scap_dump(pkt)
		print(config)
		# TODO
		
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
