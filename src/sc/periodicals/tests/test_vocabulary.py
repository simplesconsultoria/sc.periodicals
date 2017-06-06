# -*- coding: utf-8 -*-
from sc.periodicals.testing import FUNCTIONAL_TESTING
from sc.periodicals.vocabulary import thumbnail_sizes_vocabulary

import unittest


class VocabulariesTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_thumbnail_sizes_vocabulary(self):
        self.assertTrue(thumbnail_sizes_vocabulary)

    def test_thumbnail_sizes_vocabulary_quantity(self):
        vocabulary = thumbnail_sizes_vocabulary(self.portal)
        self.assertEqual(len(vocabulary.by_token), 7)

    def test_thumbnail_sizes_vocabulary_items(self):
        vocabulary = thumbnail_sizes_vocabulary(self.portal)
        clients = ['mini', 'thumb', 'large', 'listing', 'tile', 'preview', 'icon']
        for term in vocabulary.by_token.keys():
            self.assertIn(term, clients)
