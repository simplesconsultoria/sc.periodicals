# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from collective.nitf.content import INITF
from five import grok
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.directives import dexterity
from Products.CMFPlone.utils import getToolByName
from sc.periodicals.content import IPeriodical
from sc.periodicals.interfaces import IPeriodicalLayer
from zope.interface import Interface

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


class PeriodicalHeader(grok.Viewlet):
    """A viewlet to include a header in the container (Periodical) and
    contained (News Article) elements.
    """
    grok.name('sc.periodicals.periodicalheader')
    grok.context(Interface)
    grok.layer(IPeriodicalLayer)
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContent)

    def update(self):
        self.context = aq_inner(self.context)
        # is context a Periodical?
        self.is_periodical = IPeriodical.providedBy(self.context)
        # is context a News Article inside a Periodical?
        self.is_news_article = INITF.providedBy(self.context) and \
            IPeriodical.providedBy(self.context.__parent__)

    def available(self):
        return self.is_periodical or self.is_news_article

    def periodical(self):
        if self.is_periodical:
            return self.context
        if self.is_news_article:
            return self.context.__parent__

    def periodical_url(self):
        return self.periodical().absolute_url()

    def number(self):
        periodical = self.periodical()
        return periodical.number

    def publication_date(self):
        periodical = self.periodical()
        return periodical.publication_date
