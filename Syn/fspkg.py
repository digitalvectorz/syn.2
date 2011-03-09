#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global as g
import Syn.log

import json

class fspkg:
	def __init__(self, package, version):
		self.package = package
		self.version = version
		Syn.log.l(Syn.log.LOG, "Checking filesystem path %s %s" % ( package, version ))

	def loadJSON(self, path):
		Syn.log.l(Syn.log.LOG, "loading conf file %s" % ( path ))
		fd = open(path, 'r')
		meta = json.load(fd)
		fd.close()
		return meta

	def getSumFile(self):
		Syn.log.l(Syn.log.LOG, "Getting the sum file")
		path = self.getInstallPath()
		path += g.SYN_XTRACT_SUMS
		return self.loadJSON(path)

	def getAllFiles(self):
		fest = self.getSumFile()
		del(fest[g.ARCHIVE_FS_ROOT + g.SYN_BINARY_META])
		return fest

	def verify(self):
		Syn.log.l(Syn.log.LOG, "Verifying the fspkg")
		pass

	def getInstallPath(self):
		path = g.INSTALL_ROOT_PATH + self.package + "/" + self.version + "/"
		return path
