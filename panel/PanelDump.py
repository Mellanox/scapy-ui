from flexx import flx, ui
import psutil
from enum import IntEnum
from scapy.all import *

class PanelDump(ui.PyWidget):
    CSS = """
    .pkt_dump {
        font-family:Consolas, "Times New Roman", Times, serif;
        font-size: 1em;
        background-color:#f5f5f5;color:#aaaaaa
    }
    """
    def init(self, v=0):
        self.pkt = None
        with ui.VBox():
            with ui.HBox():
                self.lbl_repr = flx.LineEdit(flex=1, css_class="pkt_dump", disabled=1)
                self.btn_toggle = flx.Button(text="-")
                self.btn_save = flx.Button(text='save pcap')
            with ui.VBox(flex=1) as self._cont:
                with ui.VSplit(flex=1, parent=None) as self.splt_v:
                    pass
                with ui.HSplit(flex=1) as self.splt_h:
                    self.txt_show = ui.MultiLineEdit(css_class="pkt_dump", flex=4)
                    self.txt_hex = ui.MultiLineEdit(css_class="pkt_dump", flex=6)
            self.splt = self.splt_h
            self.toggle_layout(v)    

    @flx.reaction('btn_toggle.pointer_click')
    def on_toggle_layout(self, *events):
        self.toggle_layout(1 if self.splt == self.splt_h else 0)
        
    def toggle_layout(self, v):
        self.splt.set_parent(None)
        self.splt = self.splt_v if v else self.splt_h
        self.splt.set_parent(self._cont)
        self.txt_show.set_parent(self.splt)
        self.txt_hex.set_parent(self.splt)
        self.txt_show.set_flex(6 if v else 4)
        self.txt_hex.set_flex(4 if v else 6)
        self.btn_toggle.set_text("||" if v else "=")
            
    def show_pkt(self, pkt, rep=None):
        self.pkt = pkt
        if pkt:
            self.lbl_repr.set_text(rep if rep else repr(pkt))
            self.txt_show.set_text(pkt.show(dump=True))
            self.txt_hex.set_text(hexdump(pkt, dump=True))
            self.btn_save.set_disabled(0)
            self.btn_save.set_css_class("")
        else:
            self.lbl_repr.set_text("")
            self.txt_show.set_text("")
            self.txt_hex.set_text("")
            self.btn_save.set_css_class("disabled")
            self.btn_save.set_disabled(1)
            
    @flx.reaction('btn_save.pointer_click')
    def on_save(self, *events):
        self.root.save_pcap(self.pkt)
        