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
    }
    """
    def init(self):
        with ui.VBox():
            with ui.HBox():
                self.lbl_repr = flx.Label(flex=1, css_class="title")
                self.btn_pcap = flx.Button(text='save pcap')
            with ui.HSplit(flex=1):
                self.txt_show = ui.MultiLineEdit(css_class="pkt_dump", flex=1)
                self.txt_hex = ui.MultiLineEdit(css_class="pkt_dump", flex=1)
    
    def show_pkt(self, pkt):
        if pkt:
            self.lbl_repr.set_text(repr(pkt))
            self.txt_show.set_text(pkt.show(dump=True))
            self.txt_hex.set_text(hexdump(pkt, dump=True))
        else:
            self.lbl_repr.set_text("")
            self.txt_show.set_text("")
            self.txt_hex.set_text("")

