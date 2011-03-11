#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global  as g
import Syn.log     as l
import Syn.common  as c
import Syn.tarball as t
import Syn.s

import commands
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

def run(cmd):
	return commands.getstatusoutput(cmd)

def callScript(script):
	Syn.log.l(Syn.log.CRITICAL, "Start Configure")
	(c_return, clog) = run(script + " configure")
	Syn.log.l(Syn.log.CRITICAL, "End Configure")

	if c_return != 0:
		return (1, clog, None, None)

	Syn.log.l(Syn.log.CRITICAL, "Start Build")
	(b_return, blog) = run(script + " build")
	Syn.log.l(Syn.log.CRITICAL, "End Build")

	if b_return != 0:
		return (2, clog, blog, None)

	Syn.log.l(Syn.log.CRITICAL, "Start Stage")
	(s_return, slog) = run(script + " stage")
	Syn.log.l(Syn.log.CRITICAL, "End Stage")

	if s_return != 0:
		return (3, clog, blog, slog)

	return (0, clog, blog, slog)

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
	l_pth = pkg + "-" + ver + "." + g.SYN_LOG_PKG_XTN

	ar = t.newArchive(
		[ g.ARCHIVE_FS_ROOT ],
		b_pth,
		t.BINARY
	)

	( r_errs, n_errs, g_errs ) = Syn.synlint.runCheck(b_pth)

	errs  = "Errors (on the binary)\n"
	errs += "\n"
	errs += "Report for:"
	errs += " " + pkg + "-" + ver
	errs += "\n"
	errs += "    Serious:  " + str(r_errs) + "\n"
	errs += "  Important:  " + str(n_errs) + "\n"
	errs += "   Pedantic:  " + str(g_errs) + "\n"
	errs += "\n"

	logLog("./", "synlint", errs)

	ar = t.newArchive(
		[ g.LOG_FS_ROOT ],
		l_pth,
		t.UNKNOWN
	)

	return ( b_pth, l_pth )

def logLog(root, logname, text):
	header  = "********************************************************************************\n"
	header += "    " + logname + "\n"
	header += "********************************************************************************\n"
	header += "\n"

	text = header + text

	fd = open(root + "/" + g.LOG_FS_ROOT + logname, 'w')
	fd.write(text)
	fd.close()

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

	download = ar.getConf(g.SYN_SRC_DIR + g.SYN_BUILDDIR_META)['download']
	sourceball = os.path.basename(download)

	upstream_archive = t.archive(sourceball)
	upstream_archive.extractall()

	c.cd(upstream_archive.getRootFolder())

	setupBuildEnv(ar)

	Syn.s.putenv(g.DESTDIR, root + "/" + g.ARCHIVE_FS_ROOT)
	c.mkdir(root + "/" + g.ARCHIVE_FS_ROOT)
	c.mkdir(root + "/" + g.LOG_FS_ROOT)

	try:
		( scriptStatus, clog, blog, slog ) = callScript(script)

		logLog(root, "configure", clog)
		logLog(root, "build",     blog)
		logLog(root, "stage",     slog)

		if scriptStatus != 0:
			l.l(l.CRITICAL,"*****")
			l.l(l.CRITICAL,"FTBFS DETECTED!!!")
			l.l(l.CRITICAL,"*****")
			raise Syn.errors.BuildFailureException("FTBFS")
	except KeyboardInterrupt as e:
		raise Syn.errors.BuildFailureException("User abort.")

	c.cd("..")

	( binary, log ) = package(metainf)

	return ( binary, log )
