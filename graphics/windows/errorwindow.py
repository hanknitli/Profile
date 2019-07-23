from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QGridLayout, QDesktopWidget

from graphics.fonts.monospace import Monospace
from packages import utils


class ErrorWindow(QDialog):
	def __init__(self, parent=None):
		super(ErrorWindow, self).__init__(parent)

		self.stylesheet_path = "resources/css/windows/error.css"

		font = Monospace()
		self.setFont(font)

		self.windowtitle = QLabel()
		self.windowtitle.setObjectName("titleLabel")
		self.windowtitle.setStyleSheet(utils.parseStyleSheet(self.stylesheet_path))
		self.windowtitle.setAlignment(Qt.AlignCenter)

		self.bodylabel = QLabel()
		self.bodylabel.setObjectName("bodyLabel")
		self.bodylabel.setStyleSheet(utils.parseStyleSheet(self.stylesheet_path))
		self.bodylabel.setAlignment(Qt.AlignCenter)

		self.closebutton = QPushButton("&Close")
		self.closebutton.clicked.connect(self.close)
		self.closebutton.setObjectName("closeButton")
		self.closebutton.setStyleSheet(utils.parseStyleSheet(self.stylesheet_path))
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
		mainlayout.setContentsMargins(1, 1, 1, 1)

		self.setLayout(mainlayout)

		self.setWindow()

	# self.setGraphicsEffect(effect)
	def setWindow(self):
		desktopgeometry = QDesktopWidget().screenGeometry()

		# width is 40% of screen height
		widget_width = int(40 * desktopgeometry.width() / 100)

		# width is 12% of screen width
		widget_height = int(12 * desktopgeometry.height() / 100)

		widgetstart = desktopgeometry.width() / 2 - widget_width / 2
		widgetend = desktopgeometry.height() / 2 - widget_height / 2
		self.setGeometry(widgetstart, widgetend, widget_width, widget_height)

		self.setObjectName("errorWindow")
		self.setStyleSheet(utils.parseStyleSheet())
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowIcon(QIcon("resources/Icons/profile.ico"))

	def showError(self, title, error):
		self.setWindowTitle(title)
		self.windowtitle.setText(title)
		self.bodylabel.setText(error)
		self.show()
