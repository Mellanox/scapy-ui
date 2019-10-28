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
from panel.PanelDump import *
from panel.PanelSend import *

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
    CSS = """
    .flx-PanelLayers {
        text-align: center;
        padding: 5px;
        border-radius: 5px;
        font-family:Consolas, "Times New Roman", Times, serif;
        font-size: 1em;
    }
    """
    def init(self):
        with ui.HBox(css_class="flx-PanelLayers"):
            flx.Label(flex=4)
            for layer in layers.keys():
                LayerButton(layer, flex=1)
            flx.Label(flex=4)

class PanelTx(flx.PyWidget):
    def init(self):
        self.layer_list = []
        with ui.VFix(flex=18):
            PanelLayers(css_class="title")
            with ui.VSplit(flex=1):
                self._cont = flx.VFix(flex=0)
                self.pnl_dump = PanelDump(0, flex=1)
            PanelSend()

    def get_pkt(self):
        pkt = None
        for w in self.layer_list:
            copy = w.pkt.copy()
            if pkt:
                pkt.add_payload(copy)
            else:
                pkt = copy
        return pkt
        
    def show_pkt(self):
        self.pnl_dump.show_pkt(self.get_pkt())

    def add_layer(self, pkt):
        pkt.remove_payload()
        cls = layers.get(type(pkt), None)
        if cls != None:
            with self._cont:
                w = cls()
                w.pkt_load(pkt)
                self.layer_list.append(w)
        else: 
            self.root.set_status("layer {} not defined".format(type(pkt)))

    def set_pkt(self, pkt):
        for w in self.layer_list:
            w.set_parent(None)
        self.layer_list = []
        while pkt:
            next = pkt.payload
            self.add_layer(pkt)
            pkt = next
        self.show_pkt()

    def add_payload(self, payload):
        self.add_layer(payload)
        self.show_pkt()

    def remove_layer(self, layer):
        self.layer_list.remove(layer)
        layer.set_parent(None)
        self.show_pkt()
          
#q=flx.App(QuickEditPanel);q.serve('');flx.start()

