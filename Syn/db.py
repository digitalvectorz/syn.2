#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global as g
import Syn.log
import Syn.reg

import pickle

UNINSTALLED    = "U"
BORKED         = "B"
HALF_INSTALLED = "H"
INSTALLED      = "I"
HALF_LINKED    = "K"
LINKED         = "L"
REMOVED        = "R"

HR_STATE = {
	INSTALLED       : "Installed",
	HALF_INSTALLED  : "Half-installed",
	LINKED          : "Linked",
	REMOVED         : "Removed",
	BORKED          : "Borked",
	HALF_LINKED     : "Half-linked",
	UNINSTALLED     : "Uninstalled"
}

class SynDB:
	_database = {}

	def queryState(self, package, version):
		Syn.log.l(Syn.log.PEDANTIC, "Checking on %s (%s)" % ( package, version ))
		try:
			return self._database[package]["installed"][version]
		except KeyError as e:
			raise Syn.errors.PackageNotFoundException("No package found")

	def queryGState(self, package ):
		Syn.log.l(Syn.log.PEDANTIC, "Checking on %s" % package)
		try:
			return self._database[package]
		except KeyError as e:
			raise Syn.errors.PackageNotFoundException("No package found")

	def registerNewPackage(self, package, version, status):
		try:
			pkg = self._database[package]
			try:
				ver = pkg['installed'][version]
				raise Syn.errors.PackageInstalledException('package/version already registered')
			except KeyError:
				pkg['installed'][version] = { "status" : status }

		except KeyError:
			self._database[package] = {
				"linked"    : None,
				"installed" : {}
			}
			return self.registerNewPackage(package, version, status)

	def setState(self, package, version, status):
		Syn.log.l(Syn.log.PEDANTIC, "Setting %s (v%s) -- %s" % ( package, version, status ))
		self._database[package]['installed'][version]['status'] = status

	def setLinked(self, pkg, ver):
		self.setState(pkg, ver, LINKED)
		self._database[pkg]['linked'] = ver

	def setUnlinked(self, pkg, ver):
		self.setState(pkg, ver, INSTALLED)
		self._database[pkg]['linked'] = None

	def sync(self):
		self.writeout()

	def dump(self):
		db = self._database;
		for pkg in db:
			state = db[pkg]
			print pkg + ":"
			print "  Active Package Version: " + str(state['linked'])
			print "  Registered Versions:"
			for version in state['installed']:
				print "    " + version + ":	" + Syn.db.HR_STATE[state['installed'][version]['status']]

	def writeout(self):
		Syn.log.l(Syn.log.PEDANTIC, "Writing DB!")
		database = open(Syn.reg.CHROOT + g.SYNDB, 'wb')
		Syn.log.l(Syn.log.PEDANTIC, "File open")
		pickle.dump(self._database, database)
		Syn.log.l(Syn.log.PEDANTIC, "Dumped pickle data")
		database.close()
		Syn.log.l(Syn.log.PEDANTIC, "closed pickle")


def loadCanonicalDB():
	Syn.log.l(Syn.log.PEDANTIC, "Loading DB")
	Syn.log.l(Syn.log.PEDANTIC, "DB: " + Syn.reg.CHROOT + g.SYNDB)
	database = pickle.load(open(Syn.reg.CHROOT + g.SYNDB, 'rb'))
	Syn.log.l(Syn.log.PEDANTIC, "Extracted DB")
	ret = SynDB()
	ret._database = database
	return ret

def strapDB():
	Syn.log.l(Syn.log.PEDANTIC, "Bootstrapping Database")
	Syn.log.l(Syn.log.PEDANTIC, "ALL PACKAGE STATS WILL BE WIPED")
	ron = {}
	pickle.dump(ron,  open(Syn.reg.CHROOT + g.SYNDB, 'wb'))
	pickle.dump(True, open(Syn.reg.CHROOT + g.LOCKF, 'wb'))
	Syn.log.l(Syn.log.PEDANTIC, "Database nuked")

def aquireLock():
	Syn.log.l(Syn.log.PEDANTIC, "Snagging lock")
	lock = pickle.load(open(Syn.reg.CHROOT + g.LOCKF, 'rb'))
	if lock == True:
		pickle.dump(False, open(Syn.reg.CHROOT + g.LOCKF, 'wb'))
		Syn.log.l(Syn.log.PEDANTIC, "Got the lock!")
	else:
		raise Syn.errors.MutexException("Can not aquire lock")

def releaseLock():
	Syn.log.l(Syn.log.PEDANTIC, "Getting rid of the lock")
	lock = pickle.load(open(Syn.reg.CHROOT + g.LOCKF, 'rb'))
	if lock == False:
		pickle.dump(True, open(Syn.reg.CHROOT + g.LOCKF, 'wb'))
		Syn.log.l(Syn.log.PEDANTIC, "All set.")

