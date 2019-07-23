from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QTextEdit, QTreeWidget, QVBoxLayout, QHBoxLayout, QTreeWidgetItem

from graphics.custom import searchtree
from graphics.mainwindow.treewidget import ProfileTree
from packages import utils, graphics


class MainWidget(QWidget):
	def __init__(self, parent=None):
		super(MainWidget, self).__init__(parent)

		self.stylesheet_path = "resources/css/mainwindow/mainwidget.css"

		# this variable is used to get the current selected item
		self.currentitem = None

		self.editor = QTextEdit(self)
		self.inittextedit()

		self.tree_widget = ProfileTree(self)
		self.inittree()

		self.search_in_tree = searchtree.SearchTree(self)

		leftpane = QVBoxLayout()
		leftpane.addWidget(self.search_in_tree)
		leftpane.addWidget(self.tree_widget)

		mainlayout = QHBoxLayout()
		mainlayout.addLayout(leftpane)
		mainlayout.addWidget(self.editor)
		mainlayout.setSpacing(0)
		mainlayout.setContentsMargins(1, 1, 1, 1)
		self.setLayout(mainlayout)

		self.setObjectName("MainWidget")
		self.setStyleSheet(utils.parseStyleSheet(self.stylesheet_path))
		self.connections()

	def inittextedit(self):
		self.editor.setObjectName("editor")

	def inittree(self):
		self.maketree()
		self.setTreeStyle()

	def maketree(self):
		try:
			profile = utils.readprofile(utils.configuration.profilepath)
			self.parseprofile(profile)

		except IOError as reason:
			inputprofilewindow = graphics.InputProfileWindow(self)
			inputprofilewindow.exec_()
			try:
				profile = utils.readprofile(utils.configuration.profilepath)
				self.parseprofile(profile)

			except IOError as reason:
				graphics.showerror("Profile Error", str(reason))

		except Exception as reason:
			content = "Corrupted profile.yaml file\n" + str(reason)
			graphics.showerror("Profile Error", content)

	def parseprofile(self, profile, item=None):
		if not item:
			item = self.tree_widget.invisibleRootItem()
		if isinstance(profile, dict):
			for key in sorted(profile.keys()):
				parent = item
				item = self.addItem(item, key)
				self.parseprofile(profile[key], item)
				item = parent
		elif isinstance(profile, list):
			for key in profile.__iter__():
				if isinstance(key, dict):
					self.parseprofile(key, item)
				else:
					self.addList(item, key)

	def addItem(self, parent, key):
		item = QTreeWidgetItem(parent, [key])
		item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
		item.setExpanded(utils.configuration.expandedTree)
		return item

	def addList(self, parent, key):
		QTreeWidgetItem(parent, [key]).setExpanded(True)

	def getrootitems(self):
		rootitems = []
		index = 0
		while True:
			root = self.tree_widget.topLevelItem(index)
			index += 1
			if root:
				rootitems.append(root)
			else:
				break
		return rootitems

	def synchronize(self):
		self.tree_widget.clear()
		self.maketree()
		self.setTreeStyle()

	def synchronizeresource(self):
		inputprofilewindow = graphics.InputProfileWindow(self)
		inputprofilewindow.exec_()
		try:
			profile = utils.readprofile(utils.configuration.profilepath)
			self.parseprofile(profile)

		except IOError as reason:
			graphics.showerror("Profile Error", str(reason))

		self.tree_widget.clear()
		self.maketree()
		self.setTreeStyle()

	def connections(self):
		pass  # TODO no connections yet, add every connections here

	def setTreeStyle(self):
		self._scrollbar_set = utils.configuration.scrollbar
		if utils.configuration.scrollbar:
			self.tree_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		else:
			self.tree_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		rootitems = self.getrootitems()
		for item in rootitems:  # TODO set the color to the entire row
			item.setBackground(0, QColor(53, 53, 53))  # TODO set the color of the child indicator

	def showtreesearch(self):
		self.search_in_tree.show()
		self.search_in_tree.searchbar.setFocus()
		self.search_in_tree.searchbar.selectAll()

	def getchildren(self, item):
		children = []
		index = 0
		while True:
			child = item.child(index)
			index += 1
			if child:
				children.append(child)
			else:
				break
		return children

	def expand(self, parent):
		parent.setExpanded(True)
		children = self.getchildren(parent)
		if not children:
			return

		for item in children:
			self.expand(item)

	def collapse(self, parent):
		parent.setExpanded(False)
		children = self.getchildren(parent)
		if not children:
			return

		for item in children:
			self.collapse(item)

	def expandthis(self):
		if self.currentitem:
			self.expand(self.currentitem)

	def collapsethis(self):
		if self.currentitem:
			self.collapse(self.currentitem)

	def expandtree(self):
		rootitems = self.getrootitems()
		for item in rootitems:
			self.expand(item)

	def collapsetree(self):
		rootitems = self.getrootitems()
		for item in rootitems:
			item.setExpanded(False)
			self.collapse(item)
