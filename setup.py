# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0b2.dev0'
description = "A content type to register periodicals of a printed publication."
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='sc.periodicals',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: JavaScript",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Office/Business :: News/Diary",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone dexterity periodicals edition simples_consultoria',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='https://github.com/simplesconsultoria/sc.periodicals/',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['sc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.nitf',
          'plone.app.content',
          'plone.app.dexterity[relations]',
          'plone.app.imaging',
          'plone.app.layout',
          'plone.app.portlets',
          'plone.app.textfield',
          'plone.autoform',
          'plone.behavior',
          'plone.dexterity',
          'plone.memoize',
          'plone.namedfile',
          'plone.portlets',
          'plone.supermodel',
          'Products.CMFCore',
          'Products.CMFPlone >=4.3',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.formlib',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.customerize',
              'plone.app.robotframework',  # XXX: plone.app.event depends on this in Plone 5
              'plone.app.testing',
              'plone.browserlayer',
              'plone.registry',
              'plone.testing',
              'zope.viewlet',
          ],
      },
      entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
        """,
      )
