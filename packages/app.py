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
		message = "Could not create config.yaml file\n" + reason.message
		errorwindow.showError("Error", message)
		sys.exit(app.exec_())

	window = mainwindow.MainWindow()
	window.show()

	app.exec_()
