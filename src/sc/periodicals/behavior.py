# -*- coding: utf-8 -*-

from sc.periodicals.content import IPeriodical
from sc.periodicals.interfaces import INameFromNumber
from zope.component import adapts
from zope.interface import implements


class NameFromEdition(object):
    """A name chooser for a Zope object manager.

    If the object is adaptable to or provides INameFromEditon, use the
    periodical number to generate a name.
    """
    implements(INameFromNumber)
    adapts(IPeriodical)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return unicode(self.context.number)
