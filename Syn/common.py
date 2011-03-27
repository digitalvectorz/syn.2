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

def isRoot():
	uID = os.geteuid()
	Syn.log.l(Syn.log.PEDANTIC, "euid: " + str(uID))
	ret = uID == 0
	return ret

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

def mv(to, fro):
	shutil.move(to, fro)
	Syn.log.l(Syn.log.PEDANTIC, "move %s %s" % (to, fro))

def isln(loc):
	Syn.log.l(Syn.log.PEDANTIC, "checking is similink path `%s'" % loc)
	return os.path.islink(loc)

def xists(loc):
	Syn.log.l(Syn.log.PEDANTIC, "checking path `%s'" % loc)
	return os.path.exists(loc)

def rmdir(dirs):
	Syn.log.l(Syn.log.PEDANTIC, "rmdir " + dirs)
	shutil.rmtree(dirs)

def rm(dirs):
	Syn.log.l(Syn.log.PEDANTIC, "rm " + dirs)
	os.remove(dirs)

def ln(source, dest):
	dirski = os.path.dirname(dest)
	if not xists(dirski):
		Syn.log.l(Syn.log.PEDANTIC, "Can't find it's basedir. Creating it")
		mkdir(dirski)

	Syn.log.l(Syn.log.PEDANTIC, "ln " + source + " to " + dest)
	os.symlink(source, dest)

def fs_ln_inst(source, dest):
	#lay_claim
	ln(source,dest)

def fs_unln_inst(fi):
	#unlay claim
	rm(fi)

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
		elif os.path.islink(path + "/" + f):
			Syn.log.l(Syn.log.PEDANTIC, "  similink not getting sum'd")
		else:
			Syn.log.l(Syn.log.PEDANTIC, "  " + path + "/" + f)
			ret[path + "/" + f] = Syn.verification.md5sum(path + "/" + f)
	return ret

def isInPath(path):
	try:
		pat = os.path.dirname(path)
		ff = g.DEFAULT_PATH[pat]
		return (True, ff)
	except KeyError as e:
		return (False, False)

def isInLibPath(path):
	try:
		pat = os.path.dirname(path)
		ff = g.DEFAULT_LIBS[pat]
		return (True, ff)
	except KeyError as e:
		return (False, False)
