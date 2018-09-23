from PyQt4.QtCore import *
from PyQt4.QtGui import *
from packages import graphics
from packages import utils


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

		# TODO add menu items
		# TODO add toolbar
		# TODO add widgets

		self.mainwidget = MainWidget(self)
		self.setCentralWidget(self.mainwidget)

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
		self.setWindowIcon(QIcon("resources/profile.ico"))  # TODO create and set a window icon

	def initStatusbar(self):
		self.statusbar.setObjectName("MainStatusBar")
		self.statusbar.setStyleSheet(utils.parseStyleSheet())

	def initMenubar(self):
		self.menubar.setObjectName("MainMenuBar")
		self.menubar.setStyleSheet(utils.parseStyleSheet())
		self.menubar.setStatusTip("ToolBar")

		# File menu item for the menu bar
		self.file = QMenu("&File", self)
		self.file.setStyleSheet(utils.parseStyleSheet())
		self.menubar.addMenu(self.file)

		# sub items in File menu
		self.new = QAction("&New", self)
		self.new.setIcon(QIcon("D:/Softwares/Projects/Resources/Icons/rec.png"))  # TODO fix the icon popup
		self.new.setShortcut("Ctrl+Shift+N")

		self.sync = QAction("&Synchronize", self)
		self.sync.setIcon(QIcon())  # TODO set an icon
		self.sync.setShortcut("")  # TODO define a shortcut

		self.exit = QAction("&Exit", self)
		self.exit.setShortcut("Alt+F4")
		self.exit.setStatusTip("Exit the application")

		# add the sub items to the File menu
		self.file.addActions([self.new, self.sync, self.exit])

		# Edit menu item for the menu bar
		self.edit = QMenu("&Edit")
		self.edit.setStyleSheet(utils.parseStyleSheet())
		self.menubar.addMenu(self.edit)

		# View menu item for the menu bar
		self.view = QMenu("&View")
		self.view.setStyleSheet(utils.parseStyleSheet())
		self.menubar.addMenu(self.view)

		# sub items in View menu
		self.scrollbar = QAction("Scrollbar", self)
		self.scrollbar.setIcon(QIcon())  # TODO add the checkmark icon
		self.scrollbar.setStatusTip("Show/Hide the tree's scrollbar")

		self.showtoolbar = QAction("Toolbar", self)
		self.showtoolbar.setIcon(QIcon())  # TODO add the checkmark icon
		self.showtoolbar.setStatusTip("Show/Hide the main toolbar")

		# add the sub items to the View menu
		self.view.addActions([self.scrollbar, self.showtoolbar])

		# Tools menu item
		self.tools = QMenu("&Tools")
		self.tools.setStyleSheet(utils.parseStyleSheet())
		self.menubar.addMenu(self.tools)

		# sub items in Tools menu

		self.expand = QAction("Expand This", self)
		self.expand.setIcon(QIcon())  # TODO add an icon
		self.expand.setStatusTip("Expand all the elements under this item")

		self.collapse = QAction("Collapse This", self)
		self.collapse.setIcon(QIcon())  # TODO add an icon
		self.collapse.setStatusTip("Collapse all the elements under this item")

		self.expandall = QAction("Expand All", self)
		self.expandall.setIcon(QIcon())  # TODO add an icon
		self.expandall.setStatusTip("Expand all the tree elements")

		self.collapseall = QAction("Collapse All", self)
		self.collapseall.setIcon(QIcon())  # TODO add an icon
		self.collapseall.setStatusTip("Collapse all the tree elements")

		# add the sub items to the Tools menu
		self.tools.addActions([self.expand, self.collapse, self.expandall, self.collapseall])

	def initToolbar(self):
		self.toolbar.setMovable(False)
		self.toolbar.setObjectName("MainToolBar")
		self.toolbar.setStyleSheet(utils.parseStyleSheet())

		self.toolbar.addActions([self.new, self.exit, self.sync])
		self.toolbar.addActions([self.scrollbar])
		self.toolbar.addActions([self.expand, self.collapse, self.expandall, self.collapseall])

	def connections(self):
		self.sync.triggered.connect(self.mainwidget.synchronize)
		self.exit.triggered.connect(self.close)
		self.scrollbar.triggered.connect(self.mainwidget.togglescrollbar)
		self.showtoolbar.triggered.connect(self.toggletoolbar)
		self.expand.triggered.connect(self.mainwidget.expandthis)
		self.collapse.triggered.connect(self.mainwidget.collapsethis)
		self.expandall.triggered.connect(self.mainwidget.expandtree)
		self.collapseall.triggered.connect(self.mainwidget.collapsetree)

	def toggletoolbar(self):
		self.toolbar.toggleViewAction().trigger()


class MainWidget(QWidget):
	def __init__(self, parent=None):
		super(MainWidget, self).__init__(parent)

		# this variable is used to get the current selected item
		self.currentitem = None

		self.editor = QTextEdit(self)
		self.inittextedit()

		self.treewidget = QTreeWidget(self)
		self.inittree()

		layout = QHBoxLayout(self)
		layout.addWidget(self.treewidget)
		layout.addWidget(self.editor)
		layout.setSpacing(0)
		layout.setMargin(1)
		self.setLayout(layout)

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
			print reason.message  # TODO show an error saying profile not found

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

	def itemChanged(self):
		item = self.treewidget.selectedItems()
		self.setCurrentItem(item[0], 0)

	def setCurrentItem(self, item, column):
		self.currentitem = item

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

	def togglescrollbar(self):
		if self._scrollbarset:
			self.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		else:
			self.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self._scrollbarset = not self._scrollbarset

	def synchronize(self):
		self.treewidget.clear()
		self.maketree()

	def connections(self):
		self.treewidget.itemClicked.connect(self.setCurrentItem)
		self.treewidget.itemSelectionChanged.connect(self.itemChanged)

	def setTreeStyle(self):
		self._scrollbarset = utils.configuration.scrollbar
		if utils.configuration.scrollbar:
			self.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		else:
			self.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		rootitems = self.getrootitems()
		for item in rootitems:  # TODO set the color to the entire row
			item.setBackgroundColor(0, QColor(53, 53, 53))  # TODO set the color of the child indicator

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
