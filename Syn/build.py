#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.common as c
import Syn.Global as g
import Syn.install
import Syn.s
import Syn.log

import json

import shutil
import os

def build(pack_loc):
	build_config = Syn.s.loadBuildConfigFile()
	meta_config  = Syn.s.loadMetaConfigFile()
	package, version = Syn.s.getVersion()
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

	Syn.s.putenv(g.CONFIG_FLAGS, config_flag_string)
	Syn.s.putenv(g.BUILD_FLAGS,  build_flag_string)
	Syn.s.putenv(g.STAGE_FLAGS,  stage_flag_string)

	Syn.s.putenv(g.CONFIG, build_config['configure'])
	Syn.s.putenv(g.BUILD,  build_config['build'])
	Syn.s.putenv(g.STAGE,  build_config['stage'])

	script = os.path.abspath(g.SYN_BUILDDIR + g.SYN_BUILDDIR_SCRIPT)

	root = Syn.s._tb.getRootFolder()
	c.cd(root)

	Syn.s.putenv(g.DESTDIR, pack_loc  + "/" + g.ARCHIVE_FS_ROOT)
	c.mkdir(pack_loc + "/" + g.ARCHIVE_FS_ROOT)

	Syn.log.l(Syn.log.MESSAGE, "Start Configure")
	c_return = os.system(script + " configure")
	Syn.log.l(Syn.log.MESSAGE, "End Configure")

	if c_return != 0:
		return 1

	Syn.log.l(Syn.log.MESSAGE, "Start Build")
	b_return = os.system(script + " build")
	Syn.log.l(Syn.log.MESSAGE, "End Build")

	if b_return != 0:
		return 2

	Syn.log.l(Syn.log.MESSAGE, "Start Stage")
	s_return = os.system(script + " stage")
	Syn.log.l(Syn.log.MESSAGE, "End Stage")

	if s_return != 0:
		return 3

	return 0

def buildFromSource(pkg_path):
	pack_loc = c.getTempLocation()
	pop_location = os.path.abspath(os.getcwd())

	c.createWorkDir(pack_loc)
	Syn.s.targetTarball(pkg_path)
	Syn.s.extractSource(pack_loc)
	pkg, ver = Syn.s.getVersion()
	c.cd(pkg + "-" + ver)
	Syn.s.targetTarball(pkg + "-" + ver + ".tar.gz")
	Syn.s.extractSource(pack_loc, pkg + "-" + ver)
	c.cd(pkg + "-" + ver)
	if build(pack_loc) == 0:
		c.cd(pack_loc)

		shutil.copyfile(
			pack_loc + pkg + "-" + ver + "/" + g.SYN_BUILDDIR + g.SYN_BUILDDIR_META,
			pack_loc + g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_META
		)

		files = Syn.s.md5sumwd(pack_loc + "/" + g.ARCHIVE_FS_ROOT)

		output = json.dumps(
			files,
			sort_keys = True,
			indent    = 4
		)

		f = open(g.ARCHIVE_FS_ROOT + "/" + g.SYN_FILESUMS, 'w')
		f.write(output)
		f.close()

		Syn.s.tarup(
			g.ARCHIVE_FS_ROOT,
			pack_loc + "/" + pkg + "-" + ver + "." + g.BIN_PKG
		)
		shutil.move(
			pack_loc + "/" + pkg + "-" + ver + "." + g.BIN_PKG,
			pop_location
		)
	else:
		Syn.log.l(Syn.log.CRITICAL, "FTBFS DETECTED")

	shutil.rmtree(pack_loc + g.ARCHIVE_FS_ROOT)
	shutil.rmtree(pack_loc + pkg + "-" + ver)

	c.removeWorkDir()
