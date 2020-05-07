Quickstart
==========

.. _`Getting Started`:

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
    Apigee username (email) [None]: my_email
    Apigee password []: my_pass
    Apigee MFA key (optional) []: my_key
    Default Apigee organization (recommended) []: my_org
    Default team/resource prefix (optional) []: team_prefix


To use environment variables, do the following::

    $ export APIGEE_USERNAME=<my_email>
    $ export APIGEE_PASSWORD=<my_pass>
    $ export APIGEE_MFA_SECRET=<my_key>
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


.. _`Getting an OAuth Access Token`:

---------------------------------
Getting an OAuth Access Token
---------------------------------

To get an OAuth access token, configure an MFA key, then run::

    $ apigee auth access-token

This will return ``None`` if an MFA key is not set.

.. _`Getting Help`:

------------
Getting Help
------------

* `Apigee Product Documentation`_
* `Permissions reference`_
* `Add permissions to testing role`_



.. _`Apigee Product Documentation`: https://apidocs.apigee.com/management/apis
.. _`Permissions reference`: https://docs.apigee.com/api-platform/system-administration/permissions
.. _`Add permissions to testing role`: https://docs.apigee.com/api-platform/system-administration/managing-roles-api#addpermissionstotestingrole
.. _pip: http://www.pip-installer.org/en/latest/
