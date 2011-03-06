#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.tarball
import Syn.common as c
import Syn.Global as g
import Syn.log

import tarfile
import os.path
import shutil
import json
import os

def targetTarball(tar):
	global _tb
	global _tb_dir
	_tb_dir = os.path.dirname(os.path.abspath(tar))
	_tb = Syn.tarball.us_tb()
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

def putenv(key, value):
	Syn.log.l(Syn.log.VERBOSE, "%s = %s" % (key, value))
	# print "export " + key + "=\"" + value + "\""
	os.putenv(key, value)

def loadBuildConfigFile():
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_CONFIG)
	conf_file = f.read()
	return json.loads(conf_file)

def loadMetaConfigFile():
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_META)
	conf_file = f.read()
	return json.loads(conf_file)

def writeMetafile(frobernate):
	output = json.dumps(
		frobernate,
		sort_keys = True,
		indent    = 4
	)
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_META, 'w')
	f.write(output)
	f.close()

def extractSource(pack_loc, path="."):
	global _tb
	try:
		c.cd(pack_loc)
		root = _tb.getRootFolder()		
		_tb.extractall(path)
	except NameError as e:
		raise NameError("Package not set")

def tarup( directory, outputname ):
	tarball_target = tarfile.open(outputname, "w|gz")
	tarball_target.add(directory)
	tarball_target.close()

def buildFromSource(pkg_path):
	pack_loc = c.getTempLocation()
	pop_location = os.path.abspath(os.getcwd())

	c.createWorkDir(pack_loc)
	targetTarball(pkg_path)
	extractSource(pack_loc)
	pkg, ver = getVersion()
	c.cd(pkg + "-" + ver)
	targetTarball(pkg + "-" + ver + ".tar.gz")
	extractSource(pack_loc, pkg + "-" + ver)
	c.cd(pkg + "-" + ver)
	build(pack_loc)
	c.cd(pack_loc)

	shutil.copyfile(
		pack_loc + pkg + "-" + ver + "/" + g.SYN_BUILDDIR + g.SYN_BUILDDIR_META,
		pack_loc + g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_META
	)
	tarup(
		g.ARCHIVE_FS_ROOT,
		pack_loc + "/" + pkg + "-" + ver + "." + g.BIN_PKG
	)

	shutil.rmtree(pack_loc + g.ARCHIVE_FS_ROOT)
	shutil.rmtree(pack_loc + pkg + "-" + ver)
	shutil.move(
		pack_loc + "/" + pkg + "-" + ver + "." + g.BIN_PKG,
		pop_location
	)

	c.removeWorkDir()

def metadump(filezor):
	tarball_target = tarfile.open(filezor, "r")
	metafile = g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_META
	tarinfo = tarball_target.getmember(metafile)
	if tarinfo.isfile():
		meta = tarball_target.extractfile(metafile)
		metadata = json.loads(meta.read())
	else:
		raise KeyError("Bum file")
	tarball_target.close()
	return metadata

def build(pack_loc):
	build_config = loadBuildConfigFile()
	meta_config  = loadMetaConfigFile()
	package, version = getVersion()
	pkg = meta_config['package']
	ver = meta_config['version']
	if package != pkg:
		raise KeyError("Package metafile does not match tarball!")
	else:
		Syn.log.l(Syn.log.VERBOSE, "package matches conf")
	if version != ver:
		Syn.log.l(Syn.log.MESSAGE, "Version does not match. Resetting metafile's conf")
		meta_config['version'] = version
		writeMetafile(meta_config)
	else:
		Syn.log.l(Syn.log.VERBOSE, "Version matches conf")

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

def install(pathorig):
	path = os.path.abspath(pathorig)

	meta = metadump(path)
	pkg = meta['package']
	ver = meta['version']

	Syn.log.l(Syn.log.MESSAGE, "Installing version %s of %s" % ( ver, pkg ))
	c.cd(g.INSTALL_ROOT_PATH)

	archive = Syn.tarball.us_tb()
	archive.target(path)

	try:
		c.mkdir(pkg)
	except OSError:
		pass # it's ok to have a pkg
		#      installed. just not ver
	c.cd(pkg)

	try:
		c.mkdir(ver)
	except OSError:
		Syn.log.l(Syn.log.CRITICAL, "Package exists in syn!")
		Syn.log.l(Syn.log.CRITICAL, "Can *NOT* continue!")
		return -1
	c.cd(ver)

	archive.extractall(".")

	shutil.move(
		g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_META,
		g.SYN_XTRACT_META,
	)

	return 0
