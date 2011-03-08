#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global as g
import Syn.log

import pickle

INSTALLED      = "I"
HALF_INSTALLED = "H"
LINKED         = "L"
REMOVED        = "R"
BORKED         = "B"
UNINSTALLED    = "U"

HR_STATE = {
	INSTALLED       : "Installed",
	HALF_INSTALLED  : "Half-installed",
	LINKED          : "Linked",
	REMOVED         : "Removed",
	BORKED          : "Borked",
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

	def initPkg(self, package, version):
		self._database[package] = {
			"linked" : None,
			"installed" : {
				version : {
					"status" : "U"
				}
			}
		}

	def setState(self, package, version, status):
		Syn.log.l(Syn.log.PEDANTIC, "Setting %s (v%s) -- %s" % ( package, version, status ))
		self._database[package]['installed'][version]['status'] = status

	def sync(self):
		self.writeout()

	def writeout(self):
		Syn.log.l(Syn.log.PEDANTIC, "Writing DB!")
		database = open(g.SYNDB, 'wb')
		Syn.log.l(Syn.log.PEDANTIC, "File open")
		pickle.dump(self._database, database)
		Syn.log.l(Syn.log.PEDANTIC, "Dumped pickle data")
		Syn.log.l(Syn.log.PEDANTIC, str(self._database))
		database.close()
		Syn.log.l(Syn.log.PEDANTIC, "closed pickle")


def loadCanonicalDB():
	Syn.log.l(Syn.log.PEDANTIC, "Loading DB")
	database = pickle.load(open(g.SYNDB, 'rb'))
	Syn.log.l(Syn.log.PEDANTIC, "Extracted DB")
	ret = SynDB()
	ret._database = database
	return ret
	

def strapDB():
	Syn.log.l(Syn.log.PEDANTIC, "Bootstrapping Database")
	Syn.log.l(Syn.log.PEDANTIC, "ALL PACKAGE STATS WILL BE WIPED")
	ron = {}
	pickle.dump(ron,  open(g.SYNDB, 'wb'))
	pickle.dump(True, open(g.LOCKF, 'wb'))
	Syn.log.l(Syn.log.PEDANTIC, "Database nuked")

def aquireLock():
	Syn.log.l(Syn.log.PEDANTIC, "Snagging lock")
	lock = pickle.load(open(g.LOCKF, 'rb'))
	if lock == True:
		pickle.dump(False, open(g.LOCKF, 'wb'))
		Syn.log.l(Syn.log.PEDANTIC, "Got the lock!")
	else:
		raise Syn.errors.MutexException("Can not aquire lock")

def releaseLock():
	Syn.log.l(Syn.log.PEDANTIC, "Getting rid of the lock")
	lock = pickle.load(open(g.LOCKF, 'rb'))
	if lock == False:
		pickle.dump(True, open(g.LOCKF, 'wb'))
		Syn.log.l(Syn.log.PEDANTIC, "All set.")
