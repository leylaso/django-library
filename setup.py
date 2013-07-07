#!/usr/bin/env python

# We're using the examples from http://docs.python.org/2/distutils/setupscript.html

from distutils.core import setup

setup(name='django-library',
      version='0.099', 					# we're so pre-0.1
      description='a django library management system',
      author='Nervous Rocks',
      author_email='nervous-rocks@resist.ca',
      url='https://github.com/GuillaumeFromage/django-library',
      packages=['django-library'],
     )
