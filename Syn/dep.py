#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.fspkg
import Syn.db
import Syn.s as syn

def getDBDeps(pkg):
	db  = Syn.db.loadCanonicalDB()
	ver = db.getLatestVersion(pkg)
	return getDBDepsV(pkg, ver)

def getDBDepsV(pkg, version):
	pkg = Syn.fspkg(pkg, version)
	print pkg.getSumFile()

def getDeps(archive):
	try:
		info = syn.getBinaryMetadata(archive)
		ret = {}

		for x in info['deps']:
			ret[x] = x
			louielouie = getDBDeps(x)

	except Syn.errors.InvalidArchiveException as e:
		l.l(l.CRITICAL,str(e))

