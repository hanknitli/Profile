from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLineEdit, QHBoxLayout, QIcon, QPushButton, QWidget, QToolButton


class SearchTree(QWidget):
	def __init__(self, parent=None):
		super(SearchTree, self).__init__(parent)

		self.searchbar = QLineEdit()
		self.searchbar.setObjectName("SearchTreeBar")

		self.searchnext = QToolButton(self)
		self.searchnext.setIcon(QIcon("resources/Icons/next.png"))
		self.searchnext.setObjectName("SearchTreeNext")

		self.searchprevious = QToolButton(self)
		self.searchprevious.setIcon(QIcon("resources/Icons/previous.png"))
		self.searchprevious.setObjectName("SearchTreePrevious")

		searchpane = QHBoxLayout(self)
		searchpane.addWidget(self.searchbar)
		searchpane.addWidget(self.searchnext)
		searchpane.addWidget(self.searchprevious)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
		else:
			super(SearchTree, self).keyPressEvent(event)