==========
apigee-cli
==========

|License|

Welcome to the (Unofficial) Apigee Management API command-line interface!

.. code-block:: text

    Usage: apigee [OPTIONS] COMMAND [ARGS]...

      Welcome to the (Unofficial) Apigee Management API command-line interface!

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
      keystores      A list of URIs used to create, modify, and delete
                     keystores...

      keyvaluemaps   Key/value maps at the environment scope can be accessed by...
      maskconfigs    Specify data that will be filtered out of trace sessions.
      permissions    Permissions for roles in an organization on Apigee Edge.
      plugins        [Experimental] Simple plugins manager for distributing...
      references     References in an organization and environment.
      sharedflows    You can use the following APIs to manage shared flows and...
      targetservers  TargetServers are used to decouple TargetEndpoint...
      userroles      Roles for users in an organization on Apigee Edge.
      virtualhosts   A named network configuration (including URL) for an...


This is not an officially supported Google product, and is not affiliated with Apigee or Google in any way.

Please note that this CLI is still highly experimental and may change significantly
based on client needs.

.. contents:: :local:

--------------------
Why does this exist?
--------------------

Apigee CLI is a user-friendly command-line interface to the Apigee Edge Management API providing
automation capabilities with multi-factor authentication (MFA) and single sign-on (SSO)/SAML support.
It is intended for general administrative use from your shell, as a package for developers,
and to support automation for common development tasks, such as test automation
or Continuous Integration/Continuous Deployment (CI/CD).

^^^^^^^^^^^^^^^^^^^
Third-party plugins
^^^^^^^^^^^^^^^^^^^

The Apigee CLI also supports the ability to load third-party plugins (to be documented)
as additional commands which enables us (and third-party developers) to distribute their own commands
for very specific use cases, including those do not require any interaction with the Apigee Management API,
while being able to leverage the command-line interface without any knowledge of the CLI internals.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
How we and our clients use it
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We built and use the Apigee CLI to implement and distribute features that allow our clients
to manage CI/CD, perform self-service operations and promote our DevOps workflows
in ways that are not supported by official tools.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When to use this over the official tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Apigee Corporation has their own CLI for the Apigee Management API (`apigeetool-node`_).

It is fully-featured, well-supported and can be used as an SDK to orchestrate tasks
and may be more than suitable for your needs.

If however, you have certain use cases that cannot be satisfied by this tool,
then the Apigee CLI may have what you need.

--------
Examples
--------

^^^^^^^^^^^^^^^^^^^^^^^^
Deploy API Proxy bundles
^^^^^^^^^^^^^^^^^^^^^^^^
You can also deploy API proxy bundles to Apigee.

This command is an enhanced version of the Apigee API Proxy Deploy Tool.

It supports a bunch of useful features such as MFA, SAML, seamless deployments and automatic handling of ``missing`` and broken deployments.

.. code-block:: text

    $ apigee apis deploy -n API_NAME -e ENVIRONMENT -d DIRECTORY_WITH_APIPROXY

Some notable options::

    Deployment options: [mutually_exclusive]
                                    The deployment options
      -i, --import-only / -I, --no-import-only
                                    import only and not deploy
      -s, --seamless-deploy / -S, --no-seamless-deploy
                                    seamless deploy the bundle

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Cleaning up undeployed revisions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If deploying via CI/CD you may end up with a lot of undeployed revisions. In this case, you can
make use of the ``clean`` command to delete all undeployed revisions.

.. code-block:: text

    $ apigee apis clean -n API_NAME

You can also specify to keep the last few revisions::

    $ apigee apis clean -n API_NAME --save-last INTEGER

To only show which revisions will be deleted but not actually delete anything, use the following option::

      --dry-run / --no-dry-run  show revisions to be deleted but do not delete

^^^^^^^^^^^^^
Push commands
^^^^^^^^^^^^^
Some commands support the ``push`` subcommand which combines API calls to manage the creation, update and sometimes deletion of resources using a single command.

Push commands read JSON from a file and can be invoked like so::

    $ apigee keyvaluemaps push -e ENVIRONMENT -f FILENAME

