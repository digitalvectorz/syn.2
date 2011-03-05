import Syn.log
import tarfile
import os.path

class us_tb:
	def target( self, tarball ):
		try:
			self.tarball_target = tarfile.open(tarball, 'r')
		except ValueError as e:
			Syn.log.l(Syn.log.CRITICAL, "Failed to open tarfile")
			Syn.log.l(Syn.log.PEDANTIC, str(e))
			raise ValueError("Failed to open " + tarball)

	def getRootFolder(self):
		try:
			members = self.tarball_target.getmembers()
			directories = []
			for member in members:
				if member.isdir():
					directories.append(member.name)
			root_folder = os.path.commonprefix(directories)
			return root_folder
		except AttributeError as e:
			raise ValueError("No tarball!")
