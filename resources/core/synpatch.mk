# patch system

configure::
	@echo "Patching source"
	patch -Np1 -i ../synd/patches/*
