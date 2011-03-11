#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.tarball as t
import Syn.log     as l
import Syn.Global  as g
import Syn.policy


def checkFields(attrs, meta):
	for a in attrs:
		try:
			good = meta[a]
		except KeyError as e:
			print "================================================================================"
			print "          Missing Field: " + a
			print "================================================================================"
			print Syn.policy.DESCRS[a]

def runCheck(tarbal, verify = False ): # We're going to do a stricter check
	try:
		ar = t.archive(tarbal)
		if ar.getClass() != t.BINARY:
			l.l(l.CRITICAL,"Must be a binary package")
			return -1

		metafile = ar.getConf(g.SYN_BINARY_META)

		checkFields(Syn.policy.META_REQUIRED,   metafile)
		checkFields(Syn.policy.META_NEEDED,     metafile)
		checkFields(Syn.policy.META_GOODTOHAVE, metafile)

	except Syn.errors.SynException as e:
		l.l(l.CRITICAL, str(e))
