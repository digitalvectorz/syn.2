#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.package as package

# A = package.package("a", 1)
# B = package.package("b", 1)
# C = package.package("c", 1)
# 
# A.setDeps(["b"])
# B.setDeps(["c"])
# 
# install_packageset = {"a" : A}
# package_pool       = {"a" : A, "b" : B, "c" : C}
# install = resolveDeps(install_packageset, package_pool)

def resolveDeps(install, pool):
	staged_packages = install.copy()

	for x in install:
		package_deps = install[x].getDeps()
		for dep in package_deps:
			try:
				staged_packages[dep] = pool[dep]
			except KeyError as e:
				raise Exception("Can't resolve dep %s" % dep);
	if install != staged_packages:
		return resolveDeps(staged_packages, pool)
	else:
		return staged_packages
