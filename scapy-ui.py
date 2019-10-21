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
					with flx.HBox() as pnl_source:
						flx.Label(text="Name: ")
						self.txt_name = flx.LineEdit(text="test", flex=1)
						self.btn_save = flx.Button(text='Save')
						self.btn_new = flx.Button(text='New')
						self.btn_del = flx.Button(text='Delete')
					self.pnl_tx = flx.Label(text='PanelTx', flex=10)
			self.lbl_status = flx.Label(text='...')
		self.pnl_rx = flx.Label(text='PanelRx')
		self.pnl_rx.set_parent(None)

	@flx.reaction('btn_save.pointer_click')
	def on_save(self, *events):
		pkt = Ether()/IP(src="1.2.3.4")/UDP(sport=123)/"abc"
		self.pnl_config.save_config(self.txt_name.text, pkt)

	@flx.reaction('btn_del.pointer_click')
	def on_del(self, *events):
		self.pnl_config.del_config(self.txt_name.text)
		self.pnl_tx.set_text("")

	@flx.reaction('btn_new.pointer_click')
	def on_new(self, *events):
		self.txt_name.set_text("")
		self.pnl_tx.set_text("")

	def show_rx(self):
		self.pnl_rx.set_parent(self.root)  # Attach
		self.pnl_main.set_parent(None)  # Detach

	def show_tx(self, name, pkt):
		self.pnl_main.set_parent(self.root)
		self.pnl_rx.set_parent(None)
		self.txt_name.set_text(name)
		self.pnl_tx.set_text(repr(pkt))
		self.set_status(name)

	def set_status(self, status):
		self.lbl_status.set_text(status)

m = flx.launch(ScapyUI)
flx.run()
