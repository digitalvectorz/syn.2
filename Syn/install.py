#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import os.path
import Syn.log
import Syn.db
import Syn.Global as g
import Syn.common as c
import Syn.s

import shutil

def install(pathorig):
	path = os.path.abspath(pathorig)

	meta = Syn.s.metadump(path)
	pkg = meta['package']
	ver = meta['version']

	Syn.log.l(Syn.log.MESSAGE, "%s (version) %s" % ( pkg, ver ))
	Syn.log.l(Syn.log.PEDANTIC, "Loading DB")

	db = Syn.db.loadCanonicalDB()
	status = db.queryState(pkg, ver)
	Syn.log.l(Syn.log.MESSAGE, "Package is currently set as: " + status['status'])

	if status['status'] == Syn.db.UNINSTALLED:
		status['status'] = Syn.db.HALF_INSTALLED
		db.setState(pkg, ver, status)
		db.writeout()

		Syn.log.l(Syn.log.PEDANTIC, str(status))
		Syn.log.l(Syn.log.MESSAGE, "Installing version %s of %s" % ( ver, pkg ))

		c.cd(g.INSTALL_ROOT_PATH)

		archive = Syn.tarball.us_tb()
		archive.target(path)

		try:
			c.mkdir(pkg)
		except OSError:
			Syn.log.l(Syn.log.PEDANTIC, "we have a version of bash installed")
		c.cd(pkg)

		try:
			c.mkdir(ver)
		except OSError:
			status['status'] = Syn.db.BORKED
			db.setState(pkg, ver, status)
			db.writeout()

			Syn.log.l(Syn.log.CRITICAL, "Package exists in syn!")
			Syn.log.l(Syn.log.CRITICAL, "Can *NOT* continue!")
			return -1

		c.cd(ver)
		archive.extractall(".")
		shutil.move(
			g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_META,
			g.SYN_XTRACT_META,
		)
		status['status'] = Syn.db.INSTALLED
		db.setState(pkg, ver, status)
		db.writeout()
		Syn.log.l(Syn.log.MESSAGE, "Installed Returning happy.")

		return 0
	else:
		Syn.log.l(Syn.log.CRITICAL, "Package is not uninstalled!!")
		return 1
