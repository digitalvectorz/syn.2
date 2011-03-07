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

HR_FMT = {
	INSTALLED       : "Installed",
	HALF_INSTALLED  : "Half-installed",
	LINKED          : "Linked",
	REMOVED         : "Removed",
	BORKED          : "Borked",
	UNINSTALLED     : "Uninstalled"
}

#
# "package-n.m" : {
#    "package" : package,
#    "version" : version,
#    "status"  : status
# }
#

class SynDB:
	_database = {}

	def queryState(self, package, version):
		Syn.log.l(Syn.log.PEDANTIC, "Checking on %s (%s)" % ( package, version ))
		try:
			Syn.log.l(Syn.log.PEDANTIC, "Hit! Returning status.")
			return self._database[package + "-" + version]
		except KeyError as e:
			Syn.log.l(Syn.log.PEDANTIC, "Total miss! Dumb data!")
			return {
				"package" : package,
				"version" : version,
				"status"  : UNINSTALLED
			}

	def setState(self, package, version, status):
		Syn.log.l(Syn.log.PEDANTIC, "Setting %s (v%s) -- %s" % ( package, version, status ))
		fullid = package + "-" + version
		Syn.log.l(Syn.log.PEDANTIC, "fullid: " + fullid)

		self._database[fullid] = status

		Syn.log.l(Syn.log.PEDANTIC, "Set. Returning.")

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
	Syn.log.l(Syn.log.PEDANTIC, "Loading Canonical DB")
	database = pickle.load(open(g.SYNDB, 'rb'))
	Syn.log.l(Syn.log.PEDANTIC, "Extracted DB")
	ret = SynDB()
	ret._database = database
	Syn.log.l(Syn.log.PEDANTIC, "DB Reset")
	return ret
	

def strapDB():
	Syn.log.l(Syn.log.PEDANTIC, "Bootstrapping Database")
	ron = {}
	pickle.dump(ron, open(g.SYNDB, 'wb'))

