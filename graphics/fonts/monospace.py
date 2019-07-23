from PyQt5.QtGui import QFont


class Monospace(QFont):
	def __init__(self, parent=None):
		super(Monospace, self).__init__(parent)

		self.setFamily("Monospace")
