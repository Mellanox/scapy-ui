from scapy.all import *
from flexx import flx
from layers.LayerField import *
from panel.PanelDump import *

# Layer detail panel
class PanelLayerDetail(flx.PyWidget):
    def init(self, parent, descs):
        self.fields = []
        self.set_flex(1)
        self._parent = parent
        self.descs = descs
        with flx.VFix():
            self.lbl_title = flx.Label()
            with flx.VBox(flex=4):
                self._cont = flx.FormLayout()
                flx.Label(flex=1)
            self.pnl_dump = PanelDump(flex=6)

    def build_fields(self):
        for name in self.descs.keys():
            with self._cont:
                ScapyTextField(self, name)

    def pkt_load(self, pkt):
        self.pkt = pkt
        # self.lbl_title.set_text(pkt.__class__._name)
        for w in self.fields:
            w.load_pkt(pkt)
        self.on_update() 
        
    # field changed
    def on_update(self):
        self.pnl_dump.show_pkt(self.pkt)
        
    # apply and back
    def on_apply(self):
        self._parent.on_detail_update()

