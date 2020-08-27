==========
apigee-cli
==========

|License|

Welcome to the Apigee Management API command-line interface!

This is not an officially supported Google product, and is not affiliated with Apigee or Google in any way.

This is a user-friendly command-line interface to the Apigee Management API providing
features that automate steps that are too cumbersome to perform manually or are non-existent
in existing tools such as multi-factor authentication (MFA) and single sign-on (SSO)/SAML.

This tool was made with certain clients in mind, and is intended for general administrative
use from your shell, as a package for developers, and to support automation for common development tasks,
such as test automation or Continuous Integration/Continuous Deployment (CI/CD).

.. code-block:: text

    Usage: apigee [OPTIONS] COMMAND [ARGS]...

      Welcome to the Apigee Management API command-line interface!

      Docs:    https://mdelotavo.github.io/apigee-cli/
      PyPI:    https://pypi.org/project/apigeecli/
      GitHub:  https://github.com/mdelotavo/apigee-cli

    Options:
      -V, --version  Show the version and exit.
      -h, --help     Show this message and exit.

    Commands:
      apiproducts    API products enable you to bundle and distribute your APIs...
      apis           The proxy APIs let you perform operations on API proxies,...
      apps           Management APIs available for working with developer apps.
      auth           Custom authorization commands.
      backups        Download configuration files from Apigee that can later be...
      caches         A lightweight persistence store that can be used by...
      configure      Configure Apigee Edge credentials.
      deployments    API proxies that are actively deployed in environments on...
      developers     Developers implement client/consumer apps and must be...
      keyvaluemaps   Key/value maps at the environment scope can be accessed by...
      maskconfigs    Specify data that will be filtered out of trace sessions.
      permissions    Permissions for roles in an organization on Apigee Edge.
      sharedflows    You can use the following APIs to manage shared flows and...
      targetservers  TargetServers are used to decouple TargetEndpoint...
      userroles      Roles for users in an organization on Apigee Edge.


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

---------------
Getting Started
---------------

Before using apigee-cli, you need to tell it about your Apigee Edge credentials.  You
can do this in three ways:

* Environment variables
* Config file
* Command-line arguments

The quickest way to get started is to run the ``apigee configure`` command::

    $ apigee configure
    Apigee username (email) []: my_email
    Apigee password []: my_pass
    Apigee MFA key (optional) []: my_key
    Identity zone name (to support SAML authentication) []:
    Use OAuth, no MFA (optional)? [y/N]: n
    Default Apigee organization (recommended) []: my_org
    Default team/resource prefix (optional) []:

You can also do the same thing using command-line arguments::

    $ apigee configure -P default -u <my_email> -p <my_pass> -o <my_org> -mfa '' -z '' --no-token --prefix ''

You may need to specify empty strings as above. Also note the ``--prefix`` option. This option
will filter the output of some commands, such as the ``list`` type commands, by the prefix which may be useful to some people,
but if you want to avoid confusion just keep this value empty. You can also explicitly specify the ``--prefix``
for those commands if you need it on the fly.


To use environment variables, do the following::

    $ export APIGEE_USERNAME=<my_email>
    $ export APIGEE_PASSWORD=<my_pass>
    $ export APIGEE_MFA_SECRET=<my_key>
    $ export APIGEE_ZONENAME=<my_zonename>
    $ export APIGEE_IS_TOKEN=<bool>
    $ export APIGEE_ORG=<my_org>
    $ export APIGEE_CLI_PREFIX=<my_prefix>


To use the configuration file, create an INI formatted file like this::

    [default]
    username = my_email
    org = my_org
    mfa_secret = my_key
    prefix = my_prefix
    password = my_pass

    [produser]
    org = my_org
    username = my_email
    password = my_pass
    mfa_secret = my_key

and place it in ``~/.apigee/credentials``.

As you can see, you can have multiple ``profiles`` defined in the configuration file. You can then specify which
profile to use by using the ``-P/--profile`` option. If no profile is specified
the ``default`` profile is used.

