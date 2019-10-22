from flexx import flx, ui
from enum import IntEnum
from scapy.all import *
from layers.PanelIP import *
from layers.PanelEther import *
from layers.PanelUDP import *
from layers.PanelTCP import *
from layers.PanelVXLAN import *
from layers.PanelRaw import *

class Eline(flx.PyWidget): 

    CSS = """
    .flx-Eline {
        line-length:22px;
        background-color:white;
        opacity:1;
    }
    """

    def init(self):
        with ui.HFix():
            self.beth = ui. Button(text='ether', flex=1)
            self.bvlan = ui. Button(text='vlan', flex=1)
            self.bip4 = ui. Button(text='ip4', flex=1)
            self.bip6 = ui. Button(text='ipv6', flex=1)
            self.budp = ui. Button(text='udp', flex=1)
            self.btcp = ui. Button(text='tcp', flex=1)
            self.bvxlan = ui. Button(text='vxlan', flex=1)
            #self.bmpls = ui. Button(text='mpls', flex=1)
            self.bpload = ui. Button(text='payload', flex=1)
        self._map = {self.beth: Ether, self.bip4: IP, self.budp:UDP, self.btcp:TCP, self.bvxlan:VXLAN, self.bpload:Raw}

    @flx.reaction('beth.pointer_click', 'bip4.pointer_click', 'budp.pointer_click', 'btcp.pointer_click',
            'bvxlan.pointer_click', 'bpload.pointer_click', 'bip6.pointer_click', 'bvlan.pointer_click')
    def _check_changed(self, *events):
        cls = self._map.get(events[-1].source, None)
        print(cls)
        if cls:
            if self.root.pnl_tx.pkt != None:
                pkt = self.root.pnl_tx.pkt
                pkt.add_payload(cls())
            else:
                pkt = cls()
            self.root.pnl_tx.set_packet(pkt)
        else:
            self.root.set_status("Not Supported")


class EDP(flx.PyWidget):
    CSS = """
    .flx-EDP {
        text-align: left;
        min-width: 10px;
        min-height: 10px;
        padding: 5px;
        border: 2px solid black;
        border-radius: 5px;
    }
    """
    def init(self):
      with flx.HFix():
        self.lb = ui.Label(wrap=1, css_class="flx-EDP")

    def set_dp(self, pkt):
        self.lb.set_text(pkt)

class ERAW(ui.PyWidget):
    def init(self):
      with ui.VFix():
        with ui.HFix(flex=1):
            self.vd = flx.Label(text='valid/invalid', flex=2)
            self.ept1 = flx.Label(text=' ', flex=15)
            self.hex = flx.Label(text='hex', flex=1)
            self.pcap = flx.Label(text='save pcap', flex=2)
        self.dp = EDP(flex=20)

class EditDetail(flx.PyWidget):
    def init(self):
        with ui.VBox():
            self.el = Eline()
            with ui.VBox(flex=1) as self._root:
                self.ee = LayerEther(flex=1)
                self.eip4 = LayerIP(flex=1)
                self.eudp = LayerUDP(flex=1)
                self.etcp = LayerTCP(flex=1)
                self.evxlan = LayerVXLAN(flex=1)
                self.eei = LayerEther(flex=1)
                self.eip4i = LayerIP(flex=1)
                self.eudpi = LayerUDP(flex=1)
                self.etcpi = LayerTCP(flex=1)
                self.raw = LayerRaw(flex=1)
            self.eraw = ERAW(flex=10)

class ESend(ui.VBox):
    def init(self):
        with ui.HFix():
            self.lp = ui.Label(text="Port:", flex=2)
            self.combo = ui.ComboBox(editable=False, options=('eth1', 'eth2'),selected_key='eth1', flex=2)
            self.lept1 = ui.Label(text=" ", flex=3)
            self.lc = ui.Label(text='Count', flex=2)
            self.lcv = ui.LineEdit(placeholder_text='1', flex=2)
            self.lept2 = ui.Label(text=" ", flex=3)
            self.ll = ui.Label(text='Interval/ms', flex=3)
            self.llv = ui.LineEdit(placeholder_text='100', flex=2)
            self.lept3 = ui.Label(text=" ", flex=3)
            self.snd_btn = ui.Button(text='Send', flex=2)

    @flx.reaction('snd_btn.pointer_click')
    def _send_packet(self, *events):
        print("Will send a packet")
        #sendp(packets,iface='eth0',count=1)

class PanelTx(flx.PyWidget):
    def init(self):
        with ui.VFix(flex=20):
            self.detl = EditDetail(flex=20)
            self.snd = ESend(flex=2)
        self.outer_map = {Ether:self.detl.ee, IP:self.detl.eip4, UDP:self.detl.eudp, TCP:self.detl.etcp, VXLAN:self.detl.evxlan, Raw:self.detl.raw}
        self.inner_map = {Ether:self.detl.eei, IP:self.detl.eip4i, UDP:self.detl.eudpi, TCP:self.detl.etcpi, Raw:self.detl.raw}
        self.all_list = []
        self.all_list += self.outer_map.values()
        self.all_list += self.inner_map.values()

    def set_packet(self, pkt):
        print(type(pkt))
        self.pkt = pkt
        self.on_packet_update()
        for layer in self.all_list:
            layer.pkt_load(None)
        outer = 1
        while pkt:
            if outer:
                layer = self.outer_map.get(type(pkt), None)
            else:
                layer = self.inner_map.get(type(pkt), None)
            if layer:
                layer.pkt_load(pkt)
            else: 
                print("layer {} not defined".format(type(pkt)))
            if type(pkt) == VXLAN:
                outer = 0
            pkt = pkt.payload
      
    def on_packet_update(self):
        self.detl.eraw.dp.set_dp(repr(self.pkt))
        

#q=flx.App(QuickEditPanel);q.serve('');flx.start()

