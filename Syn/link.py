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

def linkPkg(pkg, ver):
	Syn.log.l(Syn.log.MESSAGE, "Linking " + pkg + ", version " + ver)
	db = Syn.db.loadCanonicalDB()
	status = db.queryState(pkg,ver)

	if status['status'] != Syn.db.INSTALLED:
		Syn.log.l(Syn.log.CRITICAL, "Package is not installed. Damnit!")
		raise Syn.errors.PackageNotinstalledException("Not installed: %s version %s" % (pkg, ver))
	else:
		Syn.log.l(Syn.log.LOG, "Package is installed. We can link it!")
