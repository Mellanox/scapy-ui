from flexx import flx, ui
import psutil
from enum import IntEnum
from scapy.all import *
from layers.PanelIP import *
from layers.PanelEther import *
from layers.PanelUDP import *
from layers.PanelTCP import *
from layers.PanelVXLAN import *
from layers.PanelRaw import *

layers = {Ether:LayerEther, IP:LayerIP, UDP:LayerUDP, TCP:LayerTCP, VXLAN:LayerVXLAN, Raw:LayerRaw}

class LayerButton(flx.PyWidget):
    def init(self, layer):
        self.layer = layer
        self.btn = flx.Label(text=layer._name, css_class="link", flex=1)

    @flx.reaction('btn.pointer_click')
    def on_click(self, *events):
        layer = self.layer()
        self.root.pnl_tx.add_payload(layer)


class PanelLayers(flx.PyWidget): 
    def init(self):
        with ui.HBox():
            for layer in layers.keys():
                LayerButton(layer, flex=1)
            flx.Label(flex=20)

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
        with ui.VFix():
            with ui.HFix(flex=1):
                self.btn_valid = flx.Label(text='valid/invalid', flex=2)
                flx.Label(flex=15)
                self.btn_hex = flx.ToggleButton(text='hex', flex=1)
                self.btn_pcap = flx.Button(text='save pcap', flex=2)
            self.txt_dump = ui.MultiLineEdit(css_class="pkt_dump", flex=9)

    @flx.reaction('btn_hex.user_checked')
    def on_hex(self, *events):
        checked = events[-1]['new_value']
        self.root.pnl_tx.show_pkt(checked)
    
    def show_pkt(self, pkt, hex):
        if hex == -1:
            hex = self.btn_hex.checked
        if hex:
            msg = hexdump(pkt, dump=True)
        else:
            msg = pkt.show(dump=True)
        self.txt_dump.set_text(msg)
        
class ESend(flx.PyWidget):
    def init(self):
        with ui.VBox():
            with ui.HFix():
                self.ifnames = list(psutil.net_if_addrs().keys())
                self.lp = ui.Label(text="Port:", flex=2)
                self.combo = ui.ComboBox(editable=False, options=self.ifnames, selected_key=self.ifnames[0], flex=2)
                self.lept1 = ui.Label(text=" ", flex=3)
                self.lc = ui.Label(text='Count', flex=2)
                self.lcv = ui.LineEdit(placeholder_text='1', flex=2)
                self.lept2 = ui.Label(text=" ", flex=3)
                self.ll = ui.Label(text='Interval/ms', flex=3)
                self.llv = ui.LineEdit(placeholder_text='100', flex=2)
                self.lept3 = ui.Label(text=" ", flex=3)
                self.snd_btn = ui.Button(text='Send', flex=2)

    @flx.reaction
    def update_iface(self):
        if self.combo.selected_index is not None:
            self.ifname = self.combo.text
            print(self.ifname)

    @flx.reaction('snd_btn.pointer_click')
    def _send_packet(self, *events):
        packet = self.root.pnl_tx.pkt
        sendp(packet, iface=self.ifname, count=1)

class PanelTx(flx.PyWidget):
    def init(self):
        self.pkt = None
        self.layer_list = []
        with ui.VFix(flex=20):
            PanelLayers(flex=1)
            with flx.VBox(flex=7):
                self._cont = flx.VBox()
                flx.Label(flex=1)
            self.pnl_dump = PanelDump(flex=11)
            self.snd = ESend(flex=2)

    def show_pkt(self, hex=-1):
        self.pnl_dump.show_pkt(self.pkt, hex)

    def add_layer(self, pkt):
        cls = layers.get(type(pkt), None)
        if cls != None:
            with self._cont:
                w = cls()
                w.pkt_load(pkt)
                self.layer_list.append(w)
        else: 
            self.root.set_status("layer {} not defined".format(type(pkt)))

    def set_pkt(self, pkt):
        self.pkt=pkt
        for w in self.layer_list:
            w.set_parent(None)
        while pkt:
            self.add_layer(pkt)
            pkt = pkt.payload
        self.show_pkt()

    def add_payload(self, payload):
        if self.pkt != None:
            self.pkt.add_payload(payload)
        else:
            self.pkt = payload
        self.add_layer(payload)
        self.show_pkt()
          
#q=flx.App(QuickEditPanel);q.serve('');flx.start()

