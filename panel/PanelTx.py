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
        
    # get expr of pkt being edit: Ehter(src="2", type=1)/IP()
    def get_pkt_repr(self):
        list = []
        for w in self.layer_list:
            list.append((w.pkt.name, w.get_field_repr()))
        return list

    # get string expr of pkt being edit: Ehter(src="2", type=1)/IP()
    def get_repr_str(self):
        list_pkt_repr = self.get_pkt_repr()
        print(list_pkt_repr)
        list_pkt_str = []
        for (cls, map) in list_pkt_repr:
            list_field_str = []
            for (k,v) in map.items():
                list_field_str.append(k + "=" + v)
            list_pkt_str.append(cls + "(" + ",".join(list_field_str) + ")")
        return "/".join(list_pkt_str)

    def show_pkt(self):
        self.pnl_dump.show_pkt(self.get_pkt(), self.get_repr_str())

    def add_layer(self, pkt):
        pkt.remove_payload()
        cls = layers.get(type(pkt), None)
        if cls != None:
            with self._cont:
                w = cls()
                w.pkt_load(pkt)
                self.layer_list.append(w)
        else: 
            self.root.set_status(f"layer {type(pkt)} not defined")

    def set_pkt(self, pkt):
        self._cont.set_parent(None)
        for w in self.layer_list:
            w.set_parent(None)
        self.layer_list = []
        while pkt:
            next = pkt.payload
            self.add_layer(pkt)
            pkt = next
        self._cont.set_parent(self.__cont)
        self.show_pkt()

    def add_payload(self, payload):
        self.add_layer(payload)
        self.show_pkt()

    def remove_layer(self, layer):
        self.layer_list.remove(layer)
        layer.set_parent(None)
        self.show_pkt()
          
#q=flx.App(QuickEditPanel);q.serve('');flx.start()

