# -*- coding: utf-8 -*-

from five import grok

from sc.periodicals.content import IPeriodical
from sc.periodicals.interfaces import INameFromEdition
from rwproperty import getproperty, setproperty
from zope.container.interfaces import INameChooser
from zope.interface import implements
from zope.component import adapts
from Acquisition import aq_inner, aq_base

ATTEMPTS = 100


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
#
#    def chooseName(self, name, object):
#        import pdb;pdb.set_trace()
#        container = aq_inner(self.context)
#        if not name:
#            nameFromEdition = INameFromEdition(object, None)
#            if nameFromEdition is not None:
#                number = nameFromEdition.number_edition
#            if not number:
#                number = getattr(aq_base(object), 'id', None)
#            if not number:
#                number = getattr(aq_base(object), 'portal_type', None)
#            if not number:
#                number = object.__class__.__name__
#
#        return self._findUniqueName(number, object)
#
#    def _findUniqueName(self, name, object):
#        """Find a unique name in the parent folder, based on the given id, by
#        appending -n, where n is a number greater than 1, or just the id if
#        it's ok.
#        """
#        idx = 1
#        while idx <= ATTEMPTS:
#            new_name = "%s-%d%s" % (name, idx)
#            return new_name
#
#        raise ValueError("Cannot find a unique name based on %s after %d attemps." % (name, ATTEMPTS,))
