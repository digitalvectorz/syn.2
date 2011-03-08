#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

class ArchiveNotFoundException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class InvalidJSONException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class InvalidArchiveException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class NotAnArchiveException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class FileNotPresentException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class BuildFailureException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