^^^^^^^^^^^^^^^^^^^^^^^^^
Using SAML authentication
^^^^^^^^^^^^^^^^^^^^^^^^^
If you specified an ``Identity zone name (to support SAML authentication)`` during setup,
the CLI will automatically use SAML authentication.
If you are not currently signed in by your identity provider, you will be prompted to sign in::

    $ apigee apis list
    SSO authorization page has automatically been opened in your default browser.
    Follow the instructions in the browser to complete this authorization request.

    If your browser did not automatically open, go to the following URL and sign in:

    https://{zoneName}.login.apigee.com/passcode

    then copy the Temporary Authentication Code.

    Please enter the Temporary Authentication Code:

``zoneName`` will be the ``Identity zone name`` you previously configured.

Refer to the official Apigee documentation to learn more about how to `Access the Edge API with SAML`_.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using SAML with automated tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The CLI also supports machine users as described in `Using SAML with automated tasks`_ when SAML is enabled
to support automation for common development tasks, such as test automation or Continuous Integration/Continuous Deployment (CI/CD).

To tell the CLI that the current user ``--profile`` is a machine user and thus to not redirect you to an identity provider,
you can set the following environment variable like so::

    $ export APIGEE_CLI_IS_MACHINE_USER=true

To continue using an ordinary user, you will need to unset this variable or set it to ``false``.

Refer to the official Apigee documentation to learn more about identity zones: `SAML Overview`_.

^^^^^^^^^^^^^^^^^^^^^^
Tabulating deployments
^^^^^^^^^^^^^^^^^^^^^^
Deployments information can be too verbose but you may just want to see a quick summary of which revisions of an API proxy are deployed and their status.

To tabulate the deployments response, use the ``-r/--revision-name-only`` flag in the following command::

    $ apigee deployments get -n <API_NAME> -r

