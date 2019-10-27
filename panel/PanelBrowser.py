from flexx import flx, ui
from scapy.all import *

class PanelBrowser(flx.PyWidget):
    def init(self):
        with flx.VBox(flex=1):
            self.file_browser = flx.FileBrowserWidget(flex=1)
            with flx.HBox():
                flx.LineEdit(text=lambda: self.file_browser.path, flex=8, disabled=1)
                flx.Label(text=" / ")
                self.txt_file = flx.LineEdit(flex=3)
                self.btn_file = flx.Button(flex=1)
    
    @flx.reaction('file_browser.selected')
    def on_select(self, *events):
        file = events[-1].filename
        self.txt_file.set_text(file.split("/")[-1])
        
    @flx.reaction('btn_file.pointer_click')
    def on_file(self, *events):
        file = self.file_browser.path + "/" + self.txt_file.text
        if not file.lower().endswith(".pcap"):
            self.root.set_status("Please select *.pcap file")
            return
        self.root.close_panel()
        self._callback(file, self._arg)

    def set_callback(self, callback, arg = None):
        self._callback = callback
        self._arg = arg
        self.btn_file.set_text("Save" if arg else "Open")
        
    def on_apply(self):
        self._callback = None
        self._arg = None

