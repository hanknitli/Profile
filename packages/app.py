from PyQt5.QtWidgets import QApplication

from graphics.windows import errorwindow
from graphics.mainwindow import basewindow
from packages import utils


def run():
	import sys

	app = QApplication(sys.argv)

	# check for the config.yaml file
	try:
		utils.configuration.initConfFile()

	except Exception as reason:
		error = errorwindow.ErrorWindow()
		message = "Could not create config.yaml file at\n" + utils.configuration.configfile + "\n\n" + str(reason)
		error.showError("Error", message)
		sys.exit(app.exec_())

	# check for the log.txt file
	try:
		utils.configuration.initLogFile()

	except Exception as reason:
		error = errorwindow.ErrorWindow()
		message = "Could not create Log file at\n" + utils.configuration.logfile + "\n\n" + str(reason)
		error.showError("Error", message)
		sys.exit(app.exec_())

	# check for the .profile directory path
	try:
		utils.configuration.initProfilePath()

	except Exception as reason:
		error = errorwindow.ErrorWindow()
		message = "Could not create the .profile directory at\n" + utils.configuration.profilepath + "\n\n"
		message += str(reason)
		error.showError("Error", message)
		sys.exit(app.exec_())

	main_window = basewindow.MainWindow()
	main_window.show()

	app.exec_()
