====================================
Jupyterhub REMOTE_USER Authenticator
====================================

Authenticate to Jupyterhub using an authenticating proxy that can set
the REMOTE_USER header.

------------
Installation
------------

This project folder must be on your PYTHONPATH.
You should edit your :file:`jupyterhub_config.py` to set the authenticator 
class::

    c.JupyterHub.authenticator_class = 'remote_user.remote_user_auth.RemoteUserAuthenticator'

You should be able to start jupyterhub.  The "/remote_user_login" resource
will look for the authenticated user name in the HTTP header "REMOTE_USER".
If found, and not blank, you will be logged in as that user.

