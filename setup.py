#!/usr/bin/env python
"""
Install scitools with easyviz

Usage:

python setup.py install [, --prefix=$PREFIX --easyviz_backend backendname]
"""

import os, sys, socket, re, glob, platform

scripts = [os.path.join("bin", "scitools"), os.path.join("bin", "pyreport")]

if platform.system() == "Windows" or "bdist_wininst" in sys.argv:
    # In the Windows command prompt we can't execute Python scripts 
    # without a .py extension. A solution is to create batch files
    # that runs the different scripts.
    batch_files = []
    for script in scripts:
        batch_file = script + ".bat"
        f = open(batch_file, "w")
        f.write('python "%%~dp0\%s" %%*\n' % os.path.split(script)[1])
        f.close()
        batch_files.append(batch_file)
    scripts.extend(batch_files)

# make sure we import from scitools in this package, not an installed one:
sys.path.insert(0, os.path.join('lib')); import scitools

# NOTE: now we force matplotlib as default backend if it is installed:
try:
    import matplotlib
    default_easyviz_backend = 'matplotlib'
except ImportError:
    default_easyviz_backend = 'gnuplot'

# modify config file so that it sets the wanted backend for easyviz
config_file = os.path.join('lib', 'scitools', 'scitools.cfg')
if '--easyviz_backend' in sys.argv or default_easyviz_backend != 'gnuplot':
    if '--easyviz_backend' in sys.argv:
        try:
            default_easyviz_backend = \
                sys.argv[sys.argv.index('--easyviz_backend') + 1]
        except IndexError:
            print '--easyviz_backend must be followed by a name like '\
                '\ngnuplot, matplotlib, etc.'
            sys.exit(1)
    print 'default scitools.easyviz backend is now', default_easyviz_backend
    print 'could be set by the --easyviz_backend option to setup.py'
    if default_easyviz_backend != 'gnuplot':
        # write new config file and change backend line
        os.rename(config_file, config_file + '.cop')
        infile = open(config_file + '.cop', 'r')
        outfile = open(config_file, 'w')
        for line in infile:
            if line.lstrip().startswith('backend'):
                outfile.write('backend     = %s  ; default backend\n' % \
                              default_easyviz_backend)
            else:
                outfile.write(line)
        infile.close();  outfile.close()

if  __file__ == 'setupegg.py':
    # http://peak.telecommunity.com/DevCenter/setuptools
    from setuptools import setup, Extension
else:
    from distutils.core import setup

setup(
    version = str(scitools.version), 
    author = ', '.join(scitools.author),
    author_email = "<hpl@simula.no>",
    description = scitools.__doc__,
    license = "BSD",
    name = "SciTools",
    url = "http://scitools.googlecode.com",
    package_dir = {'': 'lib'},
    packages = ["scitools",
                os.path.join("scitools", "easyviz"), 
		],
    package_data = {'': ['scitools.cfg']},
    scripts = scripts,
    data_files=[(os.path.join("share", "man", "man1"),
                 [os.path.join("doc", "man", "man1", "scitools.1.gz"),
                  os.path.join("doc", "man", "man1", "pyreport.1.gz")])],
    )

if os.path.isfile(config_file + '.cop'):
    os.rename(config_file + '.cop', config_file)

