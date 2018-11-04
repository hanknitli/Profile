from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLineEdit, QHBoxLayout, QIcon, QPushButton, QWidget, QToolButton, QLabel


class SearchTree(QWidget):
	def __init__(self, parent=None):
		super(SearchTree, self).__init__(parent)

		self.index = 0  # Set the search index which is used in searching the next occurrence
		self.result = []  # Initialize emtpy list, which will store the search results

		self.searchbar = QLineEdit()
		self.searchbar.setObjectName("SearchTreeBar")
		self.searchbar.setToolTip("Enter the text")

		self.searchnext = QToolButton(self)
		self.searchnext.setIcon(QIcon("resources/Icons/next.png"))
		self.searchnext.setObjectName("SearchTreeNext")
		self.searchnext.setToolTip("Find Next")

		self.searchprevious = QToolButton(self)
		self.searchprevious.setIcon(QIcon("resources/Icons/previous.png"))
		self.searchprevious.setObjectName("SearchTreePrevious")
		self.searchprevious.setToolTip("Find Previous")

		self.matches = QLabel()
		self.matches.setObjectName("SearchTreeMatches")

		searchpane = QHBoxLayout(self)
		searchpane.addWidget(self.searchbar)
		searchpane.addWidget(self.searchnext)
		searchpane.addWidget(self.searchprevious)
		searchpane.addWidget(self.matches)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
		else:
			super(SearchTree, self).keyPressEvent(event)
