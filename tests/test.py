
"""This module is a test for microlibs
It tests the various metadata-extraction features,
and ensures it can correctly generate a package."""

# not all of these are actually used, but it's just an example
import sys
import time

__REQUIRES__ = ['simplejson', 'requests']
import simplejson
import requests

__VERSION__ = '0.1'
__AUTHOR__ = 'Some Guy <someguy@example.com>'
__MAINTAINER__ = 'Someone Else', 'someone_else@example.com'
__LICENCE__ = '???' #TODO

def blah():
	print "This is a test"