This will output a table like so::

    name     revision    state
    prod     ['1']       ['deployed']
    test     ['1']       ['deployed']

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Tabulating resource permissions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Resource permissions responses can be slightly difficult to read so the CLI outputs this information as a table by default::

    $ apigee permissions get -n <ROLE_NAME>
    organization      path             permissions
    my_org            /                ['delete', 'get', 'put']
    my_org            /environments    ['get']
    my_org            /environments/*  ['get']
    my_org            /apimonitoring   ['delete', 'get', 'put']

If you need the JSON response, use the ``--format json`` option::

    $ apigee permissions get -n <ROLE_NAME> --format json
    {
      "resourcePermission" : [ {
        "organization" : "my_org",
        "path" : "/",
        "permissions" : [ "put", "get", "delete" ]
      }, {
        "organization" : "my_org",
        "path" : "/environments",
        "permissions" : [ "get" ]
      }, {
        "organization" : "my_org",
        "path" : "/environments/*",
        "permissions" : [ "get" ]
      }, {
        "organization" : "my_org",
        "path" : "/apimonitoring",
        "permissions" : [ "put", "get", "delete" ]
      } ]
    }

^^^^^^^^^^^^^^^^^^^^^^^^
Deploy API Proxy bundles
^^^^^^^^^^^^^^^^^^^^^^^^
You can also deploy API proxy bundles to Apigee.

This command is an enhanced version of the Apigee API Proxy Deploy Tool.

It supports a bunch of useful features such as MFA, SAML, seamless deployments and automatic handling of ``missing`` and broken deployments.

.. code-block:: text

    Usage: apigee apis deploy [OPTIONS]

      Deploy APIs using an improved version of the Apigee API Proxy Deploy Tool:
      https://github.com/apigee/api-platform-samples/tree/master/tools

         =========================================================================
         ==  NOTICE file corresponding to the section 4 d of                    ==
         ==  the Apache License, Version 2.0,                                   ==
         ==  in this case for the Apigee API Proxy Deploy Tool code.            ==
         =========================================================================

      Apigee API Proxy Deploy Tool https://github.com/apigee/api-platform-
      samples/tree/master/tools These files are Copyright 2015 Apigee
      Corporation, released under the Apache2 License.

    Options:
      -P, --profile TEXT              name of the user profile to authenticate
                                      with  [default: default]

      -o, --org TEXT                  [default: (current org)]
      -z, --zonename TEXT             [default: (current identity zone name)]
      --token / --no-token            specify to use oauth without MFA  [default:
                                      False]

      -mfa, --mfa-secret TEXT
      -p, --password TEXT             [default: (current password)]
      -u, --username TEXT             [default: (current username)]
      -v, --verbose                   [default: (toggle verbose output)]
      --silent                        [default: (toggle silent output)]
      -e, --environment TEXT          environment  [required]
      -n, --name TEXT                 name  [required]
      -d, --directory DIRECTORY       directory with the apiproxy/ bundle
                                      [required]

      Deployment options: [mutually_exclusive]
                                      The deployment options
        -i, --import-only / -I, --no-import-only
                                      import only and not deploy
        -s, --seamless-deploy / -S, --no-seamless-deploy
                                      seamless deploy the bundle
      -h, --help                      Show this message and exit.

If deploying via CI/CD you may end up with a lot of undeployed revisions. In this case, you can
make use of the ``apigee apis clean`` command to delete all those undeployed revisions and even specify to always keep the last few revisions.

^^^^^^^^^^^^^
Push commands
^^^^^^^^^^^^^
Some commands support the ``push`` subcommand which combines CRUD API calls to manage the creation, update and sometimes deletion of resources using a single command.

The following commands support the ``push`` subcommand:

- ``apiproducts``
- ``caches``
- ``keyvaluemaps``
- ``targetservers``
- ``maskconfigs``

Push commands read JSON from a file and can be invoked like so::

    $ apigee keyvaluemaps push -e <env> -f <file_path.json>

This will create the KVM if it does not exist, and update it if it does.

---------------
Troubleshooting
---------------
If you get an error like so::

    An exception of type jwt.api_jws.DecodeError occurred. Arguments:
    Invalid crypto padding

Try deleting the cached access token::

    $ rm ~/.apigee/access_token

------------
Getting Help
------------

* `The Apigee Management API command-line interface documentation`_
* `Apigee Product Documentation`_
* `GitHub`_

----------
Disclaimer
----------
This is not an officially supported Google product.


.. |Upload Python Package badge| image:: https://github.com/mdelotavo/apigee-cli/workflows/Upload%20Python%20Package/badge.svg
    :target: https://github.com/mdelotavo/apigee-cli/actions?query=workflow%3A%22Upload+Python+Package%22
.. |Python package badge| image:: https://github.com/mdelotavo/apigee-cli/workflows/Python%20package/badge.svg
    :target: https://github.com/mdelotavo/apigee-cli/actions?query=workflow%3A%22Python+package%22
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
.. |PyPI| image:: https://img.shields.io/pypi/v/apigeecli
    :target: https://pypi.org/project/apigeecli/
.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
.. _`Apigee Product Documentation`: https://apidocs.apigee.com/management/apis
.. _`Permissions reference`: https://docs.apigee.com/api-platform/system-administration/permissions
.. _`Add permissions to testing role`: https://docs.apigee.com/api-platform/system-administration/managing-roles-api#addpermissionstotestingrole
.. _pip: http://www.pip-installer.org/en/latest/
.. _`Universal Command Line Interface for Amazon Web Services`: https://github.com/aws/aws-cli
.. _`The Apigee Management API command-line interface documentation`: https://mdelotavo.github.io/apigee-cli/index.html
.. _`GitHub`: https://github.com/mdelotavo/apigee-cli
.. _`Python Package Index (PyPI)`: https://pypi.org/project/apigeecli/
.. _`Access the Edge API with SAML`: https://docs.apigee.com/api-platform/system-administration/using-saml
.. _`SAML Overview`: https://docs.apigee.com/api-platform/system-administration/saml-overview
.. _`Using SAML with automated tasks`: https://docs.apigee.com/private-cloud/v4.17.09/using-saml-automated-tasks
