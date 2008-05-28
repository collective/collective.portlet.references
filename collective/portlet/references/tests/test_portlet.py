from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.references import referencesportlet

from collective.portlet.references.tests.base import TestCase


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.references.ReferencesPortlet')
        self.assertEquals(portlet.addview,
                          'collective.portlet.references.ReferencesPortlet')

    def test_interfaces(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        portlet = referencesportlet.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.references.ReferencesPortlet')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add
        # form.
        # Note: if the portlet has a NullAddForm, simply call
        # addview() instead of the next line.
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   referencesportlet.Assignment))

    def test_invoke_edit_view(self):
        # NOTE: This test can be removed if the portlet has no edit form
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = referencesportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, referencesportlet.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        # TODO: Pass any keyword arguments to the Assignment constructor
        assignment = referencesportlet.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, referencesportlet.Renderer))


class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        # TODO: Pass any default keyword arguments to the Assignment
        # constructor.
        assignment = assignment or referencesportlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render_related_items(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        r = self.renderer(context=self.folder,
                          assignment=referencesportlet.Assignment())
        r = r.__of__(self.folder)
        r.update()
        output = r.render()

        # By default this folder has no references, so this portlet is
        # not displayed.
        self.failIf(r.available,
                    "No references, so the portlet should not be available.")

        # So we add a related item to this folder.  Note that this
        # field is normally not visible in the edit for.
        front = self.portal['front-page']
        self.folder.setRelatedItems([front])
        r.update()
        self.failUnless(
            r.available,
            "We have a related item, so the portlet should be available.")

    def test_render_references(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        front = self.portal['front-page']
        front_path = '/'.join(self.folder.getPhysicalPath())
        text_template = u'<a class="link-internal" href="%s">A link.</a>'
        self.folder.invokeFactory('Document', 'page')
        page = self.folder.page

        # Note: during processForm the references get added.
        page.processForm(values={'text': text_template % front_path})

        r = self.renderer(context=page,
                          assignment=referencesportlet.Assignment())
        r = r.__of__(page)
        r.update()
        output = r.render()

        self.assertEqual(len(page.getRefs()), 1)
        self.failUnless(
            r.available,
            "We have a reference, so the portlet should be available.")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
