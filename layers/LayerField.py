from scapy.all import *
from flexx import flx


#TODO: generate UI field from Scapy field descriptors.
class FieldDesc():
    placeholder=None
    autocomp=None
    def __init__(self, title, type=str, autocomp=None, placeholder=None, url=None, widget="LineEdit"):
        self.title = title
        self.type = type
        self.autocomp = autocomp
        self.palceholder = placeholder
        self.url = url
        self.widget = widget

class PortDesc(FieldDesc):
    def __init__(self, title):
        super().__init__(title, int)
        self.autocomp = ("1","22","80", "8080","[1,4] #2", "(1,4) #4", "range(1,4) #3", "[(1,4),5,6] #5")
class IpDesc(FieldDesc):
    def __init__(self, title):
        super().__init__(title)
        self.autocomp = ("192.168.0.1","192.168.0.2","192.168.0.1/30",
             "10.0.0.1", "10.0.0.2",
             "0.0.0.0","255.255.255.255")
class MacDesc(FieldDesc):
    def __init__(self, title):
        super().__init__(title)
        self.autocomp = ("00:00:00:00:00:00",
            "00:11:22:33:44:55",
            "66:77:88:99:aa:bb",
            "aa:bb:cc:dd:ee:ff",
            "ff:ff:ff:ff:ff:ff")

class ScapyTextField(flx.PyWidget):
    pkt = None
    def init(self, parent, name, flex=1, widget="LineEdit"):
        self._parent = parent # PanelProtocolAbstract
        self.name = name
        self.desc = parent.descs[name]
        self.text = ""
        with parent._cont:
            if widget == "MultiLineEdit":
                self.w = flx.MultiLineEdit(flex=flex, title=self.desc.title, style="height: 100%; min-height: 200px")
            else:
                self.w = flx.LineEdit(flex=flex, title=self.desc.title)
                if self.desc.placeholder:
                    self.w.set_placeholder_text(self.desc.placeholder)
                if self.desc.autocomp:
                    self.w.set_autocomp(self.desc.autocomp)
        self._parent.fields.append(self)
    
    # load field value from packet
    def load_pkt_repr(self):
        if not self.name in self._parent.field_reprs:
            self.w.set_text("")
            return
        v = self._parent.field_reprs[self.name]
        self.w.set_text(v)
        self.update_pkt_field(v)

    @flx.reaction('w.user_text')
    def update_pkt(self, *events):
        text = events[-1]['new_value']
        rep = text.strip()
        if len(rep):
            self._parent.field_reprs[self.name] = rep
        else:
            self._parent.field_reprs.pop(self.name, None)
        self.update_pkt_field(rep)
        self._parent.on_update()
    
    # set text value of pkt field
    def update_pkt_field(self, text):
        try:
            if text and len(text):
                if self.desc.type != str:
                    val = eval(text, {}, {})
                else:
                    val = text
                self._parent.pkt.setfieldval(self.name, val)
            else:
                self._parent.pkt.fields.pop(self.name, None)
        except Exception as e:
            print(e)
            self.root.set_status(str(e))
        else:
            self.root.set_status("")
    
