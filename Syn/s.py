import Syn.upstream_tarball
import Syn.log

import Syn.common as c
import Syn.Global as g

import os.path
import os

import json

def targetUpstream(tar):
	global _tb
	global _tb_dir

	_tb_dir = os.path.dirname(os.path.abspath(tar))

	_tb = Syn.upstream_tarball.us_tb()
	_tb.target(tar);

def getVersion():
	global _tb

	try:
		root = _tb.getRootFolder()
		package, version = Syn.common.processFullID(root)
		Syn.log.l(Syn.log.VERBOSE, "Processing package   `%s'" % package)
		Syn.log.l(Syn.log.VERBOSE, "Version processed as `%s'" % version)
		return [package, version]
	except NameError as e:
		raise NameError("Package not set")

def template():
	package, version = getVersion()
	Syn.common.cd(_tb_dir)
	if os.path.exists("synd"):
		raise IOError("Synd Exists!")
	else:
		Syn.common.mkdir("synd")

def loadBuildConfigFile():
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_CONFIG)
	conf_file = f.read()
	return json.loads(conf_file)

def putenv(key, value):
	Syn.log.l(Syn.log.VERBOSE, "%s = %s" % (key, value))
	# print "export " + key + "=\"" + value + "\""
	os.putenv(key, value)

def build():
	build_config = loadBuildConfigFile()

	config_flag_string = ""
	build_flag_string  = ""
	stage_flag_string  = ""

	for flag in build_config['ConfigFlags']:
		config_flag_string += flag + " "

	for flag in build_config['BuildFlags']:
		build_flag_string += flag + " "

	for flag in build_config['StageFlags']:
		stage_flag_string += flag + " "

	putenv(g.CONFIG_FLAGS, config_flag_string)
	putenv(g.BUILD_FLAGS,  build_flag_string)
	putenv(g.STAGE_FLAGS,  stage_flag_string)

	putenv(g.CONFIG, build_config['configure'])
	putenv(g.BUILD,  build_config['build'])
	putenv(g.STAGE,  build_config['stage'])

	script = os.path.abspath(g.SYN_BUILDDIR + g.SYN_BUILDDIR_SCRIPT)

	root = _tb.getRootFolder()
	os.chdir(root)

	pack_loc = c.getTempLocation()
	c.createWorkDir(pack_loc)

	putenv(g.DESTDIR, pack_loc  + "/" + g.ARCHIVE_FS_ROOT)
	c.mkdir(pack_loc + "/" + g.ARCHIVE_FS_ROOT)

	Syn.log.l(Syn.log.MESSAGE, "Start Configure")
	os.system(script + " configure")
	Syn.log.l(Syn.log.MESSAGE, "End Configure")

	Syn.log.l(Syn.log.MESSAGE, "Start Build")
	os.system(script + " build")
	Syn.log.l(Syn.log.MESSAGE, "End Build")

	Syn.log.l(Syn.log.MESSAGE, "Start Stage")
	os.system(script + " stage")
	Syn.log.l(Syn.log.MESSAGE, "End Stage")

	# c.removeWorkDir()

