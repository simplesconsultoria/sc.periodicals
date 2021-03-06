# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from sc.periodicals.portlets import latest_periodical
from sc.periodicals.testing import INTEGRATION_TESTING
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class PortletTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_portlet_type_registered(self):
        name = 'sc.periodicals.LatestPeriodicalPortlet'
        last = getUtility(IPortletType, name=name)
        self.assertEqual(last.addview, name)

    def test_interfaces(self):
        last = latest_periodical.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(last))
        self.assertTrue(IPortletDataProvider.providedBy(last.data))

    def test_invoke_add_view(self):
        name = 'sc.periodicals.LatestPeriodicalPortlet'
        last = getUtility(IPortletType, name=name)
        path = '++contextportlets++plone.leftcolumn'
        mapping = self.portal.restrictedTraverse(path)

        for m in mapping.keys():
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + last.addview)
        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], latest_periodical.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.request

        mapping['latest_periodical'] = latest_periodical.Assignment()

        editview = getMultiAdapter((mapping['latest_periodical'], request), name='edit')
        self.assertTrue(isinstance(editview, latest_periodical.EditForm))

    def test_obtain_renderer(self):
        context = self.portal
        request = self.request
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn',
            context=self.portal)

        assgmnt1 = latest_periodical.Assignment()

        renderer1 = getMultiAdapter(
            (context, request, view, manager, assgmnt1), IPortletRenderer)

        self.assertTrue(isinstance(renderer1, latest_periodical.Renderer))


class RenderTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def set_default_workflow(self):
        # setup default workflow in tests
        types = ('Periodical', 'collective.nitf.content')
        self.wf.setChainForPortalTypes(types, 'simple_publication_workflow')

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.catalog = self.portal.portal_catalog
        self.wf = self.portal.portal_workflow

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Periodical', 'p1')
        self.p1 = self.portal['p1']

        self.set_default_workflow()
        self.wf.doActionFor(self.p1, 'publish')

        # Let's create 3 nitf's
        for index in range(1, 4):
            self.p1.invokeFactory(
                'collective.nitf.content',
                'section1-nitf-%s' % index)
            n = self.p1['section1-nitf-%s' % index]
            n.title = 'Section 1 Nitf %s' % index
            n.section = 'Section 1'
            n.genre = 'Genre %s' % index
            n.created = DateTime('%(year)s/1/%(index)s %(index)s:00:00' %
                                 {'year': DateTime().year(),
                                  'index': index})
            n.reindexObject()
            self.wf.doActionFor(n, 'publish')

        self.default_query = {'Type': ('News Article',),
                              'sort_on': 'getObjPositionInParent',
                              'sort_limit': 2}

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        return getMultiAdapter(
            (context, request, view, manager, assignment),
            IPortletRenderer)

    def test_render(self):

        assgmnt1 = latest_periodical.Assignment()

        r1 = self.renderer(context=self.portal, assignment=assgmnt1)
        r1.update()

    def test_portlet_header(self):

        assgmnt1 = latest_periodical.Assignment()

        r1 = self.renderer(context=self.portal, assignment=assgmnt1)
        self.assertEqual(r1.title, u'')

    def test_portlet_available(self):

        assgmnt1 = latest_periodical.Assignment()

        r1 = self.renderer(context=self.portal, assignment=assgmnt1)

        self.wf.doActionFor(self.p1, 'retract')
        self.assertFalse(r1.available)

        self.wf.doActionFor(self.p1, 'publish')
        self.assertTrue(r1.available)

    def test_articles_in_periodical(self):
        assgmnt1 = latest_periodical.Assignment(count=2)

        self.wf.doActionFor(self.p1, 'retract')
        r1 = self.renderer(context=self.portal, assignment=assgmnt1)
        self.assertFalse(r1.get_latest_periodical())
        self.assertFalse(r1.published_news_articles())

        self.wf.doActionFor(self.p1, 'publish')
        r1 = self.renderer(context=self.portal, assignment=assgmnt1)
        self.assertIsNotNone(r1.get_latest_periodical())
        self.assertEqual(len(r1.published_news_articles()), 2)

        query = self.default_query
        catalog_results = self.catalog(**query)
        self.assertEqual(
            [i.id for i in r1.published_news_articles()],
            [i.id for i in catalog_results])

    def test_text_in_portlet(self):

        assgmnt1 = latest_periodical.Assignment(text=u'Praesent augue lorem, sagittis ut.')

        r1 = self.renderer(context=self.portal, assignment=assgmnt1)
        self.assertTrue(r1.get_text() == u'Praesent augue lorem, sagittis ut.')

    def test_thumbnail_scale(self):

        assgmnt1 = latest_periodical.Assignment(image_scale='tile')

        r1 = self.renderer(context=self.portal, assignment=assgmnt1)
        self.assertTrue(r1.get_image_scale() == 'tile')

    def test_count(self):

        assgmnt1 = latest_periodical.Assignment()

        r1 = self.renderer(context=self.portal, assignment=assgmnt1)
        self.assertEqual(r1.data.count, 5)

        assgmnt1 = latest_periodical.Assignment(count=3)

        r1 = self.renderer(context=self.portal, assignment=assgmnt1)
        self.assertEqual(r1.data.count, 3)
