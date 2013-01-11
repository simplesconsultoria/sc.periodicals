# -*- coding: utf-8 -*-

from sc.periodicals.content import IPeriodical
from sc.periodicals.testing import INTEGRATION_TESTING
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from Products.CMFPlone.interfaces import INonStructuralFolder
from zope.component import createObject
from zope.component import queryUtility

import unittest2 as unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('Periodical', 'p1')
        self.p1 = self.folder['p1']

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

    def test_is_not_non_structural_folder(self):
        """
        Periodical CT doesn't implement INonStructuralFolder any longer
        to allow folder factories menu
        """
        self.assertFalse(INonStructuralFolder.providedBy(self.p1))

    def test_allowable_types(self):
        # test if collective.nitf.content is allowed in Periodical CT
        fti = queryUtility(IDexterityFTI, name='Periodical')
        allowed_types = fti.allowed_content_types
        self.assertTrue('collective.nitf.content' in allowed_types)
