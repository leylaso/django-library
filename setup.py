#!/usr/bin/env python

# We're using the examples from http://docs.python.org/2/distutils/setupscript.html

import os
from distutils.core import setup

setup(name='django-library',
      version='1.0.1', 					# errr http://semver.org/
      description='a django library management system',
      author='Guillaume Le Punk',
      author_email='gbeaulieu@koumbit.org',
      packages=['django-library', 'django-library.library'],
      url='https://github.com/GuillaumeFromage/django-library',
      package_data = { 'django-library.library': ['static/imgs/*', 'static/css/*'] }
     )
