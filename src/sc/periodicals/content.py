# -*- coding: utf-8 -*-

from sc.periodicals import _
from five import grok
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.dexterity.content import Container
from plone.directives import form
from zope import schema
from Products.CMFCore.utils import getToolByName

from plone.namedfile.field import NamedBlobImage


class IPeriodical(form.Schema):
    """A folderish content types to include articles in it.
    """

    form.order_before(number='IDublinCore.title')
    number = schema.Int(
        title=_(u'Edition number'),
        description=_(u'help_edition_number',
            default=u'A number for this edition.'),
        required=True,
    )

    cover_image = NamedBlobImage(
        title=_(u'Cover image'),
        description=_(u'help_cover_image',
            default=u'A cover image for periodical.'),
        required=False,
    )

    circulation_date = schema.Date(
        title=_(u'Circulation date'),
        description=_(u'help_circulation_date',
            default=u''),
        required=False,
    )


class Periodical(Container):
    grok.implements(IPeriodical)


# TODO: move this to Dexterity's core
@form.default_value(field=IDublinCore['language'])
def language_default_value(data):
    """ Returns portal's default language or None.
    """
    portal_properties = getToolByName(data, "portal_properties", None)
    if portal_properties is not None:
        site_properties = getattr(portal_properties, 'site_properties', None)
        if site_properties is not None:
            if site_properties.hasProperty('default_language'):
                return site_properties.getProperty('default_language')
