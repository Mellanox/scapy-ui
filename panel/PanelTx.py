from flexx import flx, ui
import psutil
from enum import IntEnum
from scapy.all import *
from panel.PanelDump import *
from panel.PanelSend import *
from layers.PanelEther import *
from layers.PanelDot1Q import *
from layers.PanelIP import *
from layers.PanelIPv6 import *
from layers.PanelUDP import *
from layers.PanelTCP import *
from layers.PanelVXLAN import *
from layers.PanelRaw import *
from layers.PanelOthers import *

layers = {Ether:LayerEther, Dot1Q:LayerDot1Q,
          IP:LayerIP, IPv6:LayerIPv6, ARP:LayerARP,
          UDP:LayerUDP, TCP:LayerTCP, ICMP:LayerICMP,
          VXLAN:LayerVXLAN, GRE:LayerGRE,
          Raw:LayerRaw}

class LayerButton(flx.PyWidget):
    def init(self, layer):
        self.layer = layer #protocol class
        self.btn = flx.Label(text=layer._name, css_class="link", flex=1)

    @flx.reaction('btn.pointer_click')
    def on_click(self, *events):
        self.root.pnl_tx.add_layer(self.layer)


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
                with flx.VBox() as self.__cont:
                    self._cont = flx.VFix(flex=1)
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
        
    # get pkt being edit: list of (class, map of fields)
    # [[scapy.layers.l2.Ehter , {"src":"2", "type":1}], [scapy.layers.inet.IP, {}]]
    def get_pkt_repr(self):
        list = []
        for w in self.layer_list:
            list.append(w.get_pkt_repr()[0])
        return list

    def show_pkt(self):
        self.pnl_dump.show_pkt(self.get_pkt(), self.get_pkt_repr())

    # [[cls,field_map{}]]
    def set_pkt_repr(self, pkt):
        self._cont.set_parent(None)
        for w in self.layer_list:
            w.set_parent(None)
        self.layer_list = []
        if pkt:
            for (cls, fields) in pkt:
                self.add_layer_repr(eval(cls), fields)
        self._cont.set_parent(self.__cont)
        self.show_pkt()

    def add_layer_repr(self, pkt_cls, fields):
        cls = layers.get(pkt_cls, None)
        with self._cont:
            w = cls()
            w.pkt_load_repr(pkt_cls(), fields)
            self.layer_list.append(w)

    def add_layer(self, cls):
        self.add_layer_repr(cls, {})
        self.show_pkt()

    def remove_layer(self, layer):
        self.layer_list.remove(layer)
        layer.set_parent(None)
        self.show_pkt()
          
#q=flx.App(QuickEditPanel);q.serve('');flx.start()

