from scapy.all import *
from flexx import flx
from panel.PanelDump import *
from layers.LayerField import *
from util.ScapyUtil import *

# Abstract class of packet edit.
class PanelProtocolAbstract(flx.PyWidget):
    def init(self, descs):
        self.descs = descs #map of field scriptor
        self.fields = [] #map of widgets
        self.field_reprs = None  # map of value repr

    def pkt_load_repr(self, pkt, reprs):
        self.pkt = pkt
        self.field_reprs = reprs;
        link_layer(self.lbl_title, type(pkt))
        self.pkt_load_fields_repr()

    def pkt_load_fields_repr(self):
        for w in self.fields:
            w.load_pkt_repr() 

    # get field repr: {a:'x',b:1}
    def get_fields_repr(self):
        return self.field_reprs

    def get_pkt_repr(self):
        list = [(type(self.pkt).__name__, self.get_fields_repr())]
        return list

# Layer detail panel
class PanelProtocolDetail(PanelProtocolAbstract):
    def init(self, parent, descs):
        super().init(descs)
        self._parent = parent
        with flx.VBox(flex=1):
            self.lbl_title = flx.Label(css_class="center", text="protocol")
            with flx.VSplit(flex=1):
                self._cont = flx.FormLayout()
                self.pnl_dump = PanelDump(flex=1)

    # build input widget for all fields
    def build_fields(self):
        for (name, desc) in self.descs.items():
            with self._cont:
                ScapyTextField(self, name, 1, desc.widget)
        
    def pkt_load_repr(self, pkt, reprs):
        super().pkt_load_repr(pkt, reprs)
        self.on_update() 
        
    # field changed
    def on_update(self):
        self.pnl_dump.show_pkt(self.pkt, self.get_pkt_repr())
        
    # apply and back
    def on_apply(self):
        self._parent.on_detail_update()


class PanelProtocolRow(PanelProtocolAbstract):
    def init(self, descs, cls_detail=PanelProtocolDetail):
        super().init(descs)
        self.cls_detail = cls_detail
        with flx.HFix():
            self.lbl_title = flx.Label(flex=4)
            self._cont = flx.HFix(flex=42)
            self.btn_detail = flx.Button(text="...", flex=2, disabled = not cls_detail)
            self.btn_remove = flx.Button(text="-", flex=1)
            
    # detail panel changed packet
    def on_detail_update(self):
        self.pkt_load_fields_repr() 
        self.on_update()
    
    @flx.reaction('btn_detail.pointer_click')
    def on_detail(self, *events):
        with self.root.pnl_root:
            if self.cls_detail == PanelProtocolDetail: 
                pnl = self.cls_detail(self, self.descs, flex=1)
                pnl.build_fields()
            else:
                pnl = self.cls_detail(self, flex=1)
        pnl.pkt_load_repr(self.pkt, self.field_reprs)
        self.root.activate_panel(pnl)

    @flx.reaction('btn_remove.pointer_click')
    def on_remove(self, *events):
        self.root.pnl_tx.remove_layer(self)
    
    # field changed, update parent UI
    def on_update(self):
        self.root.pnl_tx.show_pkt()
            

