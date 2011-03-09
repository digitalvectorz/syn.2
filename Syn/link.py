#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global  as g
import Syn.log     as l
import Syn.common  as c
import Syn.tarball as t
import Syn.fspkg
import Syn.errors
import Syn.db

def linkPkg(pkg, ver, root="/"):
	Syn.log.l(Syn.log.MESSAGE, "Linking " + pkg + ", version " + ver)
	db = Syn.db.loadCanonicalDB()
	status = db.queryState(pkg,ver)

	if status['status'] != Syn.db.INSTALLED:
		Syn.log.l(Syn.log.CRITICAL, "Package is not installed. Damnit!")
		raise Syn.errors.PackageNotinstalledException("Not installed: %s version %s" % (pkg, ver))
	else:
		status = db.queryGState(pkg)

		if status['linked'] != None:
			Syn.log.l(Syn.log.LOG, "Different version linked!")
			raise Syn.errors.ConflictException("Different version Linked")

		Syn.log.l(Syn.log.LOG, "Package is installed. We can link it!")
		pkg = Syn.fspkg.fspkg(pkg, ver)
		fslist = pkg.getAllFiles()
		for f in fslist:
			errors = 0
			filespec = f[len(g.ARCHIVE_FS_ROOT):]
			if c.xists(root + filespec):
				Syn.log.l(Syn.log.LOG, "File in confict! %s" % filespec)
				errors += 1

		if errors != 0:
			raise Syn.errors.ConflictException("Link conflicts!")

