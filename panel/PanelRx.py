from flexx import flx, ui, event
from scapy.all import AsyncSniffer
from scapy.utils import hexdump
from time import time

import psutil
import asyncio
import psutil


p_list = []
ifname_list = []

class ListLabel(flx.PyWidget):
    idx = 0
    def init(self, text, idx):
        self.label = flx.Label(text = text, flex = 1, css_class="item")
        self.idx = idx

    @flx.reaction('label.pointer_click')
    def on_click(self, *events):
        relay.pkt_detail(self.idx)
        relay.pkt_hexdump(self.idx)

    def dispose(self):
        self.label.dispose()

class Relay(flx.Component):

    txt_packet = ''
    prev_idx = 0
    curr_idx = 0
    summary_txt = ''
    detail_txt = ''
    hexdump_txt = ''

    def init(self):
        self.sniffer = None
        self.ifname = list(psutil.net_if_addrs().keys())
        self.refresh()

    def sniff_start(self, ifname):
        p_list[:] = []
        self.summary_txt = ''
        self.detail_txt = ''
        self.hexdump_txt = ''
        self.prev_idx = 0
        self.curr_idx = 0
        self.sniffer = AsyncSniffer(iface=ifname, prn=lambda x:p_list.append(x))
        self.sniffer.start()

    def sniff_stop(self):
        self.sniffer.stop()

    def print_packet(self):
        self.curr_idx = len(p_list)
        self.summary_txt = ''
        for i in range(self.prev_idx, self.curr_idx):
            self.summary_txt += p_list[i].summary()
            if i is not self.curr_idx - 1:
                self.summary_txt += '\n'
        self.prev_idx = self.curr_idx
        return self.summary_txt

    def pkt_detail(self, idx):
        if p_list[idx]:
            self.detail_txt = p_list[idx].show(dump=True)
        else:
            self.detail_txt = ''

    def pkt_hexdump(self, idx):
        if p_list[idx]:
            self.hexdump_txt = hexdump(p_list[idx], dump=True)
        else:
            self.hexdump_txt = ''

    @flx.emitter
    def system_info(self):
        return dict(packets=self.print_packet(),
                    hexdump_txt=self.hexdump_txt,
                    detail_txt=self.detail_txt)

    def refresh(self):
        self.system_info()
        asyncio.get_event_loop().call_later(0.5, self.refresh)


# Create global relay
relay = Relay()

class PanelRx(flx.PyWidget):

    def init(self):
        with flx.VBox():
            self.root.set_status('Sniffing')
            with flx.HBox():
                self.iface=flx.ComboBox(options=relay.ifname, flex=2)
                self.start_stop=flx.Button(text="start", flex=1)
                flx.Label(text="", flex=6)
            self.view = PanelRxView(flex=1)

    @event.reaction
    def update_iface(self):
        if self.iface.selected_index is not None:
            self.ifname = self.iface.text

    @event.reaction('start_stop.pointer_click')
    def _start_stop_clicked(self, *events):
        if self.start_stop.text == "start":
            self.view.clear_info()
            relay.sniff_start(self.ifname)
            self.start_stop.set_text('stop')
        else:
            relay.sniff_stop()
            self.start_stop.set_text('start')

    @relay.reaction('system_info')  # note that we connect to relay
    def _push_info(self, *events):
        if not self.session.status:
            return relay.disconnect('system_info:' + self.id)
        for ev in events:
            self.view.update_info(dict(packets=ev.packets,
                                       hexdump_txt=ev.hexdump_txt,
                                       detail_txt=ev.detail_txt))

    def load_pkts(self, pkts):
        p_list[:] = pkts
        msg = relay.print_packet()
        self.view.add_labels(msg)

class PanelRxView(flx.PyWidget):
    CSS = """
        .detail {boarder: solid green 3px; background:white;}
    """

    labels = []
    label_idx = 0

    def init(self):
        with flx.HSplit():
            with flx.VBox(flex=1):
                self.summary = flx.GroupWidget(title="Received Packets", flex=1, css_class="list")
            with flx.VBox(flex=1):
                with flx.GroupWidget(css_class="list", flex=6, title="Detail"):
                    with flx.VBox(flex=1):
                        self.detail = flx.MultiLineEdit(flex=1)
                with flx.GroupWidget(css_class="list", flex=4, title="hexdump"):
                    self.hexdump = flx.Label(flex=1)
                    self.hexdump.set_wrap(2)
                    self.hexdump.set_css_class("detail")

    def update_info(self, info):
        if info['packets']:
            self.add_labels(info['packets'])
        if info['hexdump_txt']:
            line = '<pre><code>' + info['hexdump_txt'] + '</ code></ pre>'
            self.hexdump.set_html(line)
        if info['detail_txt']:
            self.detail.set_text(info['detail_txt'])

    def add_labels(self, msg):
        with self.summary:
            for l in msg.splitlines():
                self.add_one_label(l)

    def add_one_label(self, msg):
        self.labels.append(ListLabel(msg, self.label_idx))
        self.label_idx += 1

    def clear_labels(self):
        for l in self.labels:
            l.dispose()
        self.labels.clear()
        self.label_idx = 0
        self.hexdump.set_text('')
        self.detail.set_text('')

    def clear_info(self):
        #self.summary.clear_summary()
        self.clear_labels()

    def show_detail(self, msg):
        self.detail.set_text(msg)

    def show_hexdump(self, msg):
        self.hexdump.set_text(msg)

if __name__ == '__main__':
    a = flx.App(PanelRx)
    a.serve()
    #m = a.launch('browser')  # for use during development
    flx.start()
