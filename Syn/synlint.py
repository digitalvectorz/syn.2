#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.tarball as t
import Syn.log     as l
import Syn.Global  as g
import Syn.policy


def checkFields(attrs, meta):
	errs = 0
	for a in attrs:
		try:
			good = meta[a]
		except KeyError as e:
			print "================================================================================"
			print "          Missing Field: " + a
			print "================================================================================"
			print Syn.policy.DESCRS[a]
			errs += 1
	return errs

def sourceCheck( ar ):
	metafile = ar.getConf(g.SYN_SRC_DIR + g.SYN_BUILDDIR_META)

	r_errs = checkFields(Syn.policy.META_REQUIRED,   metafile)
	n_errs = checkFields(Syn.policy.META_NEEDED,     metafile)
	g_errs = checkFields(Syn.policy.META_GOODTOHAVE, metafile)

	return ( r_errs, n_errs, g_errs )


def binaryCheck( ar ):
	metafile = ar.getConf(g.SYN_BINARY_META)

	r_errs = checkFields(Syn.policy.META_REQUIRED,   metafile)
	n_errs = checkFields(Syn.policy.META_NEEDED,     metafile)
	g_errs = checkFields(Syn.policy.META_GOODTOHAVE, metafile)

	return ( r_errs, n_errs, g_errs )


def runCheck(tarbal): # We're going to do a stricter check
	try:
		ar = t.archive(tarbal, verify = False)
		if ar.getClass() == t.BINARY:
			( r_errs, n_errs, g_errs ) = binaryCheck(ar)
		elif ar.getClass() == t.SOURCE:
			( r_errs, n_errs, g_errs ) = sourceCheck(ar)
		else:
			l.l(l.CRITICAL,"WTF Is this I don't even")
			return -1

		sane  = False
		clean = False

		if r_errs + n_errs == 0:
			sane  = True
			clean = True

		if r_errs == 0:
			sane = True

		l.l(l.MESSAGE,"Errors:")
		l.l(l.MESSAGE,"")
		l.l(l.MESSAGE,"    Serious:  " + str(r_errs))
		l.l(l.MESSAGE,"  Important:  " + str(n_errs))
		l.l(l.MESSAGE,"   Pedantic:  " + str(g_errs))
		l.l(l.MESSAGE,"")

		if clean:
			l.l(l.MESSAGE,"This package is acceptable to build. Check with")
			l.l(l.MESSAGE," your friendly project developer about it's archive")
			l.l(l.MESSAGE," status.")
			l.l(l.MESSAGE,"")
		elif sane:
			l.l(l.MESSAGE,"This package is acceptable for basic, unofficial use.")
			l.l(l.MESSAGE," It's not in shipp-able format, but it's OK to use")
			l.l(l.MESSAGE," locally.")
			l.l(l.MESSAGE,"")
		else:
			l.l(l.MESSAGE,"This package is *NOT* acceptable for something as")
			l.l(l.MESSAGE," simple as a simple install. Please fix the issues above.")
			l.l(l.MESSAGE,"")

	except Syn.errors.SynException as e:
		l.l(l.CRITICAL, str(e))
