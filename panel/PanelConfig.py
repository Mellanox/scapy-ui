from scapy.all import *
from flexx import flx


class PanelConfig(flx.PyWidget):
	def init(self):
		with flx.VBox():
			with flx.VBox(flex=1) as self.lst_config:
				self.pnl_tx = flx.Label(text='ether')
				self.pnl_tx = flx.Label(text='ipv4')
				self.pnl_tx = flx.Label(text='ipv6')
				self.pnl_tx = flx.Label(text='vxlan')
				self.pnl_tx = flx.Label(text='vxlan-ali')
			self.btn_load = flx.Button(text='Load...')
			self.btn_sniff = flx.Button(text='Sniff...')

	@flx.reaction('btn_load.pointer_click')
	def on_load(self, *events):
		self.root.show_rx()

	@flx.reaction('btn_sniff.pointer_click')
	def on_sniff(self, *events):
		self.root.show_rx()

