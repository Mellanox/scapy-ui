from flexx import flx, ui, event
import psutil
from scapy.all import AsyncSniffer

from time import time
import psutil
import asyncio

from flexx import flx

p_list = []
ifname_list = []

class SummaryBox(flx.Label):

    CSS = """
    .flx-SummaryBox {
        overflow-x:scroll;
        overflow-y:scroll;
        background: #e8e8e8;
        border: 1px solid #444;
        margin: 3px;
    }
    """

    def init(self):
        super().init()
        global window
        self._se = window.document.createElement('div')

    def sanitize(self, text):
        self._se.textContent = text
        text = self._se.innerHTML
        self._se.textContent = ''
        return text

    @flx.action
    def add_summary(self, msg):
        #line =  '<pre>' + self.sanitize(msg) + '</ pre>'
        line = '<br />'.join(msg.splitlines())
        self.set_html(self.html + line + '<br />')

    @flx.action
    def clear_summary(self):
        self.set_html('')


class Relay(flx.Component):

    txt_packet = ''
    prev_idx = 0
    curr_idx = 0
    summary_txt = ''
    repr_txt = ''
    hexdump_txt = ''

    def init(self):
        self.sniffer = None
        self.ifname = list(psutil.net_if_addrs().keys())
        self.refresh()

    def sniff_start(self, ifname):
        self.sniffer = AsyncSniffer(iface=ifname, prn=lambda x:p_list.append(x))
        self.sniffer.start()

    def sniff_stop(self):
        self.sniffer.stop()

    def print_packet(self):
        self.curr_idx = len(p_list)
        self.summary_txt = ''
        self.repr_txt = ''
        for i in range(self.prev_idx, self.curr_idx):
            self.summary_txt += p_list[i].summary()
            if i is not self.curr_idx - 1:
                self.summary_txt += '\n'
        self.prev_idx = self.curr_idx
        return self.summary_txt

    @flx.emitter
    def system_info(self):
        return dict(packets=self.print_packet())

    def refresh(self):
        self.system_info()
        asyncio.get_event_loop().call_later(1, self.refresh)


# Create global relay
relay = Relay()

class PanelRx(flx.PyWidget):

    def init(self):
        with flx.VBox(css_class="debug"):
            flx.Label(text='Sniffing')
            with flx.HBox():
                self.iface=flx.ComboBox(options=relay.ifname)
                self.start=flx.Button(text="start")
                self.stop=flx.Button(text="stop")
            self.view = PanelRxView()

    @event.reaction
    def update_iface(self):
        if self.iface.selected_index is not None:
            self.ifname = self.iface.text
            print(self.ifname)

    @event.reaction('start.pointer_click')
    def _start_clicked(self, *events):
        self.view.clear_info()
        relay.sniff_start(self.ifname)

    @event.reaction('stop.pointer_click')
    def _stop_clicked(self, *events):
        relay.sniff_stop()

    @relay.reaction('system_info')  # note that we connect to relay
    def _push_info(self, *events):
        if not self.session.status:
            return relay.disconnect('system_info:' + self.id)
        for ev in events:
            self.view.update_info(dict(packets=ev.packets))


class PanelRxView(flx.PyWidget):

    def init(self):
        with flx.VBox():
            self.summary = SummaryBox(flex=1)

    @flx.action
    def update_info(self, info):
        if info.packets:
            self.summary.add_summary(info.packets)

    @flx.action
    def clear_info(self):
        self.summary.clear_summary()

if __name__ == '__main__':
    a = flx.App(PanelRx)
    a.serve()
    #m = a.launch('browser')  # for use during development
    flx.start()
