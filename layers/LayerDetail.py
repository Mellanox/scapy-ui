from scapy.all import *
from flexx import flx
from layers.LayerField import *
from panel.PanelDump import *
from util.ScapyUtil import *

# Layer detail panel
class PanelLayerDetail(flx.PyWidget):
    def init(self, parent, descs):
        self.fields = []
        self.set_flex(1)
        self._parent = parent
        self.descs = descs
        self.lbl_title = flx.Label(css_class="center")
        with flx.VSplit():
            self._cont = flx.FormLayout()
            self.pnl_dump = PanelDump(flex=1)
        
    def build_fields(self):
        for (name, desc) in self.descs.items():
            with self._cont:
                ScapyTextField(self, name, 1, desc.widget)

    def pkt_load(self, pkt):
        self.pkt = pkt
        link_layer(self.lbl_title, type(pkt))
        for w in self.fields:
            w.load_pkt(pkt)
        self.on_update() 
        
    # field changed
    def on_update(self):
        self.pnl_dump.show_pkt(self.pkt)
        
    # apply and back
    def on_apply(self):
        self._parent.on_detail_update()

