"""
File / folder layout
"""

SYN_TEMPLATE_DIR = "./synt"
SYN_TEMPLATE_LS  = {
	"metadata" : "dir",
	"steps"    : "dir",
	"logs"     : "dir",
	"patches"  : {
		"x86"    : "dir",
		"x86_64" : "dir",
		"sparc"  : "dir",
		"arm"    : "dir",
		"ppc"    : "dir",
		"all"    : "dir"
	}
}

SYN_DEFAULT_EMAIL = "invalid@domain.tld"
SYN_DEFAULT_NAME  = "John Q. Hacker"
SYN_RC_FILE       = "~/.synrc"                 # This will be expanded

SYN_BUILD_INFO    = "/metadata/build.synj"     # from synt root
SYN_DOWNLOAD_INFO = "/metadata/download.synj"  #  ..
SYN_PKG_INFO      = "/metadata/info.synj"      #  ..
SYN_INIT_INFO     = "/metadata/init.synj"      #  ..

SYN_SRC_XTNS = {
	"tar"      : ".tar",     # DUH
	"tar gz"   : ".tar.gz",  #   ..
	"tar gz"   : ".tgz",     #   ..
	"tar bzip" : ".tar.bz2"  #   ..
}

