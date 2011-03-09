#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

class SynException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ArchiveNotFoundException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class InvalidJSONException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class InvalidArchiveException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class NotAnArchiveException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class FileNotPresentException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class BuildFailureException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class MutexException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class PackageNotFoundException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ConflictException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class PackageInstalledException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class PackageNotinstalledException(SynException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class PackageUninstalledException(PackageNotinstalledException):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
