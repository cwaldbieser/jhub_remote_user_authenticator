import re
import os
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode


class RemoteUserLoginHandler(BaseHandler):

    def get(self):
        header_name = self.authenticator.header_name
        # Some external login system use mail address format for REMOTE_USER. In case of
        # RemoteUserLocalAuthenticator, this cause a error as prefix@domain.com is not a valid
        # format for user. To avoid this, we rename @ to -at- for unix login
        p = re.compile('@')
        remote_user = p.sub('-at-', self.request.headers.get(header_name, ""))
        if remote_user == "":
            self.redirect(self.authenticator.login_page)
        else:
            user = self.user_from_username(remote_user)
            self.set_login_cookie(user)
            self.redirect(url_path_join(self.hub.server.base_url, 'home'))

class RemoteUserLogoutHandler(BaseHandler):
    """Log a user out by clearing their login cookie."""
    def get(self):
        user = self.get_current_user()
        if user is not None:
            self.log.warning("User logged out: %s", user.name)
            self.clear_login_cookie()
            self.statsd.incr('logout')
            self.redirect(self.authenticator.logout_page)

class RemoteUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    """
    header_name = Unicode(
        default_value='REMOTE_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")
    login_page = Unicode(
        default_value='/',
        config=True,
        help="""Location of login page"""
    )
    logout_page = Unicode(
        default_value='/logout',
        config=True,
        help="""Location of logout page"""
    )
    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
            (r'/logout', RemoteUserLogoutHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()


class RemoteUserLocalAuthenticator(LocalAuthenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    Derived from LocalAuthenticator for use of features such as adding
    local accounts through the admin interface.
    """
    header_name = Unicode(
        default_value='REMOTE_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")
    login_page = Unicode(
        default_value='/',
        config=True,
        help="""Location of login page"""
    )
    logout_page = Unicode(
        default_value='/logout',
        config=True,
        help="""Location of logout page"""
    )

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
            (r'/logout', RemoteUserLogoutHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
