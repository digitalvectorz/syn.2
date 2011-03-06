#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global as g

import pickle

INSTALLED      = "I"
HALF_INSTALLED = "H"
LINKED         = "L"
REMOVED        = "R"
BORKED         = "B"
UNINSTALLED    = "U"

class SynDB:
	_database = {}

	def queryState(self, package):
		try:
			return self._database[package]
		except KeyError as e:
			return UNINSTALLED

	def setState(self, package, status):
		self._database[package] = status

def loadCanonicalDB():
	database = pickle.load(open(g.SYNDB, 'rb'))
	return database

def strapDB():
	ron = SynDB()
	pickle.dump(ron, open(g.SYNDB, 'wb'))

