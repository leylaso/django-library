#!/usr/bin/env python

# We're using the examples from http://docs.python.org/2/distutils/setupscript.html

from distutils.core import setup

def add_folder(source):
    s = set()
    for path in os.listdir(source):
        tpath = os.path.join(source,path)
        if os.path.isfile(tpath):
            s.add(tpath)
        elif os.path.isdir(tpath):
            s = s.union(add_folder(tpath))
    return list(s)

setup(name='django-library',
      version='1.0.1', 					# errr http://semver.org/
      description='a django library management system',
      author='Guillaume Le Punk',
      author_email='gbeaulieu@koumbit.org',
      data_files = [
        ('/usr/share/django-library/library/static', add_folder(os.path.abspath('django-library/library/static'))),
        ],
      url='https://github.com/GuillaumeFromage/django-library',
      packages=['django-library', 'django-library.library'],
     )
