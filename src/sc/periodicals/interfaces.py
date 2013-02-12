# -*- coding: utf-8 -*-

from plone.app.content.interfaces import INameFromTitle
from zope.interface import Interface


class IPeriodicalLayer(Interface):
    """ A layer specific for this add-on product.
    """


class INameFromNumber(INameFromTitle):

    def title():
        """Return a processed title"""
