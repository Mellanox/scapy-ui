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
    def init(self):
        with ui.HBox():
            for layer in layers.keys():
                LayerButton(layer, flex=1)
            flx.Label(flex=20)

class PanelTx(flx.PyWidget):
    def init(self):
        self.pkt = None
        self.layer_list = []
        with ui.VFix(flex=18):
            PanelLayers(css_class="title")
            with flx.VBox(flex=7):
                self._cont = flx.VBox()
                flx.Label(flex=1)
            self.pnl_dump = PanelDump(flex=11)
            PanelSend()

    def show_pkt(self):
        self.pnl_dump.show_pkt(self.pkt)

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

    def remove_layer(self, layer):
        pkt = self.pkt
        if pkt == layer:
            pkt = None
        else:
            while pkt.payload != layer:
                pkt = pkt.payload
            pkt.remove_payload()
            pkt.add_payload(layer.payload)
        self.set_pkt(pkt)
          
#q=flx.App(QuickEditPanel);q.serve('');flx.start()

