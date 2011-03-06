#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

CRITICAL = 0
HIGH     = 1
MESSAGE  = 2
NOTICE   = 3
LOG      = 4
VERBOSE  = 5
PEDANTIC = 6

DEFAULT   = MESSAGE
VERBOSITY = DEFAULT

def l(level, msg):
	if level <= VERBOSITY:
		print "[l] (" + str(level) + "): " + msg;
