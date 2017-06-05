# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView as View
from sc.periodicals.interfaces import IPeriodicalLayer
from sc.periodicals.testing import INTEGRATION_TESTING
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class ViewletTestCase(unittest.TestCase):
    """for more information on how to test viewlets, see:
    http://developer.plone.org/views/viewlets.html#finding-viewlets-programmatically
    """

    layer = INTEGRATION_TESTING
    viewlet_name = 'sc.periodicals.periodicalheader'

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IPeriodicalLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def _get_viewlet_manager(self, context, request):
        view = View(context, request)
        manager = queryMultiAdapter(
            (context, request, view), IViewletManager, 'plone.abovecontent')

        return manager

    def test_viewlet_is_registered(self):
        context = self.portal
        request = self.request
        manager = self._get_viewlet_manager(context, request)
        self.assertTrue(manager)

        manager.update()
        self.assertIn(self.viewlet_name, manager)

    def test_viewlet_is_available_on_periodicals(self):
        self.folder.invokeFactory('Periodical', 'periodical')
        context = self.folder['periodical']
        request = self.request
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager[self.viewlet_name]
        viewlet.update()
        self.assertTrue(viewlet.available())

    def test_viewlet_is_available_on_news_articles_inside_periodicals(self):
        self.folder.invokeFactory('Periodical', 'periodical')
        self.periodical = self.folder['periodical']
        self.periodical.invokeFactory('collective.nitf.content', 'n1')
        context = self.periodical['n1']
        request = self.request
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager[self.viewlet_name]
        viewlet.update()
        self.assertTrue(viewlet.available())

    def test_viewlet_is_not_available_on_news_articles_outside_periodicals(self):
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        context = self.folder['n1']
        request = self.request
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager['sc.periodicals.periodicalheader']
        viewlet.update()
        self.assertFalse(viewlet.available())

    def test_periodical_url(self):
        self.folder.invokeFactory('Periodical', 'periodical')
        periodical_url = 'http://nohost/plone/test-folder/periodical'

        # first test in the context of a periodical
        context = self.folder['periodical']
        request = self.request
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager[self.viewlet_name]
        viewlet.update()
        self.assertEqual(viewlet.periodical_url(), periodical_url)

        # now test in the context of a News Article
        self.folder.periodical.invokeFactory('collective.nitf.content', 'n1')
        context = self.folder.periodical['n1']
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager[self.viewlet_name]
        viewlet.update()
        self.assertEqual(viewlet.periodical_url(), periodical_url)

    def test_number(self):
        number = 99
        self.folder.invokeFactory('Periodical', 'periodical', number=number)

        # first test in the context of a periodical
        context = self.folder['periodical']
        request = self.request
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager[self.viewlet_name]
        viewlet.update()
        self.assertEqual(viewlet.number(), number)

        # now test in the context of a News Article
        self.folder.periodical.invokeFactory('collective.nitf.content', 'n1')
        context = self.folder.periodical['n1']
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager[self.viewlet_name]
        viewlet.update()
        self.assertEqual(viewlet.number(), number)

    def _test_publication_date(self):
        publication_date = ''
        self.folder.invokeFactory(
            'Periodical', 'periodical', publication_date=publication_date)

        # first test in the context of a periodical
        context = self.folder['periodical']
        request = self.request
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager[self.viewlet_name]
        viewlet.update()
        self.assertEqual(viewlet.number(), publication_date)

        # now test in the context of a News Article
        self.folder.periodical.invokeFactory('collective.nitf.content', 'n1')
        context = self.folder.periodical['n1']
        manager = self._get_viewlet_manager(context, request)

        manager.update()
        viewlet = manager[self.viewlet_name]
        viewlet.update()
        self.assertEqual(viewlet.number(), publication_date)
