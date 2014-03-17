import os
import subprocess

"""Loads vars from a conf file. Conf file is exec()'d.
Default conf file is ~/.microlibs, overridable with MICROLIB_CONF env var
"""

def cmd(args):
	try:
		return subprocess.check_output(args).strip()
	except subprocess.CalledProcessError:
		return None

CONF_FILE = os.environ.get('MICROLIB_CONF', None) or os.path.expanduser("~/.microlibs")

# git top level dir - you probably shouldn't override this
topdir = cmd(['git', 'rev-parse', '--show-toplevel'])

# author: Default project (author, author_email). By default, queries git config.
author = [cmd(['git', 'config', key]) for key in ('user.name', 'user.email')]

# libdir: Directory to look for libs in, relative to git top level dir
libdir = 'libs'

# setupdir: Directory to put setup.py files in, relative to git top level dir
setupdir = 'pkgs'

# now we exec the conf file with our globals
if os.path.exists(CONF_FILE):
	execfile(CONF_FILE, globals())

# then we resolve the relative paths
libdir = os.path.join(topdir, libdir)
setupdir = os.path.join(topdir, setupdir)
