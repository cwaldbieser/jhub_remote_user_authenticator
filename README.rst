====================================
Jupyterhub REMOTE_USER Authenticator
====================================

Authenticate to Jupyterhub using an authenticating proxy that can set
the REMOTE_USER header.

-----------------------------------------
Architecture and Security Recommendations
-----------------------------------------

This type of authentication relies on an HTTP header, and a malicious
client could spoof the REMOTE_USER header.  The recommended architecture for this
type of authentication requires that an authenticating proxy be placed in front
of your Jupyterhub.  Your Jupyerhub should **only** be accessible from the proxy
and **never** directly accessible by a client.  

This type of access is typically enforced with network access controls.  E.g. in
a simple case, the host on which the Jupyterhub service accepts incoming requests
has its host based firewall configured to only accept incoming connections from
the proxy host.

Further, the authenticating proxy should make sure it removes any REMOTE_USER
headers from incoming requests and only applies the header to proxied requests
that have been properly authenticated.

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

