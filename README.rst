==============
sc.periodicals
==============

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

This package defines a folderish content type that defines a Periodical. A
periodical has a number, an image associated and a publication date; it can
contain only News Articles as defined in the `collective.nitf`_ package.

The package also defines a portlet that displays the latest published
periodical on the site.

Don't Panic
-----------

Portlet
^^^^^^^

The package includes a portlet that shows the latest published periodical and
its contained news articles.

- Go to the "Manage Portlets" page and select "Latest Periodical"
- Enter a header (if needed), an image scale, the number of published News
  Articles to display and a text.

The portlet will be shown if at least one Periodical is published on the site.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.periodicals.png
    :target: http://travis-ci.org/simplesconsultoria/sc.periodicals

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`collective.nitf`: http://pypi.python.org/pypi/collective.nitf
.. _`opening a support ticket`: https://github.com/simplesconsultoria/sc.periodicals/issues
