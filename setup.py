import os
from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
DESCRIPTION = README

REQUIRES = ()

setup(name='Sack',
      version='0.1',
      description='A local dynamic PyPi repository/builder',
      long_description='\n\n'.join((README, CHANGES)),
      classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Software Distribution',
        ),
      author='Karol Pasternak',
      author_email='karol@pasternak.pro',
      url='http://packages.python.org/Sack',
      keywords='eggs easy_install pip package static repository pypi',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIRES,
      test_suite='sack.tests',
      entry_points='''
      [console_scripts]
      sack = sack.main:main
      ''')
