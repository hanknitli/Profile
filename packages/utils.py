import shutil
import sys
import os
import errno
import time

import git
import yaml

exec(open("packages/constants.py").read())


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
		self.setconfig(self.readconfig())

	def isConfFileExists(self):
		return os.path.isfile(self.configfile)

	def createConfFile(self):
		default_config = self.getDefaultConfig()
		try:
			os.makedirs(os.path.dirname(self.configfile))

		except OSError as reason:
			if reason.errno != errno.EEXIST:
				raise Exception('Unknown Error')

		with open(self.configfile, "w") as config:
			yaml.dump(default_config, config, default_flow_style=False)

	def getDefaultConfig(self):
		with open("resources/default_config.yaml", "r") as default_configfile:
			config = yaml.load(default_configfile)

		if sys.platform == "win32":
			logfile = config["logfile"]["Windows"]
			basepath = os.getenv(config["profilepath"]["Windows"])
			profilepath = os.path.join(basepath, parent_windows, __project_name__, "Resources")

		elif sys.platform == "linux2":
			basepath = os.path.expanduser(config["logfile"]["Linux"])
			logfile = os.path.join(basepath, parent_linux, __project_name__, "log.txt")

			basepath = os.path.expanduser((config["profilepath"]["Linux"]))
			profilepath = os.path.join(basepath, parent_linux, __project_name__, ".profile")

		showtoolbar = config["showtoolbar"]
		expandedTree = config["expandedTree"]
		scrollbar = config["scrollbar"]

		default_config = {"logfile": logfile, "showtoolbar": showtoolbar, "profilepath": profilepath, \
						  "expandedTree": expandedTree, "scrollbar": scrollbar}
		return default_config

	def readconfig(self):
		if not self.isConfFileExists():
			self.createConfFile()
			return self.getDefaultConfig()

		else:
			with open(self.configfile, "r") as config:
				data = yaml.load(config)
			return data

	def updateConfFile(self, setToDefault=False):
		if not self.isConfFileExists():
			self.createConfFile()

		elif setToDefault:
			default_config = self.getDefaultConfig()
			with open(self.configfile, "w") as config:
				yaml.dump(default_config, config, default_flow_style=False)

		else:
			config_data = self.getconfig()
			with open(self.configfile, "w") as config:
				yaml.dump(config_data, config, default_flow_style=False)

	def getconfig(self):
		config = {"logfile": self.logfile, "showtoolbar": self.showtoolbar, "profilepath": self.profilepath, \
				  "expandedTree": self.expandedTree, "scrollbar": self.scrollbar}

		return config

	def setconfig(self, config_data):
		self.logfile = config_data["logfile"]
		self.showtoolbar = config_data["showtoolbar"]
		self.profilepath = config_data["profilepath"]
		self.expandedTree = config_data["expandedTree"]
		self.scrollbar = config_data["scrollbar"]

	def setDefaultConfigProperty(self, key):
		default_config = configuration.getDefaultConfig()
		config_data = self.getconfig()
		config_data[key] = default_config[key]
		self.setconfig(config_data)
		self.updateConfFile()

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
			if isYAMLSane(profilepath["yaml"]):
				with open(profilepath["yaml"], "r") as profile_file:
					profile = yaml.load(profile_file)
				return profile
			else:
				raise IOError("Profile corrupted")

		elif isProfileExists(profilepath["yml"]):
			if isYAMLSane(profilepath["yml"]):
				with open(profilepath["yml"], "r") as profile_file:
					profile = yaml.load(profile_file)
				return profile
			else:
				raise IOError("Profile corrupted")

		else:
			raise IOError("Profile not found")
	else:
		raise IOError("Profile path is empty")


def isProfileExists(profilepath):
	return os.path.isfile(profilepath)


def isYAMLSane(profilepath):
	return True  # TODO check the sanity of profile.yaml file


def parseGit(gitpath):
	cleanProfileDir(True)
	repo = git.Repo.init(configuration.profilepath)
	origin = repo.create_remote('origin', gitpath)
	origin.fetch()
	origin.pull(origin.refs[0].remote_head)


def cleanProfileDir(fullclean=False):
	try:
		base = configuration.profilepath
		for content in os.listdir(base):
			if fullclean:
				entry = os.path.join(base, content)
				if os.path.isfile(entry):
					os.remove(entry)
				else:
					shutil.rmtree(entry, ignore_errors=False, onerror=caughtError)
			elif content == ".git":
				shutil.rmtree(os.path.join(base, ".git"), ignore_errors=False, onerror=caughtError)

	except OSError as reason:
		print(reason)
		pass  # TODO log the error in log.txt


def caughtError(func, path, exc):
	if sys.platform == "win32":
		os.system('rmdir /S /Q "{}" > nul 2> nul'.format(path))
	elif sys.platform == "linux2":
		os.system('rm -rdf {} > /dev/null 2> /dev/null'.format(path))


# all the things read from the config.yaml file
configuration = Configuration()
