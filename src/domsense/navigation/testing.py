from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class DomsenseNavigation(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import domsense.navigation
        xmlconfig.file('configure.zcml',
                       domsense.navigation,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'domsense.navigation:default')

DOMSENSE_NAVIGATION_FIXTURE = DomsenseNavigation()
DOMSENSE_NAVIGATION_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(DOMSENSE_NAVIGATION_FIXTURE, ),
                       name="DomsenseNavigation:Integration")