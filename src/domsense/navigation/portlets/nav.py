import random

from zope.interface import implements
from zope.component import getMultiAdapter, getUtility

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from plone.i18n.normalizer.interfaces import IIDNormalizer

from domsense.navigation import _


class INavPortlet(IPortletDataProvider):
    """A portlet which renders the results of a folder object.
    """

    header = schema.TextLine(
            title=_(u"Portlet header"),
            description=_(u"Title of the rendered portlet. \
            If none the header won't be rendered at all"),
            required=True)

    show_header = schema.Bool(
                title=_(u"Show portlet header"),
                description=_(u""),
                default=True,
                required=False)

    target_folder = schema.Choice(
        title=_(u"Target folder"),
        description=_(u"Find the folder which provides the links to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': 'Link'},
            default_query='path:'
        )
    )

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Specify the maximum number of items to show in the "
                      u"portlet. Leave this blank to show all items."),
        required=False)


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(INavPortlet)

    header = u""
    target_folder = None
    limit = None
    show_header = True

    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('nav.pt')
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @property
    def available(self):
        return len(self.results())

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portletNav-%s" % normalizer.normalize(header)

    @memoize
    def results(self):
        return self._results()

    def _results(self):
        results = []
        folder = self.folder()
        if folder is not None:
            limit = self.data.limit or -1
            results = folder.objectValues()[:limit]
        return results

    @memoize
    def folder(self):
        folder_path = self.data.target_folder
        if not folder_path:
            return None

        if folder_path.startswith('/'):
            folder_path = folder_path[1:]

        if not folder_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(folder_path, unicode):
            # restrictedTraverse accepts only strings
            folder_path = str(folder_path)
        return portal.restrictedTraverse(folder_path, default=None)

    def folder_url(self):
        folder = self.folder()
        if folder is None:
            return None
        else:
            return folder.absolute_url()


class AddForm(base.AddForm):

    form_fields = form.Fields(INavPortlet)
    form_fields['target_folder'].custom_widget = UberSelectionWidget

    label = _(u"Add Nav Portlet")
    description = _(u"This portlet display a listing of links from a "
                    u"folder.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(INavPortlet)
    form_fields['target_folder'].custom_widget = UberSelectionWidget

    label = _(u"Edit Nav Portlet")
    description = _(u"This portlet display a listing of links from a "
                    u"folder.")
