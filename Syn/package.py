#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

class package:
	def __init__(self, package, version):
		self.package = package
		self.version = version
		self.setDeps({})

	def setDeps(self, deps):
		self.deps = deps

	def getDeps(self):
		return self.deps
