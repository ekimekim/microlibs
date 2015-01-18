import os
import subprocess

from argh import EntryPoint, arg, aliases, named

from microlibs import config
from microlibs.lib import Lib
from microlibs.generate import gen_dir


cli = EntryPoint()


def get_libs():
	ret = []
	for name in os.listdir(config.libdir):
		if name.startswith('.'): continue # ignore hidden files
		if os.path.join(config.libdir, name) == config.setupdir: continue # ignore setupdir contained in libdir
		name, ext = os.path.splitext(name)
		if ext not in ('', '.py'): continue # if there's an extension, it must be .py
		ret.append(name)
	return ret


@cli
def generate(*libs):
	"""Generate a setup.py for each given lib, or all libs if none given"""
	if not libs:
		libs = get_libs()
	for name in libs:
		lib = Lib(config.libdir, name)
		path = os.path.join(config.setupdir, lib.name)
		gen_dir(lib, path)


@cli
@aliases('setup.py')
def setup(lib, *args):
	"""Run setup.py for given lib (or 'all' for all libs) with given args"""
	libs = get_libs() if lib == 'all' else (lib,)
	for lib in libs:
		setup_file = os.path.join(config.setupdir, lib, 'setup.py')
		os.chdir(os.path.dirname(setup_file)) # this makes sure the build/ dist/ and other crap ends up in the right place
		subprocess.check_call(['python', setup_file] + list(args))


@cli
@arg('--verbose', help='Print description along with name')
@named('list')
def list_libs(verbose=False):
	"""List all libs"""
	libs = get_libs()
	if verbose:
		print '\n'.join('{} - {}'.format(name, Lib(config.libdir, name).description)
						for name in libs)
	else:
		print '\n'.join(libs)


if __name__ == '__main__':
	cli()
