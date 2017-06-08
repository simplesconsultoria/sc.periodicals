# -*- coding: utf-8 -*-
from collective.nitf.content import INITF
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFPlone.i18nl10n import monthname_msgid
from Products.CMFPlone.i18nl10n import monthname_msgid_abbr
from Products.CMFPlone.i18nl10n import weekdayname_msgid
from Products.CMFPlone.i18nl10n import weekdayname_msgid_abbr
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.periodicals.content import IPeriodical
from zope.i18n import translate

import re


class View(BrowserView):

    """Default view."""

    index = ViewPageTemplateFile('view.pt')

    def __call__(self):
        return self.index()

    def results(self, object_name=None):
        """Return a list of News Article brains inside the Periodical object."""
        path = '/'.join(self.context.getPhysicalPath())
        return api.content.find(
            object_provides=INITF.__identifier__,
            path=path,
            sort_on='getObjPositionInParent'
        )


class PeriodicalHeader(ViewletBase):

    """A viewlet to include a header in the container (Periodical) and
    contained (News Article) elements.
    """

    def update(self):
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

    def publication_date(self, format='%B %Y'):
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
            # normalize to unicode then encode to utf-8
            result = safe_unicode(result).encode('utf-8')
            # process the remaining format codes normally
            return periodical.publication_date.strftime(result)
