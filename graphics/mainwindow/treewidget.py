from PyQt5.QtWidgets import QTreeWidget

from packages import utils


class ProfileTree(QTreeWidget):
	def __init__(self, parent=None):
		super(ProfileTree, self).__init__(parent)

		self.stylesheet_path = "resources/css/mainwindow/treewidget.css"

		self.setObjectName("TreeWidget")
		self.setHeaderHidden(True)

		self.setStyleSheet(utils.parseStyleSheet(self.stylesheet_path))
