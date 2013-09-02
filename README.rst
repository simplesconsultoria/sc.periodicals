**************
sc.periodicals
**************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

This package defines a folderish content type that defines a Periodical. A
periodical has a number, an image associated and a publication date; it can
contain only News Articles as defined in the `collective.nitf`_ package.

The package also defines a portlet that displays the latest published
periodical on the site.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.periodicals.png?branch=master
    :target: http://travis-ci.org/simplesconsultoria/sc.periodicals

.. image:: https://coveralls.io/repos/simplesconsultoria/sc.periodicals/badge.png?branch=master
    :target: https://coveralls.io/r/simplesconsultoria/sc.periodicals

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``sc.periodicals`` to the list of eggs to
   install::

    [buildout]
    ...
    eggs =
        sc.periodicals

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``sc.periodicals`` and click the 'Activate' button.

.. Note::
    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.

Usage
^^^^^

TBA.

Portlet
+++++++

The package includes a portlet that shows the latest published periodical and
its contained news articles.

- Go to the "Manage Portlets" page and select "Latest Periodical"
- Enter a header (if needed), an image scale, the number of published News
  Articles to display and a text.

The portlet will be shown if at least one Periodical is published on the site.

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`collective.nitf`: http://pypi.python.org/pypi/collective.nitf
.. _`opening a support ticket`: https://github.com/simplesconsultoria/sc.periodicals/issues
