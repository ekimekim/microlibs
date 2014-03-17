import importlib
import re
import os
import sys
import time

import config


class Lib(object):

	# Maps from setup.py metadata to module attrs
	# Note all these default to None if not defined
	ATTR_MAP = dict(
		base_version = '__VERSION__',
		long_description = '__doc__',
		licence = '__LICENCE__',
		install_requires = '__REQUIRES__',
	)

	def __init__(self, path, name):
		"""Import a lib from given directory with given name.
		Name may be with or without .py extension.
		If module raises any error during import, we let it raise.
		"""
		if name.endswith('.py'):
			name = name[:-len('.py')]

		self.path = path
		self.name = name

		sys.path.insert(0, path)
		try:
			self.module = importlib.import_module(name)
		finally:
			assert sys.path.pop(0) == path, "sys.path modified during import"

	def __getattr__(self, attr):
		if attr not in self.ATTR_MAP:
			raise AttributeError(attr)
		return getattr(self.module, self.ATTR_MAP[attr], None)

	def _name_and_email(self, attr):
		"""Parses fields that may contain a name and email.
		Recognises the following forms:
			"My Name"
			"My Name <myemail>"
			("My Name", "myemail")
		"""
		value = getattr(self.module, attr, None)
		if value is None:
			return None, None
		if isinstance(value, basestring):
			match = re.match('^ ([^<]*) < ([^>]*) > $', value, re.VERBOSE)
			if match:
				name, email = (s.strip() for s in match.groups())
			else:
				name, email = value, None
		else:
			# assume tuple or similar
			name, email = value
		return name, email

	@property
	def author_info(self):
		name, email = self._name_and_email('__AUTHOR__')
		if not name:
			return config.author
		return name, email
	@property
	def author(self):
		return self.author_info[0]
	@property
	def author_email(self):
		return self.author_info[1]
	@property
	def maintainer(self):
		name, email = self._name_and_email('__MAINTAINER__')
		return name
	@property
	def maintainer_email(self):
		name, email = self._name_and_email('__MAINTAINER__')
		return email

	@property
	def description(self):
		if not self.long_description:
			return None
		return self.long_description.split('\n')[0].strip()

	@property
	def version(self):
		return "%s.%d" % (self.base_version or '0.0', time.time())

	@property
	def is_package(self):
		pkg_path = os.path.join(self.path, self.name)
		if os.path.isdir(pkg_path):
			return True
		elif os.path.isfile(pkg_path + '.py'):
			return False
		else:
			raise ValueError("Cannot find module or package at %r", pkg_path)

	@property
	def filename(self):
		ret = os.path.join(self.path, self.name)
		if not self.is_package:
			ret += '.py'
		return ret
