from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenu, QAction, QAbstractItemView

from graphics.mainwindow.mainwidget import MainWidget
from packages import utils


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.stylesheet_path = "resources/css/mainwindow/mainwindow.css"

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

		self.main_widget = MainWidget(self)
		self.setCentralWidget(self.main_widget)

		# initialize scroll bar check mark
		self.initScrollbar()

		self.setObjectName("Profile")
		self.setStyleSheet(utils.parseStyleSheet(self.stylesheet_path))

		self.connections()

	def initWindow(self):
		desktopgeometry = QDesktopWidget().screenGeometry()

		# window width will be 3/4th of the screen width
		width = desktopgeometry.width() * 3 / 4

		# window height will be 3/4th of the screen height
		height = desktopgeometry.height() * 3 / 4

		start = desktopgeometry.width() / 2 - width / 2
		end = desktopgeometry.height() / 2 - height / 2
		self.setGeometry(start, end, width, height)
		self.setWindowTitle("Profile")
		self.setWindowIcon(QIcon("resources/Icons/profile.ico"))  # TODO create and set a window icon

	def initStatusbar(self):
		self.statusbar.setObjectName("MainStatusBar")

	def initMenubar(self):
		self.menubar.setObjectName("MainMenuBar")

		# File menu item for the menu bar
		self.file = QMenu("&File", self)
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
		self.edit = QMenu("&Edit", self)
		self.menubar.addMenu(self.edit)

		# sub items in Edit menu
		self.findInTree = QAction("Search tree", self)
		self.findInTree.setIcon(QIcon("resources/Icons/searchtree.png"))
		self.findInTree.setStatusTip("Search the complete tree")
		self.findInTree.setShortcut("Ctrl+T")

		# add the sub items to the Edit menu
		self.edit.addActions([self.findInTree, ])

		# View menu item for the menu bar
		self.view = QMenu("&View", self)
		self.menubar.addMenu(self.view)

		# sub items in View menu
		self.scrollbar = QAction("Scrollbar", self)
		self.scrollbar.setStatusTip("Show/Hide the tree's scrollbar")

		self.showtoolbar = QAction("Toolbar", self)
		self.showtoolbar.setStatusTip("Show/Hide the main toolbar")

		# add the sub items to the View menu
		self.view.addActions([self.scrollbar, self.showtoolbar])

		# Tools menu item
		self.tools = QMenu("&Tools", self)
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
		if self.main_widget._scrollbar_set:
			self.scrollbar.setIcon(QIcon("resources/Icons/checked.png"))
		else:
			self.scrollbar.setIcon(QIcon())

	def connections(self):
		self.sync.triggered.connect(self.main_widget.synchronize)
		self.syncresource.triggered.connect(self.main_widget.synchronizeresource)
		self.exit.triggered.connect(self.close)
		self.findInTree.triggered.connect(self.main_widget.showtreesearch)
		self.scrollbar.triggered.connect(self.togglescrollbar)
		self.showtoolbar.triggered.connect(self.toggletoolbar)
		self.expand.triggered.connect(self.main_widget.expandthis)
		self.collapse.triggered.connect(self.main_widget.collapsethis)
		self.expandall.triggered.connect(self.main_widget.expandtree)
		self.collapseall.triggered.connect(self.main_widget.collapsetree)

		self.main_widget.treewidget.itemClicked.connect(self.setCurrentItem)
		self.main_widget.treewidget.itemSelectionChanged.connect(self.itemChanged)
		self.main_widget.search_tree.searchbar.textChanged.connect(self.searchintree)
		self.main_widget.search_tree.searchnext.clicked.connect(self.searchtreenext)
		self.main_widget.search_tree.searchprevious.clicked.connect(self.searchtreeprevious)
		self.main_widget.search_tree.closesearch.clicked.connect(self.main_widget.search_tree.close)

	def toggletoolbar(self):
		checked = self.toolbar.isVisible()
		if not checked:
			self.showtoolbar.setIcon(QIcon("resources/Icons/checked.png"))
		else:
			self.showtoolbar.setIcon(QIcon())
		self.toolbar.toggleViewAction().trigger()

	def togglescrollbar(self):
		if self.main_widget._scrollbar_set:
			self.main_widget.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.scrollbar.setIcon(QIcon())
		else:
			self.main_widget.treewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
			self.scrollbar.setIcon(QIcon("resources/Icons/checked.png"))
		self.main_widget._scrollbar_set = not self.main_widget._scrollbar_set

	def itemChanged(self):
		item = self.main_widget.treewidget.selectedItems()
		# check if the list is empty
		if len(item):
			self.setCurrentItem(item[0], 0)
		path = self.getrootpath(self.main_widget.currentitem)

		windowtitle = str(path.pop(0).text(0)) + " ["
		path.reverse()
		for item in path:
			windowtitle += str(item.text(0)) + '/'
		windowtitle = windowtitle.strip('/') + '] - Profile'
		self.setWindowTitle(windowtitle)

	def setCurrentItem(self, item, column):
		self.main_widget.currentitem = item

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

	def searchintree(self, searchbartext, index=0):
		self.main_widget.search_tree.index = index
		text = searchbartext
		if not text:
			self.clearSelectItems(self.main_widget.search_tree.result)
			self.main_widget.search_tree.matches.hide()
			return  # Return if there is nothing to search
		else:
			self.main_widget.search_tree.matches.show()

		# Clear the previously selected items
		if self.main_widget.search_tree.result:
			self.clearSelectItems(self.main_widget.search_tree.result)

		self.main_widget.search_tree.result = self.main_widget.treewidget.findItems(text,
																					Qt.MatchContains | Qt.MatchRecursive)

		# Select the newly searched items
		if self.main_widget.search_tree.result:
			self.selectItems(self.main_widget.search_tree.result)

		if not self.main_widget.search_tree.result:
			# List is empty, return
			self.main_widget.search_tree.searchbar.setStyleSheet("background: rgb(140, 45, 40);")
			self.main_widget.search_tree.matches.setText("No Matches")
			return
		else:
			matches = len(self.main_widget.search_tree.result)
			self.main_widget.search_tree.matches.setText(str(matches) + " Matches")

		# Holds the current selection
		match = self.main_widget.search_tree.result[index]
		# TODO one colour for the selected item and slight green for the other searched items

		self.main_widget.collapsetree()
		self.main_widget.expand(self.getroot(match))
		self.main_widget.treewidget.scrollToItem(match, QAbstractItemView.PositionAtCenter)

	def searchtreenext(self):
		index = self.main_widget.search_tree.index
		matches = len(self.main_widget.search_tree.result)

		if index == (matches - 1):
			index = 0

		else:
			index = index + 1

		self.main_widget.search_tree.index = index
		self.searchintree(self.main_widget.search_tree.searchbar.text(), index)

	def searchtreeprevious(self):
		index = self.main_widget.search_tree.index
		matches = len(self.main_widget.search_tree.result)

		if index == 0:
			index = matches - 1

		else:
			index = index - 1

		self.main_widget.search_tree.index = index
		self.searchintree(self.main_widget.search_tree.searchbar.text(), index)

	def selectItems(self, result):
		for item in result:
			item.setSelected(True)

	def clearSelectItems(self, result):
		for item in result:
			item.setSelected(False)
