import traceback

from packages import mainwindow
from packages import graphics
from packages import utils


def run():
	import sys

	app = mainwindow.QApplication(sys.argv)

	# check for the config.yaml file
	try:
		utils.configuration.initConfFile()

	except Exception as reason:
		errorwindow = graphics.ErrorWindow()
		message = "Could not create config.yaml file at\n" + utils.configuration.configfile + "\n\n" + str(reason)
		errorwindow.showError("Error", message)
		sys.exit(app.exec_())

	# check for the config.yaml file
	try:
		utils.configuration.initLogFile()

	except Exception as reason:
		errorwindow = graphics.ErrorWindow()
		message = "Could not create Log file at\n" + utils.configuration.logfile + "\n\n" + str(reason)
		errorwindow.showError("Error", message)
		sys.exit(app.exec_())

	# check for the .profile directory path
	try:
		utils.configuration.initProfilePath()

	except Exception as reason:
		errorwindow = graphics.ErrorWindow()
		message = "Could not create the .profile directory at\n" + utils.configuration.profilepath + "\n\n"
		message += str(reason)
		errorwindow.showError("Error", message)
		sys.exit(app.exec_())

	window = mainwindow.MainWindow()
	window.show()

	app.exec_()
