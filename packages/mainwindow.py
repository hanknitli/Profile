from PyQt4.QtCore import *
from PyQt4.QtGui import *
from packages import utils
from packages import graphics
from packages import QtClasses


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.initWindow()

		# status bar for the main window
		self.statusbar = self.statusBar()
		self.initStatusbar()

		# menu bar for the main window
		self.menubar = self.menuBar()
		self.initMenubar()

		# tool bar for the main window
		self.toolbar = self.addToolBar("MainToolBar")
		self.initToolbar()

		self.mainwidget = MainWidget(self)
		self.setCentralWidget(self.mainwidget)

		# initialize scroll bar check mark
		self.initScrollbar()

		self.setObjectName("Profile")
		self.setStyleSheet(utils.parseStyleSheet())

		self.connections()

	def initWindow(self):
		desktopgeometry = QDesktopWidget().screenGeometry()
		width = desktopgeometry.width() * 3 / 4
		height = desktopgeometry.height() * 3 / 4
		start = desktopgeometry.width() / 2 - width / 2
		end = desktopgeometry.height() / 2 - height / 2
		self.setGeometry(start, end, width, height)
		self.setWindowTitle("Profile")
		self.setWindowIcon(QIcon("resources/Icons/profile.ico"))  # TODO create and set a window icon

	def initStatusbar(self):
		self.statusbar.setObjectName("MainStatusBar")
		self.statusbar.setStyleSheet(utils.parseStyleSheet())

	def initMenubar(self):
		self.menubar.setObjectName("MainMenuBar")
		self.menubar.setStyleSheet(utils.parseStyleSheet())

		# File menu item for the menu bar
		self.file = QMenu("&File", self)
		self.file.setStyleSheet(utils.parseStyleSheet())
		self.menubar.addMenu(self.file)

		# sub items in File menu
		self.new = QAction("&New", self)
		self.new.setIcon(QIcon("resources/Icons/newFolder.png"))  # TODO fix the icon popup
		self.new.setShortcut("Ctrl+Shift+N")

		self.sync = QAction("&Synchronize", self)
		self.sync.setIcon(QIcon("resources/Icons/sync.png"))
		self.sync.setShortcut("")  # TODO define a shortcut
		self.sync.setStatusTip("Sync the app with profile.yaml")

		self.syncresource = QAction("&Synchronize Resources", self)
		self.syncresource.setIcon(QIcon("resources/Icons/syncResources.png"))
		self.syncresource.setShortcut("")  # TODO define a shortcut
		self.syncresource.setStatusTip("Sync the local resource with a repository")

		self.exit = QAction("&Exit", self)
		self.exit.setIcon(QIcon("resources/Icons/exit.png"))
		self.exit.setShortcut("Alt+F4")
		self.exit.setStatusTip("Exit the application")

		# add the sub items to the File menu
		self.file.addActions([self.new, self.sync, self.syncresource, self.exit])

		# Edit menu item for the menu bar
		self.edit = QMenu("&Edit")
		self.edit.setStyleSheet(utils.parseStyleSheet())
		self.menubar.addMenu(self.edit)

		# sub items in Edit menu
		self.findInTree = QAction("Search tree", self)
		self.findInTree.setStatusTip("Search the complete tree")
		self.findInTree.setShortcut("Ctrl+T")

		# add the sub items to the Edit menu
		self.edit.addActions([self.findInTree, ])

		# View menu item for the menu bar
		self.view = QMenu("&View")
		self.view.setStyleSheet(utils.parseStyleSheet())
		self.menubar.addMenu(self.view)

		# sub items in View menu
		self.scrollbar = QAction("Scrollbar", self)
		self.scrollbar.setStatusTip("Show/Hide the tree's scrollbar")

		self.showtoolbar = QAction("Toolbar", self)
		self.showtoolbar.setStatusTip("Show/Hide the main toolbar")

		# add the sub items to the View menu
		self.view.addActions([self.scrollbar, self.showtoolbar])

		# Tools menu item
		self.tools = QMenu("&Tools")
		self.tools.setStyleSheet(utils.parseStyleSheet())
		self.menubar.addMenu(self.tools)

		# sub items in Tools menu

		self.expand = QAction("Expand This", self)
		self.expand.setIcon(QIcon("resources/Icons/expandThis.png"))
		self.expand.setStatusTip("Expand all the elements under this item")

		self.collapse = QAction("Collapse This", self)
		self.collapse.setIcon(QIcon("resources/Icons/collapseThis.png"))
		self.collapse.setStatusTip("Collapse all the elements under this item")

		self.expandall = QAction("Expand All", self)
		self.expandall.setIcon(QIcon())  # TODO add an icon
		self.expandall.setStatusTip("Expand all the tree elements")

		self.collapseall = QAction("Collapse All", self)
		self.collapseall.setIcon(QIcon())  # TODO add an icon
		self.collapseall.setStatusTip("Collapse all the tree elements")

		self.tools.addActions([self.expand, self.collapse, self.expandall, self.collapseall])

	def initToolbar(self):
		self.toolbar.setMovable(False)
		self.toolbar.setObjectName("MainToolBar")
		self.toolbar.setStyleSheet(utils.parseStyleSheet())

		self.toolbar.addActions([self.new, self.sync, self.syncresource])
		self.toolbar.addSeparator()
		self.toolbar.addActions([self.expand, self.collapse])
		self.toolbar.addSeparator()
		self.toolbar.addActions([self.expandall, self.collapseall])
		self.toolbar.addSeparator()

		if not utils.configuration.showtoolbar:
			self.toolbar.close()
			self.showtoolbar.setIcon(QIcon())
		else:
			self.showtoolbar.setIcon(QIcon("resources/Icons/checked.png"))

	def initScrollbar(self):
		if self.mainwidget._scrollbarset:
			self.scrollbar.setIcon(QIcon("resources/Icons/checked.png"))
		else:
			self.scrollbar.setIcon(QIcon())

	def connections(self):
		self.sync.triggered.connect(self.mainwidget.synchronize)
		self.syncresource.triggered.connect(self.mainwidget.synchronizeresource)
		self.exit.triggered.connect(self.close)
		self.findInTree.triggered.connect(self.mainwidget.showtreesearch)
		self.scrollbar.triggered.connect(self.togglescrollbar)
		self.showtoolbar.triggered.connect(self.toggletoolbar)
		self.expand.triggered.connect(self.mainwidget.expandthis)
		self.collapse.triggered.connect(self.mainwidget.collapsethis)
		self.expandall.triggered.connect(self.mainwidget.expandtree)
		self.collapseall.triggered.connect(self.mainwidget.collapsetree)

		self.mainwidget.treewidget.itemClicked.connect(self.setCurrentItem)
		self.mainwidget.treewidget.itemSelectionChanged.connect(self.itemChanged)
		self.mainwidget.searchtree.searchbar.textChanged.connect(self.searchintree)
		self.mainwidget.searchtree.searchnext.clicked.connect(self.searchtreenext)
		self.mainwidget.searchtree.searchprevious.clicked.connect(self.searchtreeprevious)
		self.mainwidget.searchtree.closesearch.clicked.connect(self.mainwidget.searchtree.close)

	def toggletoolbar(self):
		checked = self.toolbar.isVisible()
		if not checked:
			self.showtoolbar.setIcon(QIcon("resources/Icons/checked.png"))
		else:
			self.showtoolbar.setIcon(QIcon())
		self.toolbar.toggleViewAction().trigger()

	def togglescrollbar(self):
		if self.mainwidget._scrollbarset:
			self.mainwidget.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.scrollbar.setIcon(QIcon())
		else:
			self.mainwidget.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
			self.scrollbar.setIcon(QIcon("resources/Icons/checked.png"))
		self.mainwidget._scrollbarset = not self.mainwidget._scrollbarset

	def itemChanged(self):
		item = self.mainwidget.treewidget.selectedItems()
		# check if the list is empty
		if len(item):
			self.setCurrentItem(item[0], 0)
		path = self.getrootpath(self.mainwidget.currentitem)

		windowtitle = str(path.pop(0).text(0)) + " ["
		path.reverse()
		for item in path:
			windowtitle += str(item.text(0)) + '/'
		windowtitle = windowtitle.strip('/') + '] - Profile'
		self.setWindowTitle(windowtitle)

	def setCurrentItem(self, item, column):
		self.mainwidget.currentitem = item

	def getrootpath(self, item):
		path = [item]
		while True:
			parent = item.parent()
			if parent:
				path.append(parent)
				item = parent
			else:
				break
		return path

	def getroot(self, item):
		rootpath = self.getrootpath(item)
		return rootpath[-1]

	def searchintree(self):
		index = 0
		self.mainwidget.searchtree.index = index
		text = self.mainwidget.searchtree.searchbar.text()
		if not text:
			self.clearSelectItems(self.mainwidget.searchtree.result)
			self.mainwidget.searchtree.matches.hide()
			return  # Return if there is nothing to search
		else:
			self.mainwidget.searchtree.matches.show()

		# Clear the previously selected items
		if self.mainwidget.searchtree.result:
			self.clearSelectItems(self.mainwidget.searchtree.result)

		self.mainwidget.searchtree.result = self.mainwidget.treewidget.findItems(text,
																				 Qt.MatchContains | Qt.MatchRecursive)

		# Select the newly searched items
		if self.mainwidget.searchtree.result:
			self.selectItems(self.mainwidget.searchtree.result)

		if not self.mainwidget.searchtree.result:
			# List is empty, return
			self.mainwidget.searchtree.searchbar.setStyleSheet("background: rgb(100, 0, 0);")
			self.mainwidget.searchtree.matches.setText("No Matches")
			return
		else:
			matches = len(self.mainwidget.searchtree.result)
			self.mainwidget.searchtree.matches.setText(str(matches) + " Matches")
			self.mainwidget.searchtree.searchbar.setStyleSheet(utils.parseStyleSheet())

		match = self.mainwidget.searchtree.result[index]

		self.mainwidget.collapsetree()
		self.mainwidget.expand(self.getroot(match))
		self.mainwidget.treewidget.scrollToItem(match, QAbstractItemView.PositionAtCenter)
		print match.text(0)

	def searchtreenext(self):
		index = self.mainwidget.searchtree.index
		matches = len(self.mainwidget.searchtree.result)

		if index == (matches - 1):
			index = 0

		else:
			index = index + 1

		self.mainwidget.searchtree.index = index

	def searchtreeprevious(self):
		index = self.mainwidget.searchtree.index
		matches = len(self.mainwidget.searchtree.result)

		if index == 0:
			index = matches - 1

		else:
			index = index - 1

		self.mainwidget.searchtree.index = index

	def selectItems(self, result):
		for item in result:
			item.setSelected(True)

	def clearSelectItems(self, result):
		for item in result:
			item.setSelected(False)

