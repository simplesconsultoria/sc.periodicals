# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from collective.nitf.content import INITF
from five import grok
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.directives import dexterity
from Products.CMFPlone.utils import getToolByName
from sc.periodicals.config import PROJECTNAME
from sc.periodicals.content import IPeriodical
from sc.periodicals.interfaces import IPeriodicalLayer
from zope.interface import Interface

import locale
import logging
import os

# HACK: we need to return localized formated dates and I didn't found any way
#       to do it in Plone or Zope; I don't know if this is the right way but
#       seems to be working
logger = logging.getLogger(PROJECTNAME)
LC_TIME = os.getenv('LC_TIME')
locale.setlocale(locale.LC_TIME, LC_TIME)
logger.info(
    u"Locale category for the formatting of time was set to %s according "
    u"to the value of the 'LC_TIME' environment variable" % LC_TIME)

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

    def publication_date(self, format=None):
        """Return the periodical publication date in the specified localized
        format (see HACK at the beginning of module for more information).
        """
        periodical = self.periodical()
        # XXX: publication_date should be required
        #      see: https://github.com/simplesconsultoria/sc.periodicals/issues/5
        if periodical.publication_date:
            return periodical.publication_date.strftime(format)
