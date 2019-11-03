from scapy.all import *
from flexx import flx
import configparser
import os

class PanelSource(flx.PyWidget):
    def init(self):
        with flx.HFix():
            flx.Label(text="Name: ", flex=2)
            self.txt_name = flx.LineEdit(flex=16)
            self.btn_save = flx.Button(text='Appl(y)', flex=2)
            self.btn_new = flx.Button(text='Ne(w)', flex=2)
            self.btn_del = flx.Button(text='Delete', flex=2)
        self.on_name(None)

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
        self.root.load_config("", None)

    @flx.reaction('txt_name.text')
    def on_name(self, *events):
        if len(self.txt_name.text.strip()) == 0:
            self.btn_save.set_disabled(1)
            self.btn_save.set_css_class("disabled")
            self.btn_del.set_disabled(1)
            self.btn_del.set_css_class("disabled")
        else:
            self.btn_save.set_disabled(0)
            self.btn_save.set_css_class("")
            self.btn_del.set_disabled(0)
            self.btn_del.set_css_class("")
            

