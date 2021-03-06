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

import os

FORCE=True

def linkPkg(pkg, ver):
	root = "/"

	db = Syn.db.loadCanonicalDB()

	if Syn.reg.CHROOT != root:
		Syn.log.l(Syn.log.PEDANTIC,"Dumping into chroot for real (%s)" % Syn.reg.CHROOT)
		os.chroot(Syn.reg.CHROOT)
		Syn.log.l(Syn.log.PEDANTIC,"Swaping chroot out to /")
		Syn.reg.CHROOT = "/"
		Syn.reg.CHROOT_TOUCHED = True
		Syn.log.l(Syn.log.PEDANTIC,"Re-loading DB")
		db = Syn.db.loadCanonicalDB()

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
		fpkg = Syn.fspkg.fspkg(pkg, ver)
		fslist = fpkg.getAllFiles()
		errors = 0

		for f in fslist:
			filespec = f[len(g.ARCHIVE_FS_ROOT):]
			if c.xists(root + filespec):
				Syn.log.l(Syn.log.LOG, "File in confict! %s" % filespec)
				errors += 1

		if errors != 0:
			raise Syn.errors.ConflictException("Link conflicts!")

		db.setState(pkg,ver,Syn.db.HALF_LINKED)
		db.sync()

		for f in fslist:
			pkg_root = fpkg.getInstallPath()
			fs_root  = root
			filespec = f[len(g.ARCHIVE_FS_ROOT):]
			c.fs_ln_inst(pkg_root + f, root + filespec)

		db.setLinked(pkg,ver)
		db.sync()

def unlinkPkg(pkg, ver):

	root="/"

	db = Syn.db.loadCanonicalDB()

	if Syn.reg.CHROOT != root:
		Syn.log.l(Syn.log.PEDANTIC,"Dumping into chroot for real (%s)" % Syn.reg.CHROOT)
		os.chroot(Syn.reg.CHROOT)
		Syn.log.l(Syn.log.PEDANTIC,"Swaping chroot out to /")
		Syn.reg.CHROOT = "/"
		Syn.reg.CHROOT_TOUCHED = True
		Syn.log.l(Syn.log.PEDANTIC,"Re-loading DB")
		db = Syn.db.loadCanonicalDB()

	Syn.log.l(Syn.log.MESSAGE, "Uninking " + pkg + ", version " + ver)
	status = db.queryState(pkg,ver)

	Syn.log.l(Syn.log.VERBOSE, "Status: %s" % status['status'])

	if status['status'] != Syn.db.LINKED:
		Syn.log.l(Syn.log.CRITICAL, "Package is not linked. Damnit!")
		raise Syn.errors.PackageNotinstalledException("Not linked: %s version %s" % (pkg, ver))
	else:
		status = db.queryGState(pkg)

		if status['linked'] != ver:
			Syn.log.l(Syn.log.LOG, "Different version linked!")
			raise Syn.errors.ConflictException("Different version Linked")

		Syn.log.l(Syn.log.LOG, "Package is linked. We can unlink it!")
		fpkg = Syn.fspkg.fspkg(pkg, ver)
		fslist = fpkg.getAllFiles()
		errors = 0

		for f in fslist:
			filespec = f[len(g.ARCHIVE_FS_ROOT):]
			if c.xists(root + filespec) and not c.isln(root + filespec):
				Syn.log.l(Syn.log.LOG, "Errorful: %s" % filespec)
				errors += 1

		if errors != 0:
			Syn.log.l(Syn.log.LOG, "Errors found :(")
			raise Syn.errors.ConflictException("Link conflicts!")

		db.setState(pkg,ver,Syn.db.HALF_LINKED)
		db.sync()

		for f in fslist:
			filespec = f[len(g.ARCHIVE_FS_ROOT):]
			#try:
			c.fs_unln_inst(root+filespec)
			#except OSError as e:
			#	Syn.log.l(Syn.log.LOG, "OS Error: %s" % str(e))

		db.setUnlinked(pkg,ver)
		db.sync()

def forceUnlinkHalfLinkedPkg(pkg, ver):

	root="/"

	db = Syn.db.loadCanonicalDB()

	if Syn.reg.CHROOT != root:
		Syn.log.l(Syn.log.PEDANTIC,"Dumping into chroot for real (%s)" % Syn.reg.CHROOT)
		os.chroot(Syn.reg.CHROOT)
		Syn.log.l(Syn.log.PEDANTIC,"Swaping chroot out to /")
		Syn.reg.CHROOT = "/"
		Syn.reg.CHROOT_TOUCHED = True
		Syn.log.l(Syn.log.PEDANTIC,"Re-loading DB")
		db = Syn.db.loadCanonicalDB()

	Syn.log.l(Syn.log.MESSAGE, "Uninking " + pkg + ", version " + ver)
	status = db.queryState(pkg,ver)

	Syn.log.l(Syn.log.VERBOSE, "Status: %s" % status['status'])

	if status['status'] != Syn.db.HALF_LINKED:
		Syn.log.l(Syn.log.CRITICAL, "Package is not half-linked. Damnit!")
		raise Syn.errors.PackageNotinstalledException("Not half-linked: %s version %s" % (pkg, ver))
	else:
		fpkg = Syn.fspkg.fspkg(pkg, ver)
		fslist = fpkg.getAllFiles()
		errors = 0

		for f in fslist:
			filespec = f[len(g.ARCHIVE_FS_ROOT):]
			if c.xists(root + filespec) and not c.isln(root + filespec):
				Syn.log.l(Syn.log.LOG, "Errorful: %s" % filespec)
				errors += 1

		if errors != 0:
			Syn.log.l(Syn.log.LOG, "Errors found :(")
			Syn.log.l(Syn.log.LOG, "We're going to plow through.")

		for f in fslist:
			filespec = f[len(g.ARCHIVE_FS_ROOT):]
			try:
				c.fs_unln_inst(root+filespec)
			except OSError as e:
				Syn.log.l(Syn.log.LOG, "OS Error: %s" % str(e))
				Syn.log.l(Syn.log.LOG, "Ignoring.")

		db.setUnlinked(pkg,ver)
		db.sync()
