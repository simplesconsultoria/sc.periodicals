# -*- coding: utf-8 -*-

from sc.periodicals.content import IPeriodical
from sc.periodicals.interfaces import INameFromEdition
from zope.interface import implements
from zope.component import adapts


class NameFromEdition(object):
    """A name chooser for a Zope object manager.

    If the object is adaptable to or provides INameFromEditon, use the
    edition number to generate a name.
    """
    implements(INameFromEdition)
    adapts(IPeriodical)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return str(self.context.number)
