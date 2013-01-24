# -*- coding: utf-8 -*-

from sc.periodicals import _
from sc.periodicals.content import IPeriodical
from sc.periodicals.vocab import thumbnail_sizes_vocabulary
from collective.nitf.content import INITF
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements
from Acquisition import aq_inner


class ILastEditionPortlet(IPortletDataProvider):
    """
    A portlet which shows the last edition of a periodical.
    """

    header = schema.TextLine(
        title=_(u'Header'),
        description=_(u"The header for the portlet. Leave empty for none."),
        required=False)

    size = schema.Choice(
        title=u"Image size",
        required=True,
        default='thumb',
        source=thumbnail_sizes_vocabulary)

    quantity = schema.Int(
        title=_(u'Articles quantity'),
        description=_(u'Quantity of articles in portlet'),
        required=False,
        default=2)

    text = schema.Text(
        title=_(u'Text'),
        required=False)


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ILastEditionPortlet)

    header = u""

    def __init__(self, header=u"", size=None, quantity=2, text=u""):

        self.header = header
        self.size = size
        self.quantity = quantity
        self.text = text

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
        @return: returns the header for the portlet
        """
        return self.data.header

    def get_last_edition(self):
        """
        @return: returns the catalog results (brains) if exists
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

        quantity = self.data.quantity
        if not quantity:
            quantity = 2
        last_edition = self.get_last_edition()
        if last_edition:
            periodical = last_edition.getObject()

        else:
            return None

        if periodical:
            articles = catalog(
                object_provides=INITF.__identifier__,
                path='/'.join(periodical.getPhysicalPath()),
                sort_on='getObjPositionInParent',
                sort_limit=quantity,
                review_state='published',
            )
            if articles:
                return articles
            else:
                return None
        else:
            return None

    def get_size(self):
        return self.data.size

    def get_text(self, mt='text/x-html-safe'):
        """Use the safe_html transform to protect text output. This also
        ensures that resolve UID links are transformed into real links.

        Function retired from plone.portlet.static
        """
        orig = self.data.text
        if not orig:
            orig = u""
        context = aq_inner(self.context)
        if not isinstance(orig, unicode):
            # Apply a potentially lossy transformation, and hope we stored
            # utf-8 text. There were bugs in earlier versions of this portlet
            # which stored text directly as sent by the browser, which could
            # be any encoding in the world.
            orig = unicode(orig, 'utf-8', 'ignore')

        # Portal transforms needs encoded strings
        orig = orig.encode('utf-8')

        transformer = getToolByName(context, 'portal_transforms')
        data = transformer.convertTo(mt, orig,
                                     context=context, mimetype='text/html')
        result = data.getData()
        if result:
            if isinstance(result, str):
                return unicode(result, 'utf-8')
            return result
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
