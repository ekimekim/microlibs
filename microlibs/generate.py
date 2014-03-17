

def gen_setup(lib):
	"""Takes a Lib and generates a setup.py file for it."""
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

