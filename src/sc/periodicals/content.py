# -*- coding: utf-8 -*-

from five import grok
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from sc.periodicals import _
from zope import schema


class IPeriodical(form.Schema):
    """A folderish content types to include articles in it.
    """

    form.order_before(number='IDublinCore.title')
    number = schema.Int(
        title=_(u'Number'),
        description=_(u'help_number',
            default=u"The number of the periodical."),
        required=True,
    )

    image = NamedBlobImage(
        title=_(u'Image'),
        description=_(u'help_image',
            default=u"An image associated with the periodical. "
                    u"For printed periodicals you should use the cover."),
        required=False,
    )

    publication_date = schema.Date(
        title=_(u'Publication Date'),
        description=_(u'help_publication_date',
            default=u"The publication date of the periodical "
                    u"(do not confuse with the effective date)."),
        required=False,
    )


class Periodical(Container):
    grok.implements(IPeriodical)
