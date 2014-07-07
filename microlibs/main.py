import sys
import os
import subprocess

from lib import Lib
import config
from generate import gen_dir

HELP = """Commands:
	generate {LIBS} - Generate a setup.py for each given lib, or all libs if not given.
	help - Print this help
	list - Print a list of all libs.
	setup (LIB|all) {ARGS} - Run setup.py for given lib (or all libs) with given args.
"""

def generate(name):
	lib = Lib(config.libdir, name)
	path = os.path.join(config.setupdir, lib.name)
	gen_dir(lib, path)

def list_libs():
	ret = []
	for name in os.listdir(config.libdir):
		if name.startswith('.'): continue # ignore hidden files
		if os.path.join(config.libdir, name) == config.setupdir: continue # ignore setupdir contained in libdir
		name, ext = os.path.splitext(name)
		if ext not in ('', '.py'): continue # if there's an extension, it must be .py
		ret.append(name)
	return ret

def run_setup(name, args):
	setup_file = os.path.join(config.setupdir, name, 'setup.py')
	os.chdir(os.path.dirname(setup_file)) # this makes sure the build/ dist/ and other crap ends up in the right place
	subprocess.check_call(['python', setup_file] + list(args))

def main():
	progname = sys.argv[0]
	cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
	args = sys.argv[2:]

	if cmd == 'help':
		print HELP
	elif cmd == 'generate':
		if not args:
			args = list_libs()
		for arg in args:
			generate(arg)
	elif cmd == 'list':
		libs = list_libs()
		verbose = '-v' in args
		if libs:
			if verbose:
				print '\n'.join('%s - %s' % (name, Lib(config.libdir, name).description)
				                for name in libs)
			else:
				print '\n'.join(libs)
	elif cmd in ('setup', 'setup.py'):
		name = args.pop(0)
		if name == 'all':
			for lib in list_libs():
				run_setup(lib, args)
		else:
			run_setup(name, args)
	else:
		raise ValueError("Unknown command")
