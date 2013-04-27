# -*- coding: utf-8 -*-

from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.file import NamedBlobImage
from plone.uuid.interfaces import IAttributeUUID
from sc.periodicals.content import IPeriodical
from sc.periodicals.testing import INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility

import os
import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.setup_content(self.folder)

    def setup_content(self, folder):
        path = os.path.dirname(__file__)
        data = open(os.path.join(path, 'cover.png')).read()
        image = NamedBlobImage(data, 'image/png', u'cover.png')
        folder.invokeFactory('Periodical', 'p1')
        p1 = self.folder['p1']
        p1.image = image
        self.p1 = p1

    def test_adding(self):
        self.assertTrue(IPeriodical.providedBy(self.p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Periodical')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Periodical')
        schema = fti.lookupSchema()
        self.assertEqual(IPeriodical, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Periodical')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IPeriodical.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.p1))
        self.assertTrue(IAttributeUUID.providedBy(self.p1))

    def test_locking_behavior_available(self):
        # ILocking is not applied by default, but must be available if needed
        try:
            from plone.app.lockingbehavior.behaviors import ILocking
            assert ILocking  # Pyflakes
        except ImportError:
            self.fail('ILocking behavior not available')

    def test_allowable_types(self):
        # test if collective.nitf.content is allowed in Periodical CT
        fti = queryUtility(IDexterityFTI, name='Periodical')
        allowed_types = fti.allowed_content_types
        self.assertIn('collective.nitf.content', allowed_types)

    def test_image_thumb(self):
        """Test if traversing to image_thumb returns an image.
        """
        p1 = self.p1
        self.assertTrue(p1.restrictedTraverse('image_thumb')().read())

    def test_image_thumb_no_image(self):
        """Test if traversing to image_thumb returns None if we have no image
        there.
        """
        p1 = self.p1
        p1.image = None
        self.assertEqual(p1.restrictedTraverse('image_thumb')(), None)

        # set an empty image file
        p1.image = NamedBlobImage('', 'image/jpeg', u'picture.jpg')
        self.assertEqual(p1.restrictedTraverse('image_thumb')(), None)

    def test_image_tag(self):
        """Test if tag method works as expected.
        """
        p1 = self.p1
        expected = u'<img src="http://nohost/plone/test-folder/p1/@@images/'
        self.assertTrue(p1.tag().startswith(expected))

        expected = u'title="" height="128" width="99" class="tileImage" />'
        self.assertTrue(p1.tag().endswith(expected))

    def test_image_tag_no_image(self):
        """Test if tag method works as expected.
        """
        p1 = self.p1
        p1.image = None
        expected = u''
        self.assertEqual(p1.tag(), expected)

        # set an empty image file
        p1.image = NamedBlobImage('', 'image/jpeg', u'picture.jpg')
        self.assertEqual(p1.tag(), expected)
