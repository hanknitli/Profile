from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QToolButton, QLabel, QHBoxLayout, QLineEdit


class SearchTree(QWidget):
	def __init__(self, parent=None):
		super(SearchTree, self).__init__(parent)

		self.index = 0  # Set the search index which is used in searching the next occurrence
		self.result = []  # Initialize emtpy list, which will store the search results

		self.searchicon = SearchIcon(self)
		self.searchicon.setObjectName("SearchTreeIcon")

		self.searchbar = SearchLineEdit()
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

		self.closesearch = QToolButton(self)
		self.closesearch.setIcon(QIcon("resources/Icons/close.png"))
		self.closesearch.setObjectName("SearchTreeClose")
		self.closesearch.setToolTip("Close Search")
		self.closesearch.setCursor(Qt.PointingHandCursor)

		searchpane = QHBoxLayout(self)
		searchpane.addWidget(self.searchicon)
		searchpane.addWidget(self.searchbar)
		searchpane.addWidget(self.searchnext)
		searchpane.addWidget(self.searchprevious)
		searchpane.addWidget(self.matches)
		searchpane.addWidget(self.closesearch)

		searchpane.setContentsMargins(2, 2, 2, 2)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
		else:
			super(SearchTree, self).keyPressEvent(event)


class SearchLineEdit(QLineEdit):
	def __init__(self, parent=None):
		super(SearchLineEdit, self).__init__(parent)


class SearchIcon(QToolButton):
	def __init__(self, parent=None):
		super(SearchIcon, self).__init__(parent)

		self.setIcon(QIcon("resources/Icons/searchtree.png"))
		self.setPopupMode(QToolButton.InstantPopup)
