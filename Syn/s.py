#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.common  as c
import Syn.tarball as t
import Syn.log     as l
import Syn.build

import os

def putenv(key, value):
	Syn.log.l(Syn.log.VERBOSE, "%s = %s" % (key, value))
	os.putenv(key, value)

def buildSourcePackage(package):
	ar = t.archive(package)
	klass = ar.getClass()

	pop = os.path.abspath(os.getcwd())

	if klass != t.SOURCE:
		l.l(l.CRITICAL,"Archive is not a source package")
		return -1
	
	l.l(l.PEDANTIC,"Archive is sourceful. May continue")

	build_root = c.getTempLocation()
	c.mkdir(build_root)
	c.cd(build_root)

	try:
		build = Syn.build.build(ar)
		c.cp(build, pop + "/" + build)

	except BuildFailureException as e:
		l.l(l.CRITICAL,"Failure to build!")
		l.l(l.CRITICAL,str(e))

	c.rmdir(build_root)
	return return_value

