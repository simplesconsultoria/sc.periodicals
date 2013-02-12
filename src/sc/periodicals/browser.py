# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from collective.nitf.content import INITF
from five import grok
from plone.directives import dexterity
from Products.CMFPlone.utils import getToolByName
from sc.periodicals.content import IPeriodical
from sc.periodicals.interfaces import IPeriodicalLayer

grok.templatedir('templates')


class View(dexterity.DisplayForm):
    """ Default view.
    """
    grok.context(IPeriodical)
    grok.require('zope2.View')
    grok.layer(IPeriodicalLayer)

    def update(self):
        self.context = aq_inner(self.context)

    def results(self, object_name=None):
        """ Return a list of News Article brains inside the Periodical object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(object_provides=INITF.__identifier__, path=path, sort_on='getObjPositionInParent')
        return brains
