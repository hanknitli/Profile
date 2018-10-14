from PyQt4.QtGui import *
from PyQt4.QtCore import *
from packages import utils


class ErrorWindow(QDialog):
	def __init__(self, parent=None):
		super(ErrorWindow, self).__init__(parent)

		font = QApplication.font()
		font.setStyleStrategy(QFont.PreferAntialias)
		QApplication.setFont(font)

		self.windowtitle = QLabel()
		self.windowtitle.setObjectName("titleLabel")
		self.windowtitle.setStyleSheet(utils.parseStyleSheet())
		self.windowtitle.setAlignment(Qt.AlignCenter)

		self.bodylabel = QLabel()
		self.bodylabel.setObjectName("bodyLabel")
		self.bodylabel.setStyleSheet(utils.parseStyleSheet())
		self.bodylabel.setAlignment(Qt.AlignCenter)

		self.closebutton = QPushButton("&Close")
		self.closebutton.clicked.connect(self.close)
		self.closebutton.setObjectName("closeButton")
		self.closebutton.setStyleSheet(utils.parseStyleSheet())
		self.closebutton.setMinimumWidth(80)
		self.closebutton.setToolTip("Close and Quit")

		mainlayout = QGridLayout()
		mainlayout.addWidget(self.windowtitle, 0, 0, 1, 6)
		mainlayout.addWidget(self.bodylabel, 1, 1, 3, 2, Qt.AlignCenter)
		mainlayout.addWidget(self.closebutton, 2, 4, 1, 1)
		mainlayout.setRowMinimumHeight(0, 24)
		mainlayout.setColumnMinimumWidth(0, 10)
		mainlayout.setColumnMinimumWidth(3, 10)
		mainlayout.setColumnMinimumWidth(4, 80)
		mainlayout.setColumnMinimumWidth(5, 10)
		mainlayout.setSpacing(0)
		mainlayout.setMargin(1)

		self.setLayout(mainlayout)

		self.setWindow()

	# self.setGraphicsEffect(effect)
	def setWindow(self):
		desktopgeometry = QDesktopWidget().screenGeometry()
		widgetlength = 400
		widgetwidth = 100
		widgetstart = desktopgeometry.width() / 2 - widgetlength / 2
		widgetend = desktopgeometry.height() / 2 - widgetwidth / 2
		self.setGeometry(widgetstart, widgetend, widgetlength, widgetwidth)

		# TODO position the window at the center of the screen

		self.setObjectName("errorWindow")
		self.setStyleSheet(utils.parseStyleSheet())
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowIcon(QIcon("resources/Icons/profile.ico"))

	def showError(self, title, error):
		self.setWindowTitle(title)
		self.windowtitle.setText(title)
		self.bodylabel.setText(error)
		self.show()


class InputProfileWindow(QDialog):
	def __init__(self, parent=None):
		super(InputProfileWindow, self).__init__(parent)

		self.windowtitle = QLabel("Select the resource")
		self.windowtitle.setObjectName("profileTitleLabel")
		self.windowtitle.setStyleSheet(utils.parseStyleSheet())
		self.windowtitle.setAlignment(Qt.AlignCenter)

		self.defaultrepo = QRadioButton("Get the resources from default repository")
		self.defaultrepo.setChecked(True)
		self.defaultrepo.setStyleSheet(utils.parseStyleSheet())

		self.defaultrepotext = QLabel("from https://github.com/hanknitli/profile_resources/")

		self.enterrepo = QRadioButton("Get the resources from a different repository")
		self.enterrepo.setChecked(False)

		self.inputrepo = QLineEdit("Enter the .git repository")
		self.inputrepo.setObjectName("InputRepo")
		self.inputrepo.setStyleSheet(utils.parseStyleSheet())
		self.inputrepo.selectAll()

		self.resourcepath = QRadioButton("Locate the local resource directory")
		self.resourcepath.setChecked(False)

		self.group = QButtonGroup(self)
		self.group.addButton(self.defaultrepo, 0)
		self.group.addButton(self.enterrepo, 1)
		self.group.addButton(self.resourcepath, 2)

		self.select = QPushButton("&OK")
		self.select.setObjectName("profileButton")
		self.select.setStyleSheet(utils.parseStyleSheet())
		self.cancel = QPushButton("&Cancel")
		self.cancel.setObjectName("profileButton")
		self.cancel.setStyleSheet(utils.parseStyleSheet())

		# TODO add a dynamic layout arrangement (stack layout?)

		defaultrepo_layout = QVBoxLayout()
		defaultrepo_layout.addWidget(self.defaultrepo)
		defaultrepo_layout.addWidget(self.defaultrepotext)

		enterrepo_layout = QVBoxLayout()
		enterrepo_layout.addWidget(self.enterrepo)
		enterrepo_layout.addWidget(self.inputrepo)

		resourcepath_layout = QVBoxLayout()
		resourcepath_layout.addWidget(self.resourcepath)

		layout = QGridLayout(self)
		layout.addWidget(self.windowtitle, 0, 0, 1, 6)
		layout.addLayout(defaultrepo_layout, 2, 1, 1, 4)
		layout.addLayout(enterrepo_layout, 3, 1, 1, 4)
		layout.addWidget(self.resourcepath, 4, 1, 1, 4)
		layout.addWidget(self.select, 6, 2, 1, 1)
		layout.addWidget(self.cancel, 6, 3, 1, 1)
		layout.setRowMinimumHeight(0, 24)
		layout.setRowMinimumHeight(1, 10)
		layout.setRowMinimumHeight(5, 10)
		layout.setSpacing(5)
		layout.setMargin(1)

		self.setLayout(layout)
		self.connections()
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
		self.setObjectName("InputProfileWindow")
		self.setStyleSheet(utils.parseStyleSheet())

	def connections(self):
		self.defaultrepo.toggled.connect(self.defaultrepooption)
		self.enterrepo.toggled.connect(self.enterrepooption)
		self.resourcepath.toggled.connect(self.resourcepathoption)
		self.select.clicked.connect(self.processresource)
		self.cancel.clicked.connect(self.close)

	def defaultrepooption(self, button):
		print 'button 1', button

	def enterrepooption(self, button):
		print 'button 2', button

	def resourcepathoption(self, button):
		print 'button 3', button

	def processresource(self):
		print 'processing git...'
		print self.group.checkedId()
		self.close()


class ToolTip(QLabel):
	def __init__(self, parent=None):
		super(ToolTip, self).__init__(parent)

		self.setWindowFlags(Qt.ToolTip)
		self.setFrameShape(QFrame.StyledPanel)
		self.hide()  # TODO implement a tooltip mechanism (maybe mousetracking and hover event)
