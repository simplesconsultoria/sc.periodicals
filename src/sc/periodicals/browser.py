# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from sc.periodicals.content import IPeriodical
from sc.periodicals.interfaces import IPeriodicalLayer
from five import grok
from plone.directives import dexterity
from Products.CMFPlone.utils import getToolByName
from collective.nitf.content import INITF

grok.templatedir('templates')


class View(dexterity.DisplayForm):
    """ Default view looks like a News Item.
    """
    grok.context(IPeriodical)
    grok.require('zope2.View')
    grok.layer(IPeriodicalLayer)

    def update(self):
        self.context = aq_inner(self.context)

    def results(self, object_name=None):
        """ Return a list of brains inside the Periodical object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(object_provides=INITF.__identifier__, path=path, sort_on='getObjPositionInParent')
        return brains

    def getImage(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        images = catalog(Type='Image', path=path, sort_on='getObjPositionInParent')
        if len(images) > 0:
            return images[0].getObject()
        return None
