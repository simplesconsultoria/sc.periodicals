# -*- coding: utf-8 -*-

from sc.periodicals.interfaces import IPeriodicalLayer
from sc.periodicals.testing import INTEGRATION_TESTING
from plone.app.customerize import registration
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
from zope.interface import directlyProvides
from zope.app.file.tests.test_image import zptlogo
from StringIO import StringIO

import unittest2 as unittest


class DefaultViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IPeriodicalLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Periodical', 'periodical')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.p1 = self.portal['periodical']

    def test_default_view_is_registered(self):
        pt = self.portal['portal_types']
        self.assertEqual(pt['Periodical'].default_view, 'view')

        registered = [v.name for v in registration.getViews(IPeriodicalLayer)]
        self.assertTrue('view' in registered)

    def test_results(self):
        view = getMultiAdapter((self.p1, self.request), name='view')
        self.assertEqual(len(view.results()), 0)

        self.p1.invokeFactory('collective.nitf.content', 'n1')
        self.assertEqual(len(view.results()), 1)

    def test_getImage(self):
        view = getMultiAdapter((self.p1, self.request), name='view')
        self.assertEqual(view.getImage(), None)

        self.p1.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.p1['n1']
        n1.invokeFactory('Image', 'foo', title='bar', description='baz', image=StringIO(zptlogo))
        image = view.getImage()
        self.assertEqual(len(image), 1)
        self.assertEqual(image.id, 'foo')
        self.assertEqual(image.Title(), 'bar')
        self.assertEqual(image.Description(), 'baz')
