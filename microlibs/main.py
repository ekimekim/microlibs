import sys
import os
import subprocess

from lib import Lib
import config
import generate


def generate(name):
	lib = Lib(config.libdir, name)
	setup = generate.gen_setup(lib)
	path = os.path.join(config.setupdir, name)
	os.makedirs(path)
	with open(os.path.join(path, 'setup.py'), 'w') as f:
		f.write(setup)

def list_libs():
	ret = []
	for name in os.listdir(config.libdir):
		if name.startswith('.'): continue # ignore hidden files
		if os.path.join(config.libdir, name) == config.setupdir: continue # ignore setupdir contained in libdir
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
		print '\n'.join(list_libs())
	elif cmd in ('setup', 'setup.py'):
		name = args.pop(0)
		if name == 'all':
			for lib in list_libs():
				run_setup(lib, args)
		else:
			run_setup(name, args)
	else:
		raise ValueError("Unknown command")
