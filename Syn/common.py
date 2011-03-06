import time
import os

import Syn.Global

def processFullID(identifier):
	split = identifier.index("-")
	package_id = identifier[:split]
	version_id = identifier[split+1:]
	return [ package_id, version_id ]

def getTempLocation():
	timestamp = time.time()
	unpack_dir = Syn.Global.WORKDIR + str(timestamp) + "/"
	return unpack_dir

def createWorkDir(location):
	Syn.log.l(Syn.log.PEDANTIC, "creating work dir " + location)
	global _CUR_WORK_DIR
	_CUR_WORK_DIR = location
	os.makedirs(_CUR_WORK_DIR)

def mkdir(location):
	Syn.log.l(Syn.log.PEDANTIC, "creating dir " + location)
	os.makedirs(location)

def removeWorkDir():
	global _CUR_WORK_DIR
	Syn.log.l(Syn.log.PEDANTIC, "removing work dir " + _CUR_WORK_DIR)
	os.rmdir(_CUR_WORK_DIR)

def cd(work_dir):
	Syn.log.l(Syn.log.PEDANTIC, "chdir to " + work_dir)
	os.chdir(work_dir)

