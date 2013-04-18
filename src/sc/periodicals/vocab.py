# -*- coding: utf-8 -*-

from five import grok
from plone.app.imaging.utils import getAllowedSizes

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


@grok.provider(IContextSourceBinder)
def thumbnail_sizes_vocabulary(context):
    """Builds a vocabulary of thumbnail sizes. An example item in vocabulary
    would have title set to "tile (64, 64)" and value to ('tile', 64, 64).

    :returns: Vocabulary items for each allowed thumbnail size."
    rtype: SimpleVocabulary
    """
    terms = []
    for name, size in sorted((item for item in getAllowedSizes().iteritems()),
                              key=lambda item: item[1][0]):
        terms.append(SimpleVocabulary.createTerm(name, str(name), u"%s" % name))
    return SimpleVocabulary(terms)
