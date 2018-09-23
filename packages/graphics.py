from PyQt4.QtGui import *
from PyQt4.QtCore import *
from packages import utils


class ErrorWindow(QWidget):
	def __init__(self, parent=None):
		super(ErrorWindow, self).__init__(parent)

		self.setWindow()

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
		self.setObjectName("errorWindow")
		self.setStyleSheet(utils.parseStyleSheet())
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowIcon(QIcon("resources/Icons/profile.ico"))

	# self.setGraphicsEffect(effect)
	def setWindow(self):
		desktopgeometry = QDesktopWidget().screenGeometry()
		widgetlength = 400
		widgetwidth = 100
		widgetstart = desktopgeometry.width() / 2 - widgetlength / 2
		widgetend = desktopgeometry.height() / 2 - widgetwidth / 2
		self.setGeometry(widgetstart, widgetend, widgetlength, widgetwidth)

	def showError(self, title, error):
		self.setWindowTitle(title)
		self.windowtitle.setText(title)
		self.bodylabel.setText(error)
		self.show()


class ToolTip(QLabel):
	def __init__(self, parent=None):
		super(ToolTip, self).__init__(parent)

		self.setWindowFlags(Qt.ToolTip)
		self.setFrameShape(QFrame.StyledPanel)
		self.hide()  # TODO implement a tooltip mechanism (maybe mousetracking and hover event)
