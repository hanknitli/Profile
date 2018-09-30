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

		with open("resources/default_config.yaml", "r") as default_config:
			config = yaml.load(default_config)

		if sys.platform == "win32":
			__appdata__ = os.getenv(config["configfile"]["Windows"])
			self._configfilepath = os.path.join(__appdata__, parent_windows, __project_name__, configfile)

		elif sys.platform == "linux2":
			__config__ = os.path.expanduser(config["configfile"]["Linux"])
			self._configfilepath = os.path.join(__config__, parent_linux, __project_name__, configfile)
		self.configfile = self._configfilepath

	def initConfFile(self):
		if not self.isConfFileExists():
			self.createConfFile()
		self.setConfig()

	def isConfFileExists(self):
		return os.path.isfile(self.configfile)

	def createConfFile(self):
		default_config = self.defaultConfig()
		try:
			os.makedirs(os.path.dirname(self.configfile))

		except OSError as reason:
			if reason.errno != errno.EEXIST:
				raise Exception, 'Unknown Error'

		with open(self.configfile, "w") as config:
			yaml.dump(default_config, config, default_flow_style=False)

	def defaultConfig(self):
		with open("resources/default_config.yaml", "r") as default_config:
			config = yaml.load(default_config)

		if sys.platform == "win32":
			self.logfile = config["logfile"]["Windows"]
			basepath = os.getenv(config["profilepath"]["Windows"])
			self.profilepath = os.path.join(basepath, ".profile")

		elif sys.platform == "linux2":
			basepath = os.path.expanduser(config["logfile"]["Linux"])
			self.logfile = os.path.join(basepath, parent_linux, __project_name__, "log.txt")

			basepath = os.path.expanduser((config["profilepath"]["Linux"]))
			self.profilepath = os.path.join(basepath, parent_linux, __project_name__, ".profile")

		self.showtoolbar = config["showtoolbar"]
		self.expandedTree = config["expandedTree"]
		self.scrollbar = config["scrollbar"]

		default_config = {"logfile": self.logfile, "showtoolbar": self.showtoolbar, "profilepath": self.profilepath, \
						  "expandedTree": self.expandedTree, "scrollbar": self.scrollbar}
		return default_config

	def setConfig(self):
		config = self.readconfig()

		self.logfile = config["logfile"]
		self.showtoolbar = config["showtoolbar"]
		self.profilepath = config["profilepath"]
		self.expandedTree = config["expandedTree"]
		self.scrollbar = config["scrollbar"]

	def readconfig(self):
		if not self.isConfFileExists():
			self.createConfFile()
			return self.defaultConfig()

		else:
			with open(self.configfile, "r") as config:
				data = yaml.load(config)
			return data

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

	def initProfilePath(self):
		if not self.isProfilePathExists():
			self.createProfilePath()

	def isProfilePathExists(self):
		return os.path.isdir(self.profilepath)

	def createProfilePath(self):
		try:
			os.makedirs(self.profilepath)

		except OSError as reason:
			if reason.errno != errno.EEXIST:
				raise Exception('Unknown Error')


def parseStyleSheet():
	with open("resources/stylesheet.css", "r") as cssfile:
		cssdata = cssfile.read()
	return cssdata


def readprofile(basepath):
	if basepath:
		profilepath = {"yaml": os.path.join(basepath, "profile.yaml"), "yml": os.path.join(basepath, "profile.yml")}
		if isProfileExists(profilepath["yaml"]):
			with open(profilepath["yaml"], "r") as profile_file:
				profile = yaml.load(profile_file)
			return profile
		if isProfileExists(profilepath["yml"]):
			with open(profilepath["yml"], "r") as profile_file:
				profile = yaml.load(profile_file)
			return profile
		else:
			raise IOError("Profile not found")
	else:
		raise IOError("Profile path is empty")


def isProfileExists(profilepath):
	return os.path.isfile(profilepath)


# all the things read from the config.yaml file
configuration = Configuration()
