# -*- coding: utf-8 -*-

from five import grok
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from sc.periodicals import _
from zope import schema


def has_image(periodical):
    image = periodical.image
    return (image and image.getSize())


class IPeriodical(form.Schema):
    """A folderish content types to include articles in it.
    """

    form.order_before(number='IDublinCore.title')
    number = schema.Int(
        title=_(u'Number'),
        description=_(
            u'help_number',
            default=u"The number of the periodical."),
        required=True,
    )

    image = NamedBlobImage(
        title=_(u'Image'),
        description=_(
            u'help_image',
            default=u"An image associated with the periodical. "
                    u"For printed periodicals you should use the cover."),
        required=False,
    )

    publication_date = schema.Date(
        title=_(u'Publication Date'),
        description=_(
            u'help_publication_date',
            default=u"The publication date of the periodical "
                    u"(do not confuse with the effective date)."),
        required=False,
    )


class Periodical(Container):
    grok.implements(IPeriodical)

    def image_thumb(self):
        ''' Return a thumbnail '''
        if not has_image(self):
            return None
        view = self.unrestrictedTraverse('@@images')
        return view.scale(fieldname='image',
                          scale='thumb').index_html()

    def tag(self, scale='thumb', css_class='tileImage', **kw):
        ''' Return a tag to the image '''
        if not has_image(self):
            return ''
        view = self.unrestrictedTraverse('@@images')
        return view.tag(fieldname='image',
                        scale=scale,
                        css_class=css_class,
                        **kw)

    # XXX: we have to figure out an unified way of doing this
    #      above we needed those for summary_view in collections
    #      below we need this for the same on sumary_view in folders?
    #      taken from collective.nitf

    def getImage(self):
        """Return the first Image inside the News Article.
        """
        content_filter = {'portal_type': 'Image'}
        images = self.listFolderContents(content_filter)
        return images[0] if len(images) > 0 else None

    image = getImage  # XXX: a hack to support summary_view
