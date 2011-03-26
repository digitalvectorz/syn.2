#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

# Default package classes and such

PKG_CLASS_DEFAULTS = {
	"*"              : "pkg-base"
	"/usr/bin/*"     : "user-bin",
	"/bin/*"         : "susr-bin",
	"/usr/include/*" : "user-inc",
	"/usr/lib/*"     : "user-lib",
	"/lib/*"         : "glob-lib",
	"/etc/*"         : "srvg-sug"
}
