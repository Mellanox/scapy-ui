#!/usr/bin/python3

from scapy.all import *
from flexx import flx

from panel.PanelConfig import *


class ScapyUI(flx.PyWidget):
	def init(self):
		with flx.VBox():
			with flx.HSplit() as self.pnl_main:
				self.pnl_config = PanelConfig()
				with flx.VBox():
					self.pnl_source = flx.Label(text='PanelSource')
					self.pnl_tx = flx.Label(text='PanelTx', flex=1)
		self.pnl_rx = None

	def show_rx(self):
		self.pnl_main.set_parent(None)  # Detach
		if self.pnl_rx == None:
			with self.root:
				self.pnl_rx = flx.Label(text='PanelRx')
		self.pnl_rx.set_parent(self.root)  # Attach
		print('success!')

m = flx.launch(ScapyUI)
flx.run()
