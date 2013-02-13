# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from collective.nitf.content import INITF
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.periodicals import _
from sc.periodicals.content import IPeriodical
from sc.periodicals.vocab import thumbnail_sizes_vocabulary
from zope import schema
from zope.formlib import form
from zope.interface import implements


class ILatestPeriodicalPortlet(IPortletDataProvider):
    """This portlet shows the latest published Periodical.
    """

    header = schema.TextLine(
        title=_(u'Portlet header'),
        description=_(
            'help_header',
            default=u"The header for the portlet. Leave empty for none."),
        required=False)

    image_scale = schema.Choice(
        title=u"Image scale",
        description=_(
            'help_image_scale',
            default=u"The scale of the image associated with the periodical."),
        required=True,
        default='thumb',
        source=thumbnail_sizes_vocabulary)

    count = schema.Int(
        title=_(u"Number of items to display"),
        description=_(
            'help_count',
            default=u'How many items to list.'),
        default=5,
        required=False)

    text = schema.Text(
        title=_(u'Text'),
        required=False)


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ILatestPeriodicalPortlet)

    def __init__(self, header=u"", image_scale=None, count=5, text=u""):

        self.header = header
        self.image_scale = image_scale
        self.count = count
        self.text = text

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return _(u"Latest Periodical")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('latest_periodical.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        """Show the portlet only if there is at least one item."""
        return self.get_latest_periodical() is not None

    @property
    def title(self):
        return self.data.header

    def get_latest_periodical(self):
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

        return results[0] if results else None

    def published_news_articles(self):
        return self._data()

    @memoize
    def _data(self):
        """
        @return:returns the articles in a periodical
        """
        periodical = self.get_latest_periodical()
        if periodical is None:
            return

        periodical = periodical.getObject()

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(periodical.getPhysicalPath())
        count = self.data.count

        articles = catalog(
            object_provides=INITF.__identifier__,
            path=path,
            review_state='published',
            sort_on='getObjPositionInParent',
            sort_limit=count,
        )

        return articles[:count] if articles else None

    def get_image_scale(self):
        return self.data.image_scale

    # XXX: this method seems to be complete needless as text field is
    #      schema.Text and not RichText; we have to review this later
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

    def get_periodical_title(self):
        periodical = self.get_latest_periodical()
        return periodical.Title if periodical is not None else None


class AddForm(base.AddForm):

    form_fields = form.Fields(ILatestPeriodicalPortlet)

    label = _(u"Add Latest Periodical Portlet")
    description = _(u"This portlet display the last edition of a periodical.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(ILatestPeriodicalPortlet)

    label = _(u"Edit Latest Periodical Portlet")
    description = _(u"This portlet display the last edition of a periodical.")
