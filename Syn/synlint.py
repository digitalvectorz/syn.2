#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.tarball as t
import Syn.log     as l


def checkFields(attrs, meta):
	pass

def runCheck(tarball, verify = False ): # We're going to do a stricter check
	try:
		ar = t.archive(tarball)
		metafile = ar.getConf(g.SYN_SRC_DIR + g.SYN_BUILDDIR_META])
		
	except Syn.errors.SynException as e:
		l.l(l.CRITICAL, str(e))
