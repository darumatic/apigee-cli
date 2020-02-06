==========
apigee-cli
==========

|Upload Python Package badge|

This package provides a command-line interface for the Apigee Management API with multi-factor authentication. ::

    usage: apigee [-h] [-V]
                  {authorization,auth,configure,apis,deployments,deps,keyvaluemaps,kvms,developers,devs,apps,products,prods,targetservers,ts,maskconfigs,masks,permissions,perms,userroles,roles,caches}
                  ...

    Apigee Management API command-line interface with multi-factor authentication

    positional arguments:
      {authorization,auth,configure,apis,deployments,deps,keyvaluemaps,kvms,developers,devs,apps,products,prods,targetservers,ts,maskconfigs,masks,permissions,perms,userroles,roles,caches}
        authorization (auth)
                            verify authorization
        configure           configure credentials
        apis                manage apis
        deployments (deps)  see apis that are actively deployed
        keyvaluemaps (kvms)
                            manage keyvaluemaps
        developers (devs)   manage developers
        apps                manage developer apps
        products (prods)    manage api products
        targetservers (ts)  manage target servers
        maskconfigs (masks)
                            manage data masks
        permissions (perms)
                            manage permissions for a role
        userroles (roles)   manage user roles
        caches              manage caches

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit


The apigee-cli package works on Python versions:

* 3.5.x and greater
* 3.6.x and greater
* 3.7.x and greater

Documentation: `The Apigee Management API command-line interface documentation`_

------------
Installation
------------

The easiest way to install apigee-cli is to use `pip`_ in a ``virtualenv``::

    $ pip install apigeecli

or, if you are not installing in a ``virtualenv``, to install globally::

    $ sudo pip install apigeecli

or for your user::

    $ pip install --user apigeecli

If you have the apigee-cli installed and want to upgrade to the latest version
you can run::

    $ pip install --upgrade apigeecli

------------
Getting Help
------------

* `The Apigee Management API command-line interface documentation`_
* `Apigee Product Documentation`_



.. |Upload Python Package badge| image:: https://github.com/mdelotavo/apigee-cli/workflows/Upload%20Python%20Package/badge.svg
    :target: https://github.com/mdelotavo/apigee-cli/actions?query=workflow%3A%22Upload+Python+Package%22
.. _`Apigee Product Documentation`: https://apidocs.apigee.com/management/apis
.. _`Permissions reference`: https://docs.apigee.com/api-platform/system-administration/permissions
.. _`Add permissions to testing role`: https://docs.apigee.com/api-platform/system-administration/managing-roles-api#addpermissionstotestingrole
.. _pip: http://www.pip-installer.org/en/latest/
.. _`Universal Command Line Interface for Amazon Web Services`: https://github.com/aws/aws-cli
.. _`The Apigee Management API command-line interface documentation`: https://mdelotavo.github.io/apigee-cli/index.html
