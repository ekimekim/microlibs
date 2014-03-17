import os
from setuptools import find_packages


def gen_setup(lib, location=None):
	"""Takes a Lib and generates a setup.py file for it.
	If location is given, makes paths relative to it.
	"""
	SETUP_KWARGS = {
		'name',
		'version',
		'author',
		'author_email',
		'maintainer',
		'maintainer_email',
		'description',
		'long_description',
		'licence',
	}
	setup_kwargs = {kwarg: getattr(lib, kwarg) for kwarg in SETUP_KWARGS if getattr(lib, kwarg)}
	pkg_path = os.path.join(lib.path, lib.name)
	if os.path.isdir(pkg_path):
		setup_kwargs['package_dir'] = {'': lib.path}
		setup_kwargs['packages'] = [lib.name] + find_packages(pkg_path)
	elif os.path.isfile(pkg_path + '.py'):
		setup_kwargs['py_modules'] = [pkg_path + '.py']
	else:
		raise ValueError("Cannot find module or package at %r", pkg_path)

	# make paths relative
	if location:
		if 'package_dir' in setup_kwargs:
			setup_kwargs['package_dir'][''] = os.path.relpath(setup_kwargs['package_dir'][''], location)
		if 'packages' in setup_kwargs:
			setup_kwargs['packages'] = [os.path.relpath(pkg, location) for pkg in setup_kwargs['packages']]
		if 'py_modules' in setup_kwargs:
			setup_kwargs['py_modules'] = [os.path.relpath(module, location) for module in setup_kwargs['py_modules']]

	# there's no real nice way to do this, the best we can do is ensure eval(repr(x)) == x
	for value in setup_kwargs.values():
		try:
			good = (eval(repr(value)) == value)
		except Exception:
			# error in the eval
			good = False
		if not good:
			raise ValueError("Illegal value %r - doesn't repr/eval cleanly" % value)

	setup_kwarg_string = '\n'.join("\t%s = %r" % item for item in setup_kwargs.items())
	return (
		"from setuptools import setup\n"
		"\n"
		"setup(\n"
		"%s\n"
		")\n"
	) % setup_kwarg_string

