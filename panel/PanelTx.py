from flexx import flx, ui
from enum import IntEnum
from scapy.all import *
from layers.PanelIP import *

packets = Ether()/IP(dst="11.22.33.44",src="1.2.3.4")/UDP()

class TxItem(IntEnum):
    eth = 0
#    vlan
    ip4 = 1
#    ip6
    vxlan = 2
    ip4i = 3
    tcp = 4
    udp = 5
    gre = 6
#    mpls
    payload = 7
    
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
            self.beth = ui.ToggleButton(text='ether', checked=1, flex=1)
            #self.bip4 = ui.ToggleButton(text='ip4', flex=1)
            #self.bip4i = ui.ToggleButton(text='ip4i', flex=1)
            self.bip6 = ui.ToggleButton(text='ipv6', flex=1)
            self.btcp = ui.ToggleButton(text='tcp', flex=1)
            #self.budp = ui.ToggleButton(text='udp', flex=1)
            self.bvxlan = ui.ToggleButton(text='vxlan', flex=1)
            #self.bvlan = ui.ToggleButton(text='gre', flex=1)
            self.bvlan = ui.ToggleButton(text='vlan', flex=1)
            #self.bmpls = ui.ToggleButton(text='mpls', flex=1)
            self.bpload = ui.ToggleButton(text='payload', checked=1, flex=1)

    @flx.reaction('beth.checked', 'btcp.checked', 'bvxlan.checked', 'bpload.checked', 'bip6.checked', 'bvlan.checked')
    def _check_changed(self, *events):
        packets[0].show()
        if self.beth.checked:
            self.root.pnl_tx.detl.ee.e_src.set_disabled(0)
            self.root.pnl_tx.detl.ee.e_dst.set_disabled(0)
        else:
            self.root.pnl_tx.detl.ee.e_src.set_disabled(1)
            self.root.pnl_tx.detl.ee.e_dst.set_disabled(1)
        if self.btcp.checked:
            self.root.pnl_tx.detl.etcp.prot.set_text("tcp")
        else:
            self.root.pnl_tx.detl.etcp.prot.set_text("udp")
        if self.bvxlan.checked:
            #self.root.pnl_tx.detl.eip4.e_src.set_disabled(0)
            #self.root.pnl_tx.detl.eip4.e_dst.set_disabled(0)
            self.root.pnl_tx.detl.evudp.e_src.set_disabled(0)
            self.root.pnl_tx.detl.evudp.e_dst.set_disabled(0)
            self.root.pnl_tx.detl.evxlan.e_vni.set_disabled(0)
        else:
            #self.root.pnl_tx.detl.eip4.e_src.set_disabled(1)
            #self.root.pnl_tx.detl.eip4.e_dst.set_disabled(1)
            self.root.pnl_tx.detl.evudp.e_src.set_disabled(1)
            self.root.pnl_tx.detl.evudp.e_dst.set_disabled(1)
            self.root.pnl_tx.detl.evxlan.e_vni.set_disabled(1)
        if self.bpload.checked:
            self.root.pnl_tx.detl.epld.payload.set_disabled(0)
        else:
            self.root.pnl_tx.detl.epld.payload.set_disabled(1)
        #if self.bip6.checked:
            #self.root.pnl_tx.detl.eip4.line.set_text('ipv6')
        #else:
            #self.root.pnl_tx.detl.eip4.line.set_text('ipv4')
        if self.bvlan.checked:
            self.root.pnl_tx.detl.evxlan.e_vlan.set_disabled(0)
        else:
            self.root.pnl_tx.detl.evxlan.e_vlan.set_disabled(1)


class EEth(flx.PyWidget):
    def init(self):
      with flx.HFix():
        self.line = flx.Label(text='Ethernet:', flex=2)
        self.e_src = flx.LineEdit(placeholder_text='00:11:22:33:44:55', flex=10)
        self.ar = flx.Label(text='->', flex=1)
        self.e_dst = flx.LineEdit(placeholder_text='00:11:22:33:44:56', flex=10)
        self.bt_dtl = flx.Button(text='...', flex=1)

class EIP4(flx.PyWidget):
    def init(self):
      LayerIP()
###
#      with flx.HFix():
#        self.line = flx.Label(text='ip4:',flex=2)
#        self.e_src = flx.LineEdit(placeholder_text='192.168.1.1', flex=10)
#        self.ar = flx.Label(text='->', flex=1)
#        self.e_dst = flx.LineEdit(placeholder_text='192.168.1.2', flex=10)
#        self.bt_dtl = flx.Button(text='...', flex=1)
###

class EUDP(flx.PyWidget):
    def init(self):
      with flx.HFix():
        self.prot = flx.Label(text='udp:',flex=2)
        self.e_src = flx.LineEdit(placeholder_text='5464', flex=10)
        self.ar = flx.Label(text='->', flex=1)
        self.e_dst = flx.LineEdit(placeholder_text='250', flex=10)
        self.bt_dtl = flx.Button(text='...',flex=1)

class EVXLAN(flx.PyWidget):
    def init(self):
      with flx.HFix():
        self.line = flx.Label(text='vxlan:',flex=2)
        self.line2 = flx.Label(text='VNI:',flex=1)
        self.e_vni = flx.LineEdit(placeholder_text='250', flex=9)
        self.line3 = flx.Label(text='',flex=1)
        self.ar = flx.Label(text='vlan:', flex=2)
        self.e_vlan = flx.LineEdit(placeholder_text='123', flex=8)
        self.bt_dtl = flx.Button(text='...', flex=1)

class EIP4I(flx.PyWidget):
    def init(self):
      with flx.HFix():
        self.line = flx.Label(text='ip4i:', flex=2)
        self.e_src = flx.LineEdit(placeholder_text='192.168.1.1', flex=10)
        self.ar = flx.Label(text='->', flex=1)
        self.e_dst = flx.LineEdit(placeholder_text='192.168.1.2', flex=10)
        self.bt_dtl = flx.Button(text='...', flex=1)

class ETCP(flx.PyWidget):
    def init(self):
      with flx.HFix():
#        self.cb = flx.ComboBox(editable=False, options=('tcp', 'udp'),selected_key='tcp', flex=2)
        self.prot = flx.Label(text='udp:',flex=2)
        self.e_src = flx.LineEdit(placeholder_text='5464',flex=10)
        self.ar = flx.Label(text='->',flex=1)
        self.e_dst = flx.LineEdit(placeholder_text='250',flex=10)
        self.bt_dtl = flx.Button(text='...',flex=1)

class EPLD(flx.PyWidget):
    def init(self):
      with flx.HFix():
       self.line = flx.Label(text='payload:', flex=2)
       self.payload = flx.LineEdit(placeholder_text='ABCD',flex=21)
       self.bt_dtl = flx.Button(text='...',flex=1)

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
        self.lb = ui.Label(wrap=1,text='Ether(src="00:11:22:33:44::55", dst="00:11:22:33:44:66")/IP(src=')

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
        with ui.VFix():
            self.el = Eline(flex=1)
            self.ee = EEth(flex=1)
            self.eip4 = EIP4(flex=1)
            self.evudp = ETCP(flex=1)
            self.evxlan = EVXLAN(flex=1)
            self.eip4i = EIP4I(flex=1)
            self.etcp = ETCP(flex=1)
            self.epld = EPLD(flex=1)
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
 
#q=flx.App(QuickEditPanel);q.serve('');flx.start()

