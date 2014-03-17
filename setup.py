from setuptools import setup

setup(
	name = "microlibs",
	version = "0.1",
	description = "Utility for managing many small libraries",
	author = "Mike Lang",
	author_email = "mikelang3000@gmail.com",
	packages = ['microlibs'],
	entry_points = {'microlibs':['microlibs = microlibs:main']},
)
