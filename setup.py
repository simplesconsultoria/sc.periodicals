from setuptools import setup, find_packages
import os

version = '1.0a2.dev0'
description = "A content type to register periodicals of a printed publication."
long_description = open("README.txt").read() + "\n" +\
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +\
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +\
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='sc.periodicals',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='plone dexterity periodicals edition simples_consultoria',
      author='Gustavo Lepri',
      author_email='lepri@simplesconsultoria.com.br',
      url='https://github.com/simplesconsultoria/sc.periodicals/',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['sc'],
      include_package_data=True,
      zip_safe=False,
    install_requires=[
        'setuptools',
        'Pillow',
        'Products.CMFPlone>=4.2',
        'collective.nitf',
        'plone.namedfile[blobs]',
        'plone.formwidget.namedfile',
        'plone.app.dexterity[grok]',
        'plone.behavior',
        ],
    extras_require={
        'test': ['plone.app.testing'],
        },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
