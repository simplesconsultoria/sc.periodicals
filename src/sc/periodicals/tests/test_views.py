# -*- coding: utf-8 -*-

from plone.app.customerize import registration
from plone.app.testing import TEST_USER_ID, setRoles
from sc.periodicals.interfaces import IPeriodicalLayer
from sc.periodicals.testing import INTEGRATION_TESTING
from sc.periodicals.testing import zptlogo
from StringIO import StringIO
from zope.component import getMultiAdapter
from zope.interface import directlyProvides

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
        self.assertIn('view', registered)

    def test_results(self):
        view = getMultiAdapter((self.p1, self.request), name='view')
        self.assertEqual(len(view.results()), 0)

        self.p1.invokeFactory('collective.nitf.content', 'n1')
        self.assertEqual(len(view.results()), 1)
