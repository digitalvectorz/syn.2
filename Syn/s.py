#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.verification

import Syn.tarball
import Syn.common as c
import Syn.Global as g
import Syn.build
import Syn.log

import tarfile
import os.path
import shutil
import json
import os
import os.path

def targetTarball(tar):
	global _tb
	global _tb_dir
	_tb_dir = os.path.dirname(os.path.abspath(tar))
	_tb = Syn.tarball.us_tb()
	_tb.target(tar);

def getVersion():
	global _tb
	try:
		root = _tb.getRootFolder()
	except NameError as e:
		raise NameError("Package not set")

	package, version = Syn.common.processFullID(root)
	Syn.log.l(Syn.log.VERBOSE, "Processing package   `%s'" % package)
	Syn.log.l(Syn.log.VERBOSE, "Version processed as `%s'" % version)
	return [package, version]

def md5sumwd(check = os.getcwd()):
	ret = {}
	path = check # os.path.abspath(check)

	for f in os.listdir(path):
		if os.path.isdir(path + "/" + f):
			dictret = md5sumwd(path + "/" + f)
			for x in dictret:
				ret[x] = dictret[x]
		else:
			ret[path + "/" + f] = Syn.verification.md5sum(path + "/" + f)
	return ret

def putenv(key, value):
	Syn.log.l(Syn.log.VERBOSE, "%s = %s" % (key, value))
	os.putenv(key, value)

