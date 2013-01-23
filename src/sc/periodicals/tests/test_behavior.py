# -*- coding: utf-8 -*-

from sc.periodicals.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.container.interfaces import INameChooser

from sc.periodicals.behavior import ATTEMPTS
import unittest2 as unittest
import transaction


class BehaviorTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def _test_100_or_more_unique_ids(self):
        # add the same item 110 times. the first 100 items should be numbered.
        # after that it should use datetime to generate the id

        import pdb;pdb.set_trace()
        edition=1
        # create the first object, which will have no suffix
        self.folder.invokeFactory("Periodical", id='1')
        transaction.commit()

        chooser = INameChooser(self.folder)

        for i in range(1, ATTEMPTS + 1):
            id = chooser.chooseName(edition, self.folder)
            if i <= ATTEMPTS: # first addition has no suffix
                self.assertEqual("1-%s"%i, id)
            else:
                self.assertNotEqual("1-%s"%i, id)

            self.folder.invokeFactory("Periodical", id, number_edition=edition)
            transaction.savepoint(optimistic=True)
            item = self.folder.get(id)

