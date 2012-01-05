PROJECTNAME = 'domsense.navigation'

from zope.i18nmessageid import MessageFactory
DmsNavMessageFactory = MessageFactory('domsense.navigation')
_ = DmsNavMessageFactory

from Products.CMFCore.permissions import setDefaultRoles


DEFAULT_ADD_CONTENT_PERMISSION = "%s: Add Nav portlet" % PROJECTNAME

setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION,
                ('Manager', 'Site Administrator', 'Owner',))

