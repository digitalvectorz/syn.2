#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#
import Syn.Global as g
import Syn.log

import tarfile
import os.path
import shutil
import time
import os

def processFullID(identifier):
	try:
		split = identifier.index("-")
		package_id = identifier[:split]
		version_id = identifier[split+1:]
		return [ package_id, version_id ]
	except ValueError:
		return [ identifier, None ]

def getTempLocation():
	timestamp = time.time()
	unpack_dir = Syn.Global.WORKDIR + str(timestamp) + "/"
	return unpack_dir

def mkdir(location):
	Syn.log.l(Syn.log.PEDANTIC, "creating dir " + location)
	os.makedirs(location)

def cd(work_dir):
	os.chdir(work_dir)
	Syn.log.l(Syn.log.PEDANTIC, "chdir to " + work_dir)

def cp(to, fro):
	shutil.copy(to, fro)
	Syn.log.l(Syn.log.PEDANTIC, "copy %s %s" % (to, fro))

def rmdir(dirs):
	shutil.rmtree(dirs)
	Syn.log.l(Syn.log.PEDANTIC, "rmdir " + dirs)

def dict_diff(first, second):
	diff = {}
	# Check all keys in first dict
	for key in first.keys():
		if (not second.has_key(key)):
			diff[key] = (first[key], "<UNKNOWN>")
		elif (first[key] != second[key]):
			diff[key] = (first[key], second[key])
	# Check all keys in second dict to find missing
	for key in second.keys():
		if (not first.has_key(key)):
			diff[key] = (None, second[key])
	return diff

def md5sumwd(check = os.getcwd()):
	ret = {}
	path = check

	for f in os.listdir(path):
		if os.path.isdir(path + "/" + f):
			dictret = md5sumwd(path + "/" + f)
			for x in dictret:
				ret[x] = dictret[x]
		else:
			ret[path + "/" + f] = Syn.verification.md5sum(path + "/" + f)
	return ret
