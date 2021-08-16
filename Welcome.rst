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

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When to use this over the official tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Apigee Corporation maintains their own fully-featured CLI for the Apigee Management API (`apigeetool-node`_)
that can be used as an SDK to orchestrate tasks and may be more than suitable for your needs.

Our Apigee CLI provides a simpler command-line experience with CI/CD and SSO features in mind.

We built and use the Apigee CLI to implement and distribute features that allow our clients
to manage CI/CD, perform self-service operations and promote our DevOps workflows
in ways that are not supported by official tools.

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
