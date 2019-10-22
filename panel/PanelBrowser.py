from flexx import flx, ui
from scapy.all import *

class PanelBrowser(flx.PyWidget):
	def init(self):
		with flx.VBox():
			self.browser = flx.FileBrowserWidget()
	
	@flx.reaction('browser.selected')
	def on_select(self, *events):
		file = self.browser.path
		self.root.set_status(file)
		if file.lower().endswith(".pcap"):
			if self._callback:
				self._callback.on_file(file)
		else:
			self.root.set_status("Please select *.pcap file")

	def set_callback(self, callback):
		self._callback = callback

