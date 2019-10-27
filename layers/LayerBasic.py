from scapy.all import *
from flexx import flx
from layers.LayerField import *
from layers.LayerDetail import *


class LayerBasic(flx.PyWidget):
    scapy = flx.StringProp(settable=True)
    hex = flx.StringProp(settable=True)
    def init(self, descs={}, cls_detail=PanelLayerDetail):
        self.descs = descs
        self.cls_detail = cls_detail
        self.fields = []
        with flx.HFix():
            self.lbl_title = flx.Label(flex=2)
            self._cont = flx.HFix(flex=21)
            self.btn_detail = flx.Button(text="...", flex=1, disabled = not cls_detail)
            
    @flx.action
    def pkt_load(self, pkt):
        self.pkt = pkt
        self.lbl_title.set_text(pkt.__class__._name)
        self.pkt_load_fields()
        
    def pkt_load_fields(self):
        for w in self.fields:
            w.load_pkt(self.pkt) 
    
    # detail panel changed packet
    def on_detail_update(self):
        self.pkt_load_fields() 
        self.on_update()
    
    # field changed, update parent UI
    def on_update(self):
        self.root.pnl_tx.show_pkt()
            
    @flx.reaction('btn_detail.pointer_click')
    def on_detail(self, *events):
        with self.root.pnl_root:
            if self.cls_detail == PanelLayerDetail: 
                pnl = self.cls_detail(self, self.descs)
                pnl.build_fields()
            else:
                pnl = self.cls_detail(self)
        pnl.pkt_load(self.pkt)
        self.root.show_panel(pnl)
