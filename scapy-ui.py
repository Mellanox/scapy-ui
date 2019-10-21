#!/usr/bin/python3

from scapy.all import *
from flexx import flx

from panel.PanelConfig import *
from panel.PanelSource import *
from panel.PanelRx import *

class ScapyUI(flx.PyWidget):
	def init(self):
		with flx.VBox() as self.pnl_main:
			with flx.HSplit(flex=1):
				self.pnl_config = PanelConfig(flex=1)
				with flx.VBox(flex=6):
					self.pnl_source = PanelSource() 
					self.pnl_tx = flx.Label(text='PanelTx', flex=10)
			self.lbl_status = flx.Label(text='...')
#		with flx.VBox(flex=1) as self.pnl_rx:
#			self.btn_rx = flx.Button(text='Back')
		self.pnl_rx = PanelRx()
		self.pnl_rx.set_parent(None)

#	@flx.reaction('btn_rx.pointer_click')
	def on_pcap_load(self, *events):
		self.show_tx()

	def show_tx(self):
		self.pnl_main.set_parent(self._jswidget)  # Attach
		self.pnl_rx.set_parent(None)  # Detach

	def show_rx(self):
		# print(self.__dict__)
		# print(self.pnl_main.parent)
		self.pnl_rx.set_parent(self._jswidget)  # Attach
		self.pnl_main.set_parent(None)  # Detach

	def load_config(self, name, pkt):
		self.pnl_main.set_parent(self.root)
		self.pnl_rx.set_parent(None)
		self.pnl_source.txt_name.set_text(name)
		self.pnl_tx.set_text(repr(pkt))
		self.set_status(name)

	def save_config(self, name):
		pkt = Ether()/IP(src="1.2.3.4")/UDP(sport=123)/"abc"
		self.pnl_config.save_config(name, pkt)

	def del_config(self, name):
		self.pnl_tx.set_text("")
		self.pnl_config.del_config(name)

	def new_config(self, name):
		self.pnl_tx.set_text("")

	def set_status(self, status):
		self.lbl_status.set_text(status)

m = flx.launch(ScapyUI)
flx.run()
