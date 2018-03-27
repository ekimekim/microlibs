import os
from setuptools import find_packages


def gen_setup(lib):
	"""Takes a Lib and generates a setup.py file for it.
	Note resulting setup.py requires all files to be in the same dir as it.
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
		'install_requires',
	}
	setup_kwargs = {kwarg: getattr(lib, kwarg) for kwarg in SETUP_KWARGS if getattr(lib, kwarg)}
	if lib.is_package:
		setup_kwargs['packages'] = [lib.name] + find_packages(lib.filename)
	else:
		setup_kwargs['py_modules'] = [lib.name]

	# there's no real nice way to do this, the best we can do is ensure eval(repr(x)) == x
	for value in setup_kwargs.values():
		try:
			good = (eval(repr(value)) == value)
		except Exception:
			# error in the eval
			good = False
		if not good:
			raise ValueError("Illegal value %r - doesn't repr/eval cleanly" % value)

	setup_kwarg_string = '\n'.join("\t%s = %r," % item for item in setup_kwargs.items())

	return (
		"from setuptools import setup\n"
		"\n"
		"setup(\n"
		"%s\n"
		")\n"
	) % setup_kwarg_string

def gen_dir(lib, path):
	"""Generate a directory containing a working setup.py
	along with symlinks to fake the structure distutils requires.
	Note this DOES NOT WORK with pip as pip is stupid and refuses to allow symlinks."""

	if not os.path.exists(path):
		os.makedirs(path)
	with open(os.path.join(path, 'setup.py'), 'w') as f:
		f.write(gen_setup(lib))
	link_path = os.path.join(path, os.path.basename(lib.filename))
	if not os.path.exists(link_path):
		os.link(lib.filename, link_path)
