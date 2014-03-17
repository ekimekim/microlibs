import sys
import os
import subprocess

from lib import Lib
import config
from generate import gen_setup


def generate(name):
	lib = Lib(config.libdir, name)
	path = os.path.join(config.setupdir, lib.name)
	setup = gen_setup(lib, location=path)
	if not os.path.exists(path): os.makedirs(path)
	with open(os.path.join(path, 'setup.py'), 'w') as f:
		f.write(setup)

def list_libs():
	ret = []
	for name in os.listdir(config.libdir):
		if name.startswith('.'): continue # ignore hidden files
		if os.path.join(config.libdir, name) == config.setupdir: continue # ignore setupdir contained in libdir
		_, ext = os.path.splitext(name)
		if ext not in ('', '.py'): continue # if there's an extension, it must be .py
		ret.append(name)
	return ret

def run_setup(name, args):
	setup_file = os.path.join(config.setupdir, name, 'setup.py')
	subprocess.check_call(['python', setup_file] + list(args))

def main():
	progname, cmd = sys.argv[:2]
	args = sys.argv[2:]

	if cmd == 'generate':
		if not args:
			args = list_libs()
		for arg in args:
			generate(arg)
	elif cmd == 'list':
		libs = list_libs()
		if libs:
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
