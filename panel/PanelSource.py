from scapy.all import *
from flexx import flx
import configparser
import os

class PanelSource(flx.PyWidget):
	def init(self):
		with flx.HFix():
			flx.Label(text="Name: ", css_class="title", flex=2)
			self.txt_name = flx.LineEdit(flex=16)
			self.btn_save = flx.Button(text='Apply', flex=2)
			self.btn_new = flx.Button(text='New', flex=2)
			self.btn_del = flx.Button(text='Delete', flex=2)

	@flx.reaction('btn_save.pointer_click')
	def on_save(self, *events):
		txt = self.txt_name.text.strip()
		if len(txt):
			self.root.save_config(txt)

	@flx.reaction('btn_del.pointer_click')
	def on_del(self, *events):
		txt = self.txt_name.text.strip()
		if len(txt):
			self.root.del_config(txt)

	@flx.reaction('btn_new.pointer_click')
	def on_new(self, *events):
		self.txt_name.set_text("")
		self.root.new_config()

