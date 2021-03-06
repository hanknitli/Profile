import sys
import os
import errno
import time

import yaml

execfile("packages/constants.py")


class Configuration:
	def __init__(self):

		self.configfile = None
		self.logfile = None
		self.showtoolbar = None
		self.profilepath = None
		self.expandedTree = None
		self.scrollbar = None

		if sys.platform == "win32":
			__appdata__ = os.getenv("AppData")
			self._configfilepath = os.path.join(__appdata__, parent_windows, __project_name__, configfile)

		elif sys.platform == "linux2":
			path = os.path.expanduser("~/.config/UtilityBelt/Profile")
			self._configfilepath = os.path.join(path, "config.yaml")

		self.setConfig()

	def setConfig(self):
		config = self.readconfig()
		self.configfile = self._configfilepath
		if sys.platform == "win32":
			self.logfile = config["logfile"]["Windows"]
		elif sys.platform == "linux2":
			logfile = config["logfile"]["Linux"]
			self.logfile = os.path.expanduser(logfile)

		self.showtoolbar = config["showtoolbar"]
		self.profilepath = config["profilepath"]
		self.expandedTree = config["expandedTree"]
		self.scrollbar = config["scrollbar"]

	def initConfFile(self):
		if not self.isConfFileExists():
			self.createConfFile()

	def readconfig(self):
		if not self.isConfFileExists():
			self.createConfFile()
			return self.defaultConfig()

		else:
			with open(self._configfilepath, "r") as config:
				data = yaml.load(config)
			return data

	def isConfFileExists(self):
		return os.path.isfile(self._configfilepath)

	def createConfFile(self):
		default_config = self.defaultConfig()
		try:
			os.makedirs(os.path.dirname(self._configfilepath))

		except OSError as reason:
			if reason.errno != errno.EEXIST:
				raise Exception, 'Unknown Error'

		with open(self._configfilepath, "w") as config:
			yaml.dump(default_config, config, default_flow_style=False)

	def defaultConfig(self):
		with open("resources/default_config.yaml", "r") as default_config:
			config = yaml.load(default_config)
		return config

	def initLogFile(self):
		if not self.isLogFileExists():
			self.createLogFile()

	def isLogFileExists(self):
		return os.path.isfile(self.logfile)

	def createLogFile(self):
		try:
			os.makedirs(os.path.dirname(self.logfile))

		except OSError as reason:
			if reason.errno != errno.EEXIST:
				raise Exception('Unknown Error')

		with open(self.logfile, "w") as log:
			log.write("# Log file created at " + time.ctime(time.time()))


def parseStyleSheet():
	with open("resources/stylesheet.css", "r") as cssfile:
		cssdata = cssfile.read()
	return cssdata


def readprofile(profilepath):
	if profilepath:
		if isProfileExists(profilepath):
			with open(profilepath, "r") as profile_file:
				profile = yaml.load(profile_file)
			return profile
		else:
			raise IOError, "Profile not found"


def isProfileExists(profilepath):
	return os.path.isfile(profilepath)


# all the things read from the config.yaml file
configuration = Configuration()
