from flexx import flx, ui, event
from scapy.all import AsyncSniffer
from scapy.utils import hexdump
from time import time

import psutil
import asyncio
import psutil


p_list = []
ifnames = list(psutil.net_if_addrs().keys())

class ListLabel(flx.Widget):
    idx = 0
    def init(self, text, idx):
        self.label = flx.Label(text = text, flex = 1, css_class="item")
        self.idx = idx

    @flx.reaction('label.pointer_click')
    def on_click(self, *events):
        self.update_detail(self.idx)

    @flx.emitter
    def update_detail(self, idx):
        return dict(idx=idx)

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
        if self.sniffer and self.sniffer.running:
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

    def packet_info(self):
        self.curr_idx = len(p_list)
        for i in range(self.prev_idx, self.curr_idx):
            self.emit('packet_info', dict(pkt_summary=p_list[i].summary(),
                                          pkt_detail=p_list[i].show(dump=True),
                                          pkt_hex=hexdump(p_list[i], dump=True)))
        self.prev_idx = self.curr_idx

    def refresh(self):
        self.packet_info()
        asyncio.get_event_loop().call_later(0.5, self.refresh)


# Create global relay
relay = Relay()

class PanelRx(flx.PyWidget):

    def init(self):
        with flx.VBox():
            self.root.set_status('Sniffing')
            with flx.HBox():
                iface = self.root.pnl_config.get_section_config("common", "iface", "lo")
                if ifnames.count(iface) == 0:
                    iface = "lo"
                self.iface=flx.ComboBox(options=ifnames, flex=2, selected_key=iface)
                self.start_stop=flx.Button(text="start", flex=1)
                flx.Label(text="", flex=6)
            self.view = PanelRxView(flex=1)

    @event.reaction('start_stop.pointer_click')
    def _start_stop_clicked(self, *events):
        if self.start_stop.text != "stop":
            self.view.clear_info()
            relay.sniff_start(self.iface.text)
            self.start_stop.set_text('stop')
        else:
            self._stop_sniff()

    def _stop_sniff(self):
        try:
            relay.sniff_stop()
            self.root.pnl_config.set_section_config("common", "iface", self.iface.text)
        except Exception as e:
            self.root.set_status(str(e))
        self.start_stop.set_text('start')

    @relay.reaction('!packet_info')
    def _push_packet(self, *events):
        if not self.session.status:
            return relay.disconnect('packet_info:' + self.id)
        for ev in events:
            self.view.add_pkt(dict(pkt_summary=ev.pkt_summary,
                                   pkt_detail=ev.pkt_detail,
                                   pkt_hex=ev.pkt_hex))

    def load_pkts(self, pkts):
        self.view.clear_info()
        for p in pkts:
            self.view.add_pkt(dict(pkt_summary=p.summary(),
                                   pkt_hex=hexdump(p, dump=True),
                                   pkt_detail=p.show(dump=True)))

    def on_apply(self):
        self._stop_sniff()

class PanelRxView(flx.Widget):
    CSS = """
        .detail {
            boarder: solid green 3px;
            font-size:small;
            word-wrap:break-word;
            overflow: auto;
        }
        .packet_list { overflow: auto; }
        .flx-TreeWidget {
            border: gray solid 1px;
            font-size: small;
        }
        .flx-TreeItem {
            border-top: white solid 1px;
            text-overflow:ellipse;
            white-space:nowrap;
        }
        .flx-TreeItem:hover {
            background-color: #EEEEEE;
        }
        .flx-TreeItem.selected-true {
            background: blue;
            color: white;
        }
        .flx-TreeWidget .flx-TreeItem > .text.hastitle {
            width: 95%;
        }
        .flx-TreeItem > .title {
            background: white;
            color: gray;
        }
    """

    labels = flx.ListProp(settable=True)
    label_idx = flx.IntProp(settable=True)
    packets = flx.ListProp(settable=True)

    def init(self):
        with flx.HSplit():
            with flx.VBox(flex=1):
                self.summary = flx.TreeWidget(flex=1, max_selected=1)
            with flx.VSplit(flex=1):
                with flx.GroupWidget(css_class="list", flex=6, title="Detail"):
                    self.detail = flx.Label(flex=1, css_class="detail")
                    self.detail.set_wrap(2)
                with flx.GroupWidget(css_class="list", flex=4, title="hexdump"):
                    self.hexdump = flx.Label(flex=1, css_class="detail")
                    self.hexdump.set_wrap(1)

    @flx.action
    def add_pkt(self, info):
        self.packets.append(dict(summary=info['pkt_summary'], detail=info['pkt_detail'],
                            hex=info['pkt_hex']))
        self.add_one_label(info['pkt_summary'])

    @flx.action
    def update_info(self, info):
        if info['packets']:
            self.add_labels(info['packets'])
        if info['hexdump_txt']:
            line = '<pre><code>' + info['hexdump_txt'] + '</ code></ pre>'
            self.hexdump.set_html(line)
        if info['detail_txt']:
            line = '<pre><code>' + info['detail_txt'] + '</ code></ pre>'
            self.detail.set_html(line)

    @flx.action
    def add_labels(self, msg):
        with self.summary:
            for l in msg.splitlines():
                self.add_one_label(l)

    @flx.action
    def add_one_label(self, msg):
        with self.summary:
            l = flx.TreeItem(text=msg, title=str(self.label_idx), checked=None)
        self._mutate_labels([l], 'insert', len(self.labels))
        self._mutate_label_idx(self.label_idx + 1)

    @flx.action
    def clear_labels(self):
        for l in self.labels:
            l.dispose()
        self.labels.clear()
        self._mutate_label_idx(0)
        self.hexdump.set_text('')
        self.detail.set_text('')

    @flx.action
    def clear_info(self):
        self.set_packets([])
        self.clear_labels()

    @flx.reaction('summary.children**.checked', 'summary.children**.selected')
    def _update_detail(self, *events):
        e = events[-1]
        id = int(e.source.title)
        self.show_detail(self.packets[id]['detail'])
        self.show_hexdump(self.packets[id]['hex'])

    def show_detail(self, msg):
        msg = '<pre><code>' + msg + '</code></pre>'
        self.detail.set_html(msg)

    def show_hexdump(self, msg):
        msg = '<pre><code>' + msg + '</code></pre>'
        self.hexdump.set_html(msg)


if __name__ == '__main__':
    a = flx.App(PanelRx)
    a.serve()
    #m = a.launch('browser')  # for use during development
    flx.start()
