# -*- coding: utf-8 -*-

from sc.periodicals import _

from zope.interface import Interface
from plone.app.content.interfaces import INameFromTitle
from zope import schema


class IPeriodicalLayer(Interface):
    """ A layer specific for this add-on product.
    """


class INameFromEdition(INameFromTitle):
    """ A name chooser for a Zope object manager.

    If the object is adaptable to or provides INameFromEdition, use the
    edition number to generate a name.
    """

    number = schema.Int(
        title=_(u'Edition number'),
        description=_(u'help_edition_number', default=u'A number for this edition.'),
        required=True,
    )
