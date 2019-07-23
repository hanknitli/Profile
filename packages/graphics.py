import os

import git
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QGridLayout, QRadioButton, \
	QLineEdit, QCheckBox, QButtonGroup, QVBoxLayout, QHBoxLayout, QFileDialog, QFrame

from packages import utils


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

		self.defaultrepotext = QLabel("From https://github.com/hanknitli/Profile-Resources.git")
		self.defaultrepotext.setObjectName("DefaultRepoText")
		self.defaultrepotext.setStyleSheet(utils.parseStyleSheet())
		self.defaultrepotext.setDisabled(True)
		self.defaultrepotext.setAlignment(Qt.AlignCenter)

		self.enterrepo = QRadioButton("Get the resources from a different repository")
		self.enterrepo.setChecked(False)

		self.inputrepo = QLineEdit("Enter the .git repository")
		self.inputrepo.setStyleSheet(utils.parseStyleSheet())
		self.inputrepo.setDisabled(True)
		self.inputrepo.setAlignment(Qt.AlignCenter)

		self.resourcepath = QRadioButton("Locate the local resource directory")
		self.resourcepath.setChecked(False)

		self.inputpath = QLineEdit("Enter the path for profile.yaml file")
		self.inputpath.setStyleSheet(utils.parseStyleSheet())
		self.inputpath.setDisabled(True)
		self.inputpath.setAlignment(Qt.AlignCenter)

		self.browsepath = QPushButton("&Browse")
		self.browsepath.setObjectName("BrowsePathButton")
		self.browsepath.setStyleSheet(utils.parseStyleSheet())
		self.browsepath.setDisabled(True)

		self.rememberpath = QCheckBox("&Remember the file path")
		self.rememberpath.setObjectName("RememberPath")
		self.rememberpath.setStyleSheet(utils.parseStyleSheet())
		self.rememberpath.setChecked(False)
		self.rememberpath.setDisabled(True)

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

		resourcepath_hlayout = QHBoxLayout()
		resourcepath_hlayout.addWidget(self.inputpath)
		resourcepath_hlayout.addWidget(self.browsepath)
		checkbox_layout = QHBoxLayout()
		checkbox_layout.addStretch(1)
		checkbox_layout.addWidget(self.rememberpath)

		resourcepath_layout = QVBoxLayout()
		resourcepath_layout.addWidget(self.resourcepath)
		resourcepath_layout.addLayout(resourcepath_hlayout)
		resourcepath_layout.addLayout(checkbox_layout)

		layout = QGridLayout(self)
		layout.addWidget(self.windowtitle, 0, 0, 1, 6)
		layout.addLayout(defaultrepo_layout, 2, 1, 1, 4)
		layout.addLayout(enterrepo_layout, 3, 1, 1, 4)
		layout.addLayout(resourcepath_layout, 4, 1, 1, 4)
		layout.addWidget(self.select, 6, 2, 1, 1)
		layout.addWidget(self.cancel, 6, 3, 1, 1)
		layout.setRowMinimumHeight(0, 24)
		layout.setRowMinimumHeight(1, 10)
		layout.setRowMinimumHeight(5, 10)
		layout.setRowMinimumHeight(7, 5)
		layout.setSpacing(5)
		layout.setContentsMargins(1, 1, 1, 1)

		self.setLayout(layout)
		self.connections()
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
		self.setObjectName("InputProfileWindow")
		self.setStyleSheet(utils.parseStyleSheet())
		self.setWindowTitle("Select the resource")

	def connections(self):
		self.defaultrepo.toggled.connect(self.defaultrepooption)
		self.enterrepo.toggled.connect(self.enterrepooption)
		self.resourcepath.toggled.connect(self.resourcepathoption)
		self.browsepath.clicked.connect(self.browse)
		self.select.clicked.connect(self.processresource)
		self.cancel.clicked.connect(self.close)

	def defaultrepooption(self, button):
		if button:
			self.defaultrepotext.setStyleSheet(utils.parseStyleSheet())
		else:
			self.defaultrepotext.setStyleSheet("background-color: rgb(50, 50, 50)")

	def enterrepooption(self, button):
		if button:
			self.inputrepo.setDisabled(False)
			self.inputrepo.setFocus()
			self.inputrepo.clear()
		else:
			self.inputrepo.setDisabled(True)
			self.inputrepo.setText("Enter the .git repository")

	def resourcepathoption(self, button):
		if button:
			self.inputpath.setDisabled(False)
			self.inputpath.setFocus()
			self.inputpath.clear()
			self.browsepath.setDisabled(False)
			self.rememberpath.setDisabled(False)
		else:
			self.inputpath.setDisabled(True)
			self.inputpath.setText("Enter the path for profile.yaml file")
			self.browsepath.setDisabled(True)
			self.rememberpath.setChecked(False)
			self.rememberpath.setDisabled(True)

	def browse(self):
		browsedialog = QFileDialog(self)
		self.inputpath.setText(browsedialog.getOpenFileName())

	def processresource(self):
		selection = self.group.checkedId()

		# TODO add a progress bar for fetching resources

		try:
			if selection == 0:
				utils.configuration.setDefaultConfigProperty("profilepath")
				gitpath = "https://github.com/hanknitli/Profile-Resources.git"
				utils.parseGit(gitpath)

			elif selection == 1:
				utils.configuration.setDefaultConfigProperty("profilepath")
				gitpath = str(self.inputrepo.text())
				utils.parseGit(gitpath)

			elif selection == 2:
				path = str(self.inputpath.text())
				utils.configuration.profilepath = os.path.dirname(path)
				if self.rememberpath.isChecked():
					utils.configuration.updateConfFile()

		except git.GitCommandError as reason:
			self.hide()
			showerror("Git Error", str(reason.stderr))

		except Exception as reason:
			self.hide()
			showerror("Error in Resource", str(reason))

		finally:
			utils.cleanProfileDir()

		self.close()


class ToolTip(QLabel):
	def __init__(self, parent=None):
		super(ToolTip, self).__init__(parent)

		self.setWindowFlags(Qt.ToolTip)
		self.setFrameShape(QFrame.StyledPanel)
		self.hide()  # TODO implement a tooltip mechanism (maybe mousetracking and hover event)


def showerror(title=None, reason=None, parent=None):
	error = ErrorWindow(parent)
	if not title:
		title = "Error"
	if not reason:
		content = "Unknown Error"
	else:
		content = reason
	error.showError(title.strip(), content.strip())
	error.exec_()
