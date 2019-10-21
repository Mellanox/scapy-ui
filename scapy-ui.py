#!/usr/bin/python3

from scapy.all import *
from flexx import flx

from panel.PanelConfig import *
from panel.PanelSource import *
from panel.PanelRx import *
from panel.PanelTx import *

from layers.PanelIP import *


class ScapyUI(flx.PyWidget):
	CSS = """
		.list {overflow:auto;}
		.link {text-decoration:underline; color:blue;}
		.link:hover {background-color:#EEEEEE;}
		.link:active {text-decoration:none}
		.title {background: #eff;}
		.no_border {border: 0px}
		.debug {border: 5px solid green; background: #eee;}
	"""	

	def init(self):
		with flx.VBox() as self.pnl_main:
			with flx.HSplit(flex=1):
				self.pnl_config = PanelConfig(flex=2)
				with flx.VBox(flex=8):
					LayerIP()
					self.pnl_source = PanelSource() 
					self.pnl_tx = PanelTx(flex=10)
			self.lbl_status = flx.Label(text='...')
		self.pnl_active = self.pnl_main
		self.pnl_rx = PanelRx()
		self.pnl_rx.set_parent(None)

	def show_panel(self, pnl):
		pnl.set_parent(self._jswidget)  # Attach
		print("switch to panel: {}".format(pnl))
		if self.pnl_active != None:
			self.pnl_active.set_parent(None)  # Detach
		self.pnl_active = pnl

	def show_tx(self):
		self.show_panel(self.pnl_main)

	def show_rx(self):
		self.show_panel(self.pnl_rx)

	def load_config(self, name, pkt):
		self.pnl_source.txt_name.set_text(name)
		self.pnl_tx.set_text(repr(pkt))
		self.set_status(name)

	def save_config(self, name):
		pkt = Ether()/IP(src="1.2.3.4")/UDP(sport=123)/"abc"
		self.pnl_config.save_config(name, pkt)

	def del_config(self, name):
		self.pnl_tx.set_text("")
		self.pnl_config.del_config(name)

	def new_config(self):
		self.pnl_tx.set_text("")

	def set_status(self, status):
		self.lbl_status.set_text(status)

m = flx.launch(ScapyUI)
flx.run()
