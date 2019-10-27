from scapy.all import *
from flexx import flx

class FieldDesc():
    placeholder=None
    autocomp=None
    def __init__(self, title, type=str, autocomp=None, placeholder=None):
        self.title = title
        self.type = type
        self.autocomp = autocomp
        self.palceholder = placeholder

class PortDesc(FieldDesc):
    def __init__(self, title):
        super().__init__(title, int)
        self.autocomp = ("1","22","80", "8080","[1,4] #2", "(1,4) #4", "range(1,4) #3", "[(1,4),5,6] #5")
    
class ScapyTextField(flx.PyWidget):
    pkt = None
    def init(self, parent, name, flex=1):
        self._parent = parent
        self.name = name
        self.desc = parent.descs[name]
        with parent._cont:
            self.w = flx.LineEdit(flex=flex, title=self.desc.title)
        self._parent.fields.append(self)
        if self.desc.placeholder:
            self.w.set_placeholder_text(self.desc.placeholder)
        if self.desc.autocomp:
            self.w.set_autocomp(self.desc.autocomp)
    
    @flx.action
    def load_pkt(self, pkt):
        self.pkt = pkt
        v = pkt.fields.get(self.name,None)
        if type(v) == Net:
            v = v.repr
        elif type(v) == int:
            v = str(v)
        elif v == None:
            v = ""
        elif type(v) == str:
            pass
        else:
            v = repr(v)
        self.w.set_text(v)
        
    @flx.reaction('w.user_text')
    def update_pkt(self, *events):
        if not self.pkt:
            return
        text = events[-1]['new_value'].strip()
        try:
            if len(text):
                if self.desc.type != str:
                    text = eval(text)
                self._parent.pkt.setfieldval(self.name, text)
            else:
                self._parent.pkt.fields.pop(self.name, None)
            self._parent.on_update()
        except Exception as e:
            self.root.set_status(str(e))
        else:
            self.root.set_status("")
    
class MacField(ScapyTextField):
    def init(self, parent, name, flex=1):
        super().init(parent, name, flex)
        

# Layer detail panel
class PanelLayer(flx.PyWidget):
    def init(self, parent, descs):
        print(parent)
        self.fields = []
        self.set_flex(1)
        self._parent = parent
        self.descs = descs
        with flx.VBox(flex=1):
            self.lbl_title = flx.Label()
            with flx.VBox():
                self._cont = flx.FormLayout()
            flx.Label()
            self.lbl_scapy = flx.MultiLineEdit(flex=5)
            flx.Label()
            self.lbl_hex = flx.Label(wrap=1, flex=5)

    def build_fields(self):
        for name in self.descs.keys():
            with self._cont:
                ScapyTextField(self, name)

    def pkt_load(self, pkt):
        self.pkt = pkt
        self.lbl_title.set_text(pkt.__class__._name)
        for w in self.fields:
            w.load_pkt(pkt)
        self.on_update() 
        
    # field changed
    def on_update(self):
        self.lbl_scapy.set_text(self.pkt.show(dump=True))
        self.lbl_hex.set_text(hexdump(self.pkt, dump=True))
        
    # apply and back
    def on_apply(self):
        self._parent.on_detail_update()

        
class LayerBase(flx.PyWidget):
    scapy = flx.StringProp(settable=True)
    hex = flx.StringProp(settable=True)
    def init(self, descs={}, cls_detail=PanelLayer):
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
            if self.cls_detail == PanelLayer: 
                pnl = self.cls_detail(self, self.descs)
                pnl.build_fields()
            else:
                pnl = self.cls_detail(self)
        pnl.pkt_load(self.pkt)
        self.root.show_panel(pnl)
