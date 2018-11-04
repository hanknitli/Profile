from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLineEdit


class SearchLineEdit(QLineEdit):
	def __init__(self, parent=None):
		super(SearchLineEdit, self).__init__(parent)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()