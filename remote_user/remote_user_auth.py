
import os
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode


class RemoteUserLoginHandler(BaseHandler):
    header_name = 'REMOTE_USER'

    def get(self):
        header_name = self.header_name
        remote_user = self.request.headers.get(header_name, "")
        if remote_user == "":
            raise web.HTTPError(401)
        else:
            user = self.user_from_username(remote_user)
            self.set_login_cookie(user)
            self.redirect(url_path_join(self.hub.server.base_url, 'home'))


class RemoteUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    """
    remote_user_header = Unicode(
        "REMOTE_USER",
        config=True,
        help="""HTTP header to inspect for the authenticated username."""
    )
   
    def get_handlers(self, app):
        return [
            (r'/remote_user_login', RemoteUserLoginHandler),
        ]
 
    @gen.coroutine
    def authenticate(self, *args):
        print("args: {0}".format(args))
        raise NotImplementedError()
