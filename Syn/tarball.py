#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.Global as g

import Syn.verification
import Syn.package
import Syn.common
import Syn.errors
import Syn.log

import tarfile
import os.path
import json
import os

BINARY  = 1
SOURCE  = 2
UNKNOWN = 3

HR_CLASSES = {
	BINARY  : "binary",
	SOURCE  : "source",
	UNKNOWN : "unknown"
}

class archive:
	def __init__(self, archive, verify=False, inPlace=True):
		Syn.log.l(Syn.log.VERBOSE, "attempting to load " + archive )
		try:
			self.tarball_target = tarfile.open(archive, 'r')
			self._klass = UNKNOWN
			self._konf  = {}

			self._classify()
			self._loadResources()

			if verify:
				try:
					self._verify(inPlace)
				except AssertionError:
					raise Syn.errors.InvalidArchiveException("Verification Failed!")
		except ValueError as e:
			Syn.log.l(Syn.log.CRITICAL, "Failed to open archive " + str(e))
			raise Syn.errors.ArchiveNotFoundException(e)
		except IOError:
			raise Syn.errors.InvalidArchiveException("Failure to read archive!")

	def getConf(self, conffile):
		return self._konf[conffile]

	def _verify(self, inPlace=True):
		root = self.getRootFolder()
		package, version = Syn.common.processFullID(root)

		if self._klass == SOURCE:
			Syn.log.l(Syn.log.MESSAGE, "Checking Package Name for Consistancy")
			assert package == self._konf[g.SYN_SRC_DIR + g.SYN_BUILDDIR_META]['package']
			Syn.log.l(Syn.log.MESSAGE, "Checking Version for Consistancy")
			assert version == self._konf[g.SYN_SRC_DIR + g.SYN_BUILDDIR_META]['version']
			try:
				Syn.log.l(Syn.log.MESSAGE, "Checking if tarball is intact")
				sourceball = self._konf[g.SYN_SRC_DIR + g.SYN_BUILDDIR_META]['download']
				sourceball = os.path.basename(sourceball)
				sourceball_ar = self.tarball_target.getmember(package + "-" + version + "/" + sourceball)
				sourceball_ar = os.path.basename(sourceball_ar.name)
			except KeyError:
				Syn.log.l(Syn.log.MESSAGE, "Tarball does not match download metainf!")
				assert True == False

			Syn.log.l(Syn.log.MESSAGE, "Tarball exists, ensuring they match.")
			assert sourceball == sourceball_ar

		if self._klass == BINARY:
			Syn.log.l(Syn.log.MESSAGE, "Getting a filesum list")
			actualSums = self.genSums(inPlace=inPlace)
			del(actualSums[g.ARCHIVE_FS_ROOT + g.SYN_BINARY_FILESUMS])
			Syn.log.l(Syn.log.MESSAGE, "Comparing to stored sums")
			delta = Syn.common.dict_diff(actualSums, self._konf[g.SYN_BINARY_FILESUMS])
			errors = 0
			for x in delta:
				Syn.log.l(Syn.log.MESSAGE, x + " is in conflict")
				errors += 1
			Syn.log.l(Syn.log.MESSAGE, str(errors) + " errors in md5 checking")
			assert errors == 0

	def _loadResources(self):
		root = self.getRootFolder()
		processList = [];

		if self._klass == BINARY:
			processList = g.SYN_BIN_LOAD_ON_LOAD
		elif self._klass == SOURCE:
			processList = g.SYN_SRC_LOAD_ON_LOAD

		for f in processList:
			self._konf[f] = self.pullJSON(root + "/" + f)

	def genSums(self, inPlace = True):
		if inPlace:
			Syn.log.l(Syn.log.MESSAGE, "In Place")
			return self.genSumsInPlace()
		else:
			Syn.log.l(Syn.log.MESSAGE, "In Tmp")
			return self.genSumsInTmp()

	def genSumsInTmp(self):
		ret_loc = os.getcwd()
		build_root = Syn.common.getTempLocation()
		Syn.common.mkdir(build_root)
		Syn.common.cd(build_root)

		self.extractall()
		sums = Syn.common.md5sumwd(g.ARCHIVE_FS_ROOT_NOSLASH)

		Syn.common.rmdir(build_root)
		Syn.common.cd(ret_loc)
		return sums

	def genSumsInPlace(self):
		filelist = self.tarball_target.getmembers()
		sumlist = {}

		for tarinfo in filelist:
			Syn.log.l(Syn.log.PEDANTIC, "  " + tarinfo.name)
			if tarinfo.isfile() or tarinfo.islnk():
				fd = self.tarball_target.extractfile(tarinfo)
				md5 = Syn.verification.sumfile(fd)
				fd.close()
				sumlist[tarinfo.name] = md5
			else:
				Syn.log.l(Syn.log.PEDANTIC, "  " + tarinfo.name + " ignoring nonfile ")
				Syn.log.l(Syn.log.PEDANTIC, "  " + tarinfo.name + " h: " + str(tarinfo.islnk()))
				Syn.log.l(Syn.log.PEDANTIC, "  " + tarinfo.name + " s: " + str(tarinfo.issym()))
				

		return sumlist

	def _classify(self):
		try:
			self.pullJSON(g.ARCHIVE_FS_ROOT + g.SYN_BINARY_META)
			self._klass = BINARY
			Syn.log.l(Syn.log.VERBOSE, "discovered the binary giveaway")
			return
		except Syn.errors.FileNotPresentException:
			pass

		try:
			pkg_root = self.getRootFolder()
			self.pullJSON(pkg_root + "/" + g.SYN_SRC_DIR + g.SYN_BUILDDIR_META)
			self._klass = SOURCE
			Syn.log.l(Syn.log.VERBOSE, "discovered the source giveaway")
			return
		except Syn.errors.FileNotPresentException:
			pass

	def getRootFolder(self):
		members = self.tarball_target.getmembers()
		directories = []
		for member in members:
			#if member():
			directories.append(member.name)

		# print directories

		root_folder = os.path.commonprefix(directories)
		return root_folder

	def getClass(self):
		return self._klass

	def pullJSON(self, info_file):
		Syn.log.l(Syn.log.VERBOSE, "reading (json)" + info_file )
		try:
			tarinfo = self.tarball_target.getmember(info_file)
			if tarinfo.isfile():
				meta = self.tarball_target.extractfile(info_file)
				metadata = json.loads(meta.read())
				return metadata
			else:
				raise Syn.errors.FileNotPresentException(str(info_file + " is not a file"))
		except ValueError as e:
			raise Syn.errors.InvalidJSONException(info_file)

		except KeyError as e:
			raise Syn.errors.FileNotPresentException(str(info_file + " does not exist in this archive"))

	def extractall(self, path = "."):
		self.tarball_target.extractall(path)
	def close(self):
		self.tarball_target.close()

def newArchive( dirs, output, expectedType ):
	Syn.log.l(Syn.log.PEDANTIC,"Taring " + output)
	tarball_target = tarfile.open(str(output), "w|gz")

	for directory in dirs:
		Syn.log.l(Syn.log.PEDANTIC,"Adding " + directory)
		tarball_target.add(directory)

	tarball_target.close()

	ar = archive(output)
	if ar._klass != expectedType:
		raise Syn.errors.InvalidArchiveException("Wrong output archive type.")

	return ar

