#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global  as g
import Syn.log     as l
import Syn.common  as c
import Syn.tarball as t
import Syn.s

import json
import os

def readConfFile(f):
	l.l(l.PEDANTIC,"Reading Conf: " + f)
	meta = open(f)
	return json.loads(meta.read())

def setupBuildEnv(ar):
	build_config = ar.getConf(g.SYN_SRC_DIR + g.SYN_BUILDDIR_CONFIG)

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

def callScript(script):
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

def package(metainf):
	for x in g.SYN_SRC_TO_BIN_FILESPEC:
		c.cp(x, "../" + g.SYN_SRC_TO_BIN_FILESPEC[x])

	c.cd("..")
	files = c.md5sumwd(g.ARCHIVE_FS_ROOT_NOSLASH)
	output = json.dumps(files, sort_keys = True, indent = 4)
	f = open(g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_FILESUMS, 'w')
	f.write(output)
	f.close()

	pkg = metainf['package']
	ver = metainf['version']

	b_pth = pkg + "-" + ver + "." + g.SYN_BIN_PKG_XTN

	ar = t.newArchive(
		[ g.ARCHIVE_FS_ROOT ],
		b_pth,
		t.BINARY
	)

	return b_pth

def build(ar):
	l.l(l.PEDANTIC,"Extracting archive")
	ar.extractall()
	l.l(l.PEDANTIC,"Archive extracted")

	root = os.path.abspath(os.getcwd())
	l.l(l.PEDANTIC,"Current root: %s" % ( root ))

	metainf = ar.getConf(g.SYN_SRC_DIR + g.SYN_BUILDDIR_META)

	pkg = metainf['package']
	ver = metainf['version']

	script = os.path.abspath(
		pkg + "-" + ver + "/" + g.SYN_SRC_DIR + g.SYN_BUILDDIR_SCRIPT
	)

	l.l(l.PEDANTIC,
		"Maintainer is %s <%s>" % (
			metainf['maintainer']['name'],
			metainf['maintainer']['email']
		)
	)

	l.l(l.PEDANTIC,"Building %s version %s" % ( pkg, ver ))

	c.cd(pkg + "-" + ver)

	upstream_archive = t.archive(pkg + "-" + ver + ".tar.gz") #XXX: Fixme
	upstream_archive.extractall()

	c.cd(pkg + "-" + ver)

	setupBuildEnv(ar)

	Syn.s.putenv(g.DESTDIR, root + "/" + g.ARCHIVE_FS_ROOT)
	c.mkdir(root + "/" + g.ARCHIVE_FS_ROOT)

	if callScript(script) != 0:
		l.l(l.CRITICAL,"*****")
		l.l(l.CRITICAL,"FTBFS DETECTED!!!")
		l.l(l.CRITICAL,"*****")
		raise Syn.errors.BuildFailureException("FTBFS")
	c.cd("..")

	binary = package(metainf)

	return binary
