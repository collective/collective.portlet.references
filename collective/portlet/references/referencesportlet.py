from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from collective.portlet.references import ReferencesPortletMessageFactory as _


class IReferencesPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IReferencesPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "References portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('referencesportlet.pt')

    @property
    def refs(self):
        context = aq_inner(self.context)
        try:
            refs = context.getRefs()
        except AttributeError:
            # For example a Plone Site has no references field.
            refs = []
        if len(refs) == 0:
            return refs
        wf_tool = getToolByName(context, 'portal_workflow')
        infos = []
        for ref in refs:
            visible_for_anonymous = False
            for perm in ref.permissionsOfRole('Anonymous'):
                if perm['name'] == 'View':
                    visible_for_anonymous = (perm['selected'] == 'SELECTED')
                    break

            review_state_id = wf_tool.getInfoFor(ref, 'review_state')
            review_state_title = wf_tool.getTitleForStateOnType(
                review_state_id, ref.portal_type)
            info = dict(
                title = ref.title_or_id(),
                url = ref.absolute_url(),
                state_id = review_state_id,
                state_title = review_state_title,
                visible_for_anonymous = visible_for_anonymous,
                )
            infos.append(info)
        return infos

    @property
    def available(self):
        # XXX not for anonymous
        return len(self.refs) > 0


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.

    NOTE: If this portlet does not have any configurable parameters, you can
    inherit from NullAddForm and remove the form_fields variable.
    """
    form_fields = form.Fields(IReferencesPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.

    NOTE: IF this portlet does not have any configurable parameters, you can
    remove this class definition and delete the editview attribute from the
    <plone:portlet /> registration in configure.zcml
    """
    form_fields = form.Fields(IReferencesPortlet)
