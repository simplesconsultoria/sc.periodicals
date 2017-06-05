# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.nitf.content import INITF
from five import grok
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.directives import dexterity
from Products.CMFPlone.i18nl10n import monthname_msgid
from Products.CMFPlone.i18nl10n import monthname_msgid_abbr
from Products.CMFPlone.i18nl10n import weekdayname_msgid
from Products.CMFPlone.i18nl10n import weekdayname_msgid_abbr
from Products.CMFPlone.utils import getToolByName
from sc.periodicals.content import IPeriodical
from sc.periodicals.interfaces import IPeriodicalLayer
from zope.i18n import translate
from zope.interface import Interface

import re


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

    def _translate(self, msgid):
        return translate(msgid, 'plonelocales', context=self.request)

    def publication_date(self, format=None):
        """Return the periodical publication date localized and in the format
        specified. For more information on format codes see:
        http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        """
        periodical = self.periodical()
        if periodical.publication_date:
            day = periodical.publication_date.weekday()
            month = periodical.publication_date.month

            # let's map and translate the directives we care about
            # an example of what we get for Friday, April 26, 2013:
            # {'%a': 'Fri', '%A': 'Friday', '%b': 'Apr', '%A': 'April'}
            codes = {
                '%a': self._translate(weekdayname_msgid_abbr(day)),
                '%A': self._translate(weekdayname_msgid(day)),
                '%b': self._translate(monthname_msgid_abbr(month)),
                '%B': self._translate(monthname_msgid(month)),
            }

            # replace occurrences of directives with our translated strings
            prog = re.compile('|'.join(codes.keys()))
            result = prog.sub(lambda m: codes[m.group(0)], format)
            # process the remaining format codes normally
            return periodical.publication_date.strftime(result)
