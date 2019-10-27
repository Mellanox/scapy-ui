from flexx import flx, ui
import psutil
from enum import IntEnum
from scapy.all import *

class PanelDump(ui.PyWidget):
    CSS = """
    .pkt_dump {
        text-align: left;
        min-width: 10px;
        min-height: 10px;
        padding: 5px;
        border: 2px solid black;
        border-radius: 5px;
        font-family:Consolas, "Times New Roman", Times, serif;
        font-size: 1em;
    }
    """
    def init(self):
        self.pkt = None
        with ui.VBox():
            with ui.HBox():
                self.lbl_repr = flx.LineEdit(flex=1, css_class="title", disabled=1)
                self.btn_save = flx.Button(text='save pcap', disabled=lambda: self.pkt == None)
            with ui.HSplit(flex=1):
                self.txt_show = ui.MultiLineEdit(css_class="pkt_dump", flex=4)
                self.txt_hex = ui.MultiLineEdit(css_class="pkt_dump", flex=6)
    
    def show_pkt(self, pkt):
        self.pkt = pkt
        if pkt:
            self.lbl_repr.set_text(repr(pkt))
            self.txt_show.set_text(pkt.show(dump=True))
            self.txt_hex.set_text(hexdump(pkt, dump=True))
        else:
            self.lbl_repr.set_text("")
            self.txt_show.set_text("")
            self.txt_hex.set_text("")

    @flx.reaction('btn_save.pointer_click')
    def on_save(self, *events):
        self.root.save_pcap(self.pkt)
        