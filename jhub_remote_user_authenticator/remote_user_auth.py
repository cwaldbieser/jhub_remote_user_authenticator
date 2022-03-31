import os
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode


class RemoteUserLoginHandler(BaseHandler):

    def get(self):
        remote_user = self.request.headers.get("Cn", "").lower()
        remote_roles = self.request.headers.get("isMemberOf", "")
        if remote_user == "":
            raise web.HTTPError(401)
        else:
            user = self.user_from_username(remote_user)
            home_dir_exists = os.path.exists(os.path.expanduser('~{}'.format(remote_user)))

            if remote_user == "saz31":
                self.redirect("https://crc.pitt.edu/node/1041")
            
            if (not home_dir_exists) and remote_roles == "SAM-SSLVPNSAMUsers":
                self.redirect("https://crc.pitt.edu/node/1042")
            elif remote_roles == "SAM-SSLVPNSAMUsers":
                self.set_login_cookie(user)
                self.redirect(url_path_join(self.hub.server.base_url, 'home'))
            else:
                self.redirect("https://crc.pitt.edu/node/1041")


class RemoteUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    """
    header_name = Unicode(
        default_value='REMOTE_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
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

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
