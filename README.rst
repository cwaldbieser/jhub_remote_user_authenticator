====================================
Jupyterhub REMOTE_USER Authenticator
====================================

Authenticate to Jupyterhub using an authenticating proxy that can set
the REMOTE_USER header.

------------
Installation
------------

This package can be installed with `pip` either from a local git repository or from PyPi.

Installation from local git repository::

    cd jhub_remote_user_authenticator
    pip install .

Installation from PyPi::

    pip install jhub_remote_user_authenticator

Alternately, you can add the local project folder must be on your PYTHONPATH.

-------------
Configuration
-------------

You should edit your :file:`jupyterhub_config.py` to set the authenticator 
class::

    c.JupyterHub.authenticator_class = 'jhub_remote_user_authenticator.remote_user_auth.RemoteUserAuthenticator'

You should be able to start jupyterhub.  The "/hub/login" resource
will look for the authenticated user name in the HTTP header "REMOTE_USER" [#f1]_.
If found, and not blank, you will be logged in as that user.

Alternatively, you can use `RemoteUserLocalAuthenticator`::

    c.JupyterHub.authenticator_class = 'jhub_remote_user_authenticator.remote_user_auth.RemoteUserLocalAuthenticator'

This provides the same authentication functionality but is derived from
`LocalAuthenticator` and therefore provides features such as the ability
to add local accounts through the admin interface if configured to do so.

.. [#f1] The HTTP header name is configurable.  Note that NGINX, a popular
   proxy, drops headers that contain an underscore by default. See
   http://nginx.org/en/docs/http/ngx_http_core_module.html#underscores_in_headers
   for details.

