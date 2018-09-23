from packages import mainWindow
from packages import graphics
from packages import utils


def run():
	import sys

	app = mainWindow.QApplication(sys.argv)

	# check for the config.yaml file
	try:
		utils.configuration.initConfFile()

	except Exception as reason:
		errorwindow = graphics.ErrorWindow()
		message = "Could not create config.yaml file\n" + reason.message
		errorwindow.showError("Error", message)
		sys.exit(app.exec_())

	mainwindow = mainWindow.MainWindow()
	mainwindow.show()

	app.exec_()
