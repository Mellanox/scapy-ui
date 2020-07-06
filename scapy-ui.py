#!/usr/bin/python3

from scapy.all import *
from flexx import flx, app

from panel.PanelConfig import *
from panel.PanelSource import *
from panel.PanelRx import *
from panel.PanelTx import *
from panel.PanelBrowser import *


logo_html = '<a href="https://scapy.net" target="_blank"><img src="https://scapy.net/assets/img/logo.png" height="96" width="96"/></a>'
title_html = '<a href="https://github.com/Mellanox/scapy-ui" target="_blank" title="Mellanox DPDK China group Hackathon project"><font size="+2">Scapy Web GUI</font></a>'

class FocusBox(flx.VBox):
    @flx.action
    def focus(self):
        self.node.focus()

class ScapyUI(flx.PyWidget):
    CSS = """
        .center {padding: 7px auto; text-align: center;}
        .status {background-color:#f0f0f0;color:#aaaaaa}
        .list {overflow:auto;}
        .link {text-decoration:underline; color:blue;}
        .link:hover {background-color:#EEEEEE;}
        .link:active {text-decoration:none}
        .item {color:blue;}
        .item:hover {background-color:#EEEEEE;}
        .title {background: #eff;}
        .no_border {border: 0px}
        .disabled {opacity: 0.6; cursor: not-allowed;}
        .debug {border: 5px solid green; background: #eee;}
    """    

    def init(self):
        with FocusBox(flex=1, title="Scapy GUI", tabindex=0) as self.pnl_app:
            with flx.HBox():
                flx.Label(html=title_html, css_class="status")
                self.lbl_status = flx.Label(text='...', flex=1, css_class="status")
                self.btn_back = flx.Button(text="Apply & Back", disabled = 1, css_class = "disabled")
            with flx.VBox(flex=1) as self.pnl_root:
                with flx.HSplit(flex=1) as self.pnl_main:
                    with flx.VBox(flex=2):
                        flx.Label(html=logo_html)
                        self.pnl_config = PanelConfig(flex=1)
                    with flx.VBox(flex=8):
                        self.pnl_source = PanelSource() 
                        self.pnl_tx = PanelTx(flex=15)
                self.pnl_active = self.pnl_main
                self.pnl_rx = PanelRx(flex=1)
                self.pnl_rx.set_parent(None)
                self.pnl_browser = PanelBrowser(flex=1)
                self.pnl_browser.set_parent(None)
        self.load_config("test", [["Ether", {}], ["IP", {}], ["Raw", {"load":"'abcd'"}]])
                
    def _show_panel(self, pnl):
        pnl.set_parent(self.pnl_root) #_jswidget)  # Attach
        if self.pnl_active != None:
            self.pnl_active.set_parent(None)  # Detach
        self.pnl_active = pnl
        if getattr(pnl, "_pnl_prev", None):
            self.btn_back.set_disabled(0)
            self.btn_back.set_css_class("")
        else:
            self.btn_back.set_disabled(1)
            self.btn_back.set_css_class("disabled")
        self.pnl_app.focus()
            
    def activate_panel(self, pnl):
        pnl._pnl_prev = self.pnl_active
        self._show_panel(pnl)

    def close_panel(self):
        pnl = self.pnl_active._pnl_prev
        self._show_panel(pnl)
        pnl._pnl_prev = None

    @flx.reaction('btn_back.pointer_click')
    def on_back(self, *events):
        self.pnl_active.on_apply()
        self.close_panel()

    @flx.reaction('pnl_app.key_down')
    def on_key(self, *events):
        e = events[-1]
        if e['key']=='Escape' and len(e['modifiers'])==0:
            if not self.btn_back.disabled:
                self.on_back(events)
        if self.pnl_active == self.pnl_main and len(e['modifiers'])==1 and 'Alt' in e['modifiers']:
            if e['key'] == 's': #send
                self.pnl_tx.pnl_send.send_packet()
            elif e['key'] == 'y': #apply
                self.pnl_source.on_save()
            elif e['key'] == 'w': #new
                self.pnl_source.on_new()
            elif e['key'] == 'n': #sniff
                self.show_rx()

    def show_rx(self):
        self.activate_panel(self.pnl_rx)

    def load_config(self, name, pkt):
        self.pnl_source.txt_name.set_text(name)
        self.pnl_tx.set_pkt_repr(pkt)

    def save_config(self, name):
        pkt = self.pnl_tx.get_pkt_repr()
        self.pnl_config.save_config(name, pkt)

    def del_config(self, name):
        self.pnl_config.del_config(name)

    def set_status(self, status):
        self.lbl_status.set_text(status)

    def _on_load_file(self, file, arg):
        pkts = rdpcap(file)
        self.show_rx()
        self.pnl_rx.load_pkts(pkts)
        self.set_status(f"Loaded file: {file}")

    def _on_save_file(self, file, pkt):
        wrpcap(file, pkt)
        self.set_status(f"Saved to file: {file}")

    def load_pcap(self):
        self.pnl_browser.set_callback(self._on_load_file)
        self.activate_panel(self.pnl_browser)

    def save_pcap(self, pkt):
        self.pnl_browser.set_callback(self._on_save_file, pkt)
        self.activate_panel(self.pnl_browser)

if __name__ == '__main__':
    if sys.argv[-1] in ["--help","-h"]:
        print("""
        Start Scapy web GUI in server mode which support multiple users.
        Please open URL in broswer Chrome or Firefox
        
        Options:
            --flexx-hostname=<host> Host/IP to listen on
            --flexx-port=<port>     Port number to listen on
            --app:                  Start as application single user mode, quit once page close.
            --help(-h)              Show this help
            """)
    elif sys.argv[-1] == "--app":
        flx.launch(ScapyUI)
        flx.run()
    else:
        app.serve(ScapyUI)
        app.start()
