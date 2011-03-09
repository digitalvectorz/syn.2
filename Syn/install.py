#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global  as g
import Syn.log     as l
import Syn.common  as c
import Syn.tarball as t
import Syn.errors
import Syn.db

def installArchive(ar):
	if ar.getClass() != t.BINARY:
		raise Syn.errors.InvalidArchiveException(
			"Need a binary package to install"
		)

	metainf = ar.getConf(g.SYN_BINARY_META)
	pkg = metainf['package']
	ver = metainf['version']
	l.l(l.LOG,"Installing package %s, version %s" % (pkg, ver))

	db = Syn.db.loadCanonicalDB()

	try:
		state = db.queryState(pkg, ver)
		l.l(l.LOG,"Oh shit. We have a hit on this package")
		if state['status'] != Syn.db.UNINSTALLED:
			raise Syn.errors.PackageInstalledException("Package already in the DB. Please purge")
		l.l(l.LOG,"Package is uninstalled. Phew.")
	except Syn.errors.PackageNotFoundException as e:
		l.l(l.LOG,"Package not found. Good. We may continue.")
		db.registerNewPackage(pkg, ver, Syn.db.UNINSTALLED)
		db.sync()

	l.l(l.LOG,"Moving on with the package install")

	# XXX: Someone fix below this, please.
	#      use Syn.fspkg.fspkg()

	c.cd(g.INSTALL_ROOT_PATH)
	if not c.xists(pkg):
		c.mkdir(pkg)
	c.cd(pkg)

	db.setState(pkg,ver,Syn.db.HALF_INSTALLED)
	db.sync()

	if c.xists(ver):
		raise Syn.errors.PackageInstalledException("Package already in the FS. Please purge")

	c.mkdir(ver)
	c.cd(ver)

	# XXX: Above this

	ar.extractall()
	
	for path in g.SYN_BIN_TO_XTRACT:
		c.mv(path, g.SYN_BIN_TO_XTRACT[path])

	db.setState(pkg,ver,Syn.db.INSTALLED)
	db.sync()