This will create the KVM if it does not exist, and update it if it does.

----------------
Managing plugins
----------------
The simple plugins manager uses Git to install commands from remote sources, thus you will need to have Git installed for installation to work.
However, it is possible to install plugins manually by storing plugins in the correct location (to be documented).

Currently, only the commands below are supported. More commands will be added to improve automation and user experience.

The steps below show how to install commands from a public plugins repository located here:

* https://github.com/mdelotavo/apigee-cli-plugins

^^^^^^^^^^^
Configuring
^^^^^^^^^^^

To configure remote sources for installing plugins, run::

    apigee plugins configure -a

This will open a text editor so that you can specify the remote sources.

If you don't want changes to be automatically applied, then you can drop the ``-a`` option.

When the editor opens, copy and paste the following example configuration::

    [sources]
    public = https://github.com/mdelotavo/apigee-cli-plugins.git

After saving the changes, the CLI will attempt to install the plugins from the specified Git URI.
Here we use the HTTPS URI but you can also use SSH if you have configured it.

You can also specify multiple sources, as long as the key (``public`` in this case) is unique.
The key will be the name of the repository on your local machine under ``~/.apigee/plugins/``.

If installation is successful, you should now see additional commands when you run ``apigee -h``

^^^^^^^^
Updating
^^^^^^^^

If you specified the ``-a`` option when running ``apigee plugins configure`` then install will occur automatically.
Otherwise you can run::

     apigee plugins update

This will install and update plugins.

^^^^^^^
Pruning
^^^^^^^

If you specified the ``-a`` option when running ``apigee plugins configure`` then the removal of plugins will occur automatically.
Otherwise you can run::

     apigee plugins prune

^^^^^^^
Showing
^^^^^^^

To show the plugins you have configured, run::

     apigee plugins show

You can also run the following commands if you specify the plugin name::

    apigee plugins show -n PLUGIN_NAME --show-commit-only
    apigee plugins show -n PLUGIN_NAME --show-dependencies-only

Some plugins will not load if dependencies are not installed. You can run the following command to install them.
In order for this to work, the plugin needs to have the ``Requires`` key in the JSON body of the ``apigee-cli.info`` file.
More details coming soon.::

    pip3 install $(apigee plugins show -n PLUGIN_NAME --show-dependencies-only)

^^^^^^^^^^^^
How it works
^^^^^^^^^^^^

1. The plugins manager ``apigee/plugins/commands.py`` will clone or pull remote repositories into ``~/.apigee/plugins/``.
2. The ``_load_all_modules_in_directory()`` function in ``apigee/__main__.py`` will attempt to import the functions as specified in the ``__init__.py`` file for each plugin repository found in ``~/.apigee/plugins/``.
3. If the functions found are of instance type ``(click.core.Command, click.core.Group)`` then the CLI will add it to the list of available commands.

Further details are to be documented, including how to write plugins and leverage some useful CLI libraries.

------------
Getting Help
------------

* `The Apigee Management API command-line interface documentation`_
* `Apigee Product Documentation`_
* `GitHub`_
* `Mirror`_

For further questions, feel free to contact us at hello@darumatic.com or contact matthew@darumatic.com.

----------
Disclaimer
----------
This is not an officially supported Google product.


.. _`apigeetool-node`: https://github.com/apigee/apigeetool-node

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

.. _`Commands cheatsheet`: https://github.com/mdelotavo/apigee-cli-docs
.. _`Using SAML with automated tasks`: https://github.com/mdelotavo/apigee-cli-docs
.. _`Tabulating deployments`: https://github.com/mdelotavo/apigee-cli-docs
.. _`Tabulating resource permissions`: https://github.com/mdelotavo/apigee-cli-docs
.. _`Troubleshooting`: https://github.com/mdelotavo/apigee-cli-docs
.. _`Mirror`: https://github.com/darumatic/apigee-cli

.. _`Apigee CI/CD Docker releases`: https://hub.docker.com/r/darumatic/apigee-cicd
