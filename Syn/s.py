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
	# print "export " + key + "=\"" + value + "\""
	os.putenv(key, value)

def loadBuildConfigFile():
	Syn.log.l(Syn.log.VERBOSE, "Loading build config")
	Syn.log.l(Syn.log.VERBOSE, "Opening" + g.SYN_BUILDDIR + g.SYN_BUILDDIR_CONFIG )
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_CONFIG)
	Syn.log.l(Syn.log.VERBOSE, "File open")
	conf_file = f.read()
	#Syn.log.l(Syn.log.VERBOSE, "Read file " + conf_file)
	config_json = json.loads(conf_file)
 	#Syn.log.l(Syn.log.VERBOSE, "str: " + str(config_json))
	return config_json

def loadMetaConfigFile():
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_META)
	Syn.log.l(Syn.log.VERBOSE, "Opening " + g.SYN_BUILDDIR + g.SYN_BUILDDIR_CONFIG )
	conf_file = f.read()
	Syn.log.l(Syn.log.VERBOSE, "file read")
	#Syn.log.l(Syn.log.VERBOSE, "read as: " + str(conf_file))
	config_json = json.loads(conf_file)
	#Syn.log.l(Syn.log.VERBOSE, "str: " + str(config_json))
	return config_json

def writeMetafile(frobernate):
	output = json.dumps(
		frobernate,
		sort_keys = True,
		indent    = 4
	)
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_META, 'w')
	f.write(output)
	f.close()

def extractSource(pack_loc, path="."):
	global _tb
	c.cd(pack_loc)
	try:
		root = _tb.getRootFolder()		
		_tb.extractall(path)
	except NameError as e:
		raise NameError("Package not set")

def tarup( directory, outputname ):
	Syn.log.l(Syn.log.PEDANTIC,"Taring " + outputname)
	tarball_target = tarfile.open(str(outputname), "w|gz")
	Syn.log.l(Syn.log.PEDANTIC,"Adding " + directory)
	tarball_target.add(directory)
	tarball_target.close()

def buildFromSource(pkg_path):
	Syn.build.buildFromSource(pkg_path)

def metadump(filezor):
	tarball_target = tarfile.open(filezor, "r")
	metafile = g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_META
	tarinfo = tarball_target.getmember(metafile)
	if tarinfo.isfile():
		meta = tarball_target.extractfile(metafile)
		metadata = json.loads(meta.read())
	else:
		raise KeyError("Bum file")
	tarball_target.close()
	return metadata

def loadVerificationFile(filezor):
	tarball_target = tarfile.open(filezor, "r")
	metafile = g.ARCHIVE_FS_ROOT + "/" + g.SYN_FILESUMS
	tarinfo = tarball_target.getmember(metafile)
	if tarinfo.isfile():
		meta = tarball_target.extractfile(metafile)
		metadata = json.loads(meta.read())
	else:
		raise KeyError("Bum file")
	tarball_target.close()
	return metadata

def verifyTar(verify):
	tar_info = Syn.verification.md5sumtar(verify)
	del(tar_info[g.ARCHIVE_FS_ROOT + "/" + g.SYN_FILESUMS])

	md5_info = loadVerificationFile(verify)	
	delta = c.dict_diff(tar_info, md5_info)

	Syn.log.l(Syn.log.PEDANTIC, "Processed " + str(len(md5_info)) + " files in the map.")
	Syn.log.l(Syn.log.PEDANTIC, "Processed " + str(len(tar_info)) + " files in the tarball.")

	errors = 0

	for i in delta:
		Syn.log.l(Syn.log.CRITICAL, i)

		if i in tar_info:
			Syn.log.l(Syn.log.CRITICAL, " Tar file is: %s" % tar_info[i])
		else:
			Syn.log.l(Syn.log.CRITICAL, " Tarball does not have this file!")

		if i in md5_info:
			Syn.log.l(Syn.log.CRITICAL, " File shows:  %s" % md5_info[i])
		else:
			Syn.log.l(Syn.log.CRITICAL, " Map does not have this file!!!! WARNING!")

		errors += 1

	Syn.log.l(Syn.log.MESSAGE, "" )
	Syn.log.l(Syn.log.MESSAGE, "Total Errors: " + str(errors) )
	Syn.log.l(Syn.log.MESSAGE, "" )

	return errors

def build(pack_loc):
	return Syn.build.build(pack_loc)

def buildSourcePackage(pkg_loc):
	return Syn.build.buildSourcePackage(pkg_loc)

def install(pathorig):
	return Syn.install.install(pathorig)
