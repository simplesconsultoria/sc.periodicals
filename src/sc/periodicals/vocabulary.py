# -*- coding: utf-8 -*-
from plone.app.imaging.utils import getAllowedSizes
from zope.schema.vocabulary import SimpleVocabulary


def thumbnail_sizes_vocabulary(context):
    """Builds a vocabulary of thumbnail sizes. An example item in vocabulary
    would have title set to "tile (64, 64)" and value to ('tile', 64, 64).

    :returns: Vocabulary items for each allowed thumbnail size."
    rtype: SimpleVocabulary
    """
    terms = []
    for name, size in getAllowedSizes().iteritems():
        terms.append(SimpleVocabulary.createTerm(name, str(name), u'%s' % name))
    return SimpleVocabulary(terms)