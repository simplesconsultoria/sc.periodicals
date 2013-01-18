# -*- coding: utf-8 -*-

from sc.periodicals import _
from sc.periodicals.content import IPeriodical
from collective.nitf.content import INITF
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements


class ILastEditionPortlet(IPortletDataProvider):
    """
    A portlet which shows the last edition of a periodical.
    """

    header = schema.TextLine(
        title=_(u'Header'),
        description=_(u"The header for the portlet. Leave empty for none."),
        required=False)


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ILastEditionPortlet)

    header = u""

    def __init__(self, header=u""):

        self.header = header

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return _(u"Last Edition")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('last_edition.pt')

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        return self.get_last_edition()

    def getHeader(self):
        """
        Returns the header for the portlet
        """
        return self.data.header

    def get_last_edition(self):
        """
        @return:returns the catalog results (brains) if exists
        """
        catalog = getToolByName(self, 'portal_catalog')
        results = catalog(
            object_provides=IPeriodical.__identifier__,
            sort_on='created',
            sort_order='descending',
            review_state='published',
        )
        if results:
            return results[0]
        else:
            return None

    def get_articles(self):
        """
        @return:returns the articles in a periodical
        """
        catalog = getToolByName(self, 'portal_catalog')

        last_edition = self.get_last_edition()
        if last_edition:
            periodical = last_edition.getObject()

        else:
            return None

        if periodical:
            articles = catalog(
                object_provides=INITF.__identifier__,
                path='/'.join(periodical.getPhysicalPath()),
                sort_on='created',
                sort_order='descending',
                sort_limit=2,
                review_state='published',
            )
            if articles:
                return articles
            else:
                return None
        else:
            return None


class AddForm(base.AddForm):

    form_fields = form.Fields(ILastEditionPortlet)

    label = _(u"Add last edition Portlet")
    description = _(u"This portlet display the last edition of a periodical.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(ILastEditionPortlet)

    label = _(u"Edit last edition Portlet")
    description = _(u"This portlet display the last edition of a periodical.")
