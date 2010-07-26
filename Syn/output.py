"""
Output functions. Helps with logging etc.


Verbosity Levels:

-v        == 0
-vv       == 1
-vvv      == 2
-vvvv     == 4
-vuvuzela == BBBZZZZZZZZZZZZZZZZZZZZZZZZzzzzZZZZ


0 -- Critical output. Usually one per command, if it's successful.
     Try and avoid null output

1 -- Detailed output. Put this in if the next line will take a long
     time to finish

2 -- Internal output. Put this in for commands that use varables
     that are not defined in the code ( read -- external conf files )

3 -- Messy output. Put as much as you can on this level. Helps avoid
     adding print statements in later


Oh, and please be funny.

"""

import Syn
import sys

verbosity = Syn.__default_verbosity__

LOG_PREFIX   = " [ -- ]   "
PASS_PREFIX  = " [ [32mok[0m ]   "
FAIL_PREFIX  = " [ [31mno[0m ]   "


def query( string, default, verbose ):
	"""Log a message that explains the internals"""
	if verbose <= verbosity:
		print "Q: Enter " + string + " ( default: " + default + " )"
		s = sys.stdin
		r = s.readline()
		r = r.strip()
		if r != "":
			return r.strip()
		else:
			return default
	else:
		return default


def log( string, verbose ):
	"""Log a message that explains the internals"""
	if verbose <= verbosity:
		print LOG_PREFIX + string
	else:
		pass

def error( string, verbose ):
	"""Log an error message"""
	if verbose <= verbosity:
		print FAIL_PREFIX + string
	else:
		pass

def success( string, verbose ):
	"""Log something that went just fine"""
	if verbose <= verbosity:
		print PASS_PREFIX + string
	else:
		pass


log(
	"Starting " + Syn.__appname__ +
	" version " + Syn.__version__
	,
	3
)
log( Syn.__copyright__, 3 )