class MainWidget(QWidget):
	def __init__(self, parent=None):
		super(MainWidget, self).__init__(parent)

		# this variable is used to get the current selected item
		self.currentitem = None

		self.editor = QTextEdit(self)
		self.inittextedit()

		self.treewidget = QTreeWidget(self)
		self.inittree()

		self.searchtree = QtClasses.SearchTree(self)
		self.searchtree.setObjectName("SearchTree")
		self.searchtree.setStyleSheet(utils.parseStyleSheet())
		self.searchtree.hide()

		leftpane = QVBoxLayout()
		leftpane.addWidget(self.searchtree)
		leftpane.addWidget(self.treewidget)

		mainlayout = QHBoxLayout()
		mainlayout.addLayout(leftpane)
		mainlayout.addWidget(self.editor)
		mainlayout.setSpacing(0)
		mainlayout.setMargin(1)
		self.setLayout(mainlayout)

		self.setObjectName("MainWidget")
		self.setStyleSheet(utils.parseStyleSheet())
		self.connections()

	def inittextedit(self):
		self.editor.setObjectName("editor")
		self.editor.setStyleSheet(utils.parseStyleSheet())

	def inittree(self):
		self.treewidget.setObjectName("TreeWidget")
		self.treewidget.setStyleSheet(utils.parseStyleSheet())
		self.treewidget.setHeaderHidden(True)
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
			item = self.treewidget.invisibleRootItem()
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
			root = self.treewidget.topLevelItem(index)
			index += 1
			if root:
				rootitems.append(root)
			else:
				break
		return rootitems

	def synchronize(self):
		self.treewidget.clear()
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

		self.treewidget.clear()
		self.maketree()
		self.setTreeStyle()

	def connections(self):
		pass  # TODO no connections yet, add every connections here

	def setTreeStyle(self):
		self._scrollbarset = utils.configuration.scrollbar
		if utils.configuration.scrollbar:
			self.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		else:
			self.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		rootitems = self.getrootitems()
		for item in rootitems:  # TODO set the color to the entire row
			item.setBackgroundColor(0, QColor(53, 53, 53))  # TODO set the color of the child indicator

	def showtreesearch(self):
		self.searchtree.show()
		self.searchtree.searchbar.setFocus()
		self.searchtree.searchbar.selectAll()

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
