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

HR_LOGLEVELS = {
	CRITICAL : "Critical ",
	HIGH     : "High     ",
	MESSAGE  : "Message  ",
	NOTICE   : "Notice   ",
	LOG      : "Log      ",
	VERBOSE  : "Verbose  ",
	PEDANTIC : "Pedantic "
}

DEFAULT   = LOG
VERBOSITY = DEFAULT

def l(level, msg):
	if level <= VERBOSITY:
		print "[l] (" + HR_LOGLEVELS[level] + "): " + msg;
def p(msg):
	level = NOTICE
	if level <= VERBOSITY:
		print msg

