#!/usr/bin/python3

from scapy.all import *
from flexx import flx

from panel.PanelConfig import *


class ScapyUI(flx.PyWidget):
	def init(self):
		with flx.VBox():
			with flx.HSplit(flex=1) as self.pnl_main:
				self.pnl_config = PanelConfig(flex=1)
				with flx.VBox(flex=6):
					self.pnl_source = flx.Label(text='PanelSource')
					self.pnl_tx = flx.Label(text='PanelTx', flex=1)
			self.lbl_status = flx.Label(text='...')
		self.pnl_rx = flx.Label(text='PanelRx')
		self.pnl_rx.set_parent(None)

	def show_rx(self):
		self.pnl_main.set_parent(None)  # Detach
		self.pnl_rx.set_parent(self.root)  # Attach

	def show_tx(self, name, pkt):
		self.pnl_main.set_parent(self.root)
		self.pnl_rx.set_parent(None)
		self.set_status(name)
		self.pnl_tx.set_text(repr(pkt))

	def set_status(self, status):
		self.lbl_status.set_text(status)

m = flx.launch(ScapyUI)
flx.run()
