#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.common  as c
import Syn.tarball as t
import Syn.Global  as g
import Syn.log     as l

import os.path
import os

def bundleSource(directory):
	abspath = os.path.abspath(directory)
	pkgdir  = os.path.basename(abspath)

	c.cd(directory)
	c.cd("..")

	pkgname = str(pkgdir + "." + g.SYN_SRC_PKG_XTN)

	t.newArchive(
		[pkgdir],
		pkgname,
		t.SOURCE
	)

	return pkgname
