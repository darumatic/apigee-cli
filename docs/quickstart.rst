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
    Apigee password [None]: my_pass
    Apigee MFA key (recommended) [None]: my_key
    Default Apigee organization (recommended) [None]: my_org
    Default team/resource prefix (recommended) [None]: team_prefix


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


.. _`Getting an OAuth 2.0 Access Token`: #getting-an-oauth-20-access-token

---------------------------------
Getting an OAuth 2.0 Access Token
---------------------------------

To get an OAuth 2.0 access token, configure an MFA key, then run::

    $ apigee auth access-token

This will return ``None`` if an MFA key is not set.

.. _`Listing API Proxies`:

-------------------
Listing API Proxies
-------------------

To list all APIs in an organization, run::

    $ apigee apis list

To only list APIs that start with a prefix, run::

    $ apigee apis list --prefix [team_prefix]

This will list all APIs within an organization that start with ``[team_prefix]``. To change
the organization, specify ``-o/--organization``.

.. _`Deploying an API Proxy`:

----------------------
Deploying an API Proxy
----------------------

To seamless deploy an API Proxy, run::

    $ apigee apis deploy --seamless-deploy -d [path] -n [name] -e [env]

.. _`Exporting an API Proxy`:

----------------------
Exporting an API Proxy
----------------------

To export an API Proxy revision, run::

    $ apigee apis export -n [name] -r [revision]

This will export to ``[name].zip``.

To export to a specific file, run::

    $ apigee apis export -n [name] -r [revision] -O [new_name].zip

This will export to ``[new_name].zip``.

.. _`Pulling an API proxy and its dependencies`:

-----------------------------------------
Pulling an API Proxy and its dependencies
-----------------------------------------

To pull an API proxy revision and its dependencies into the current working directory, run::

    $ apigee apis pull -e [env] -n [name] -r [revision]

To specify a target directory, use the ``--work-tree``  option::

    $ apigee apis pull -e [env] -n [name] -r [revision] --work-tree [dir]

You can also add a prefix to the name of the API and its dependencies using the ``--prefix`` option::

    $ apigee apis pull -e [env] -n [name] -r [revision] --prefix [prefix]

If you get the following error::

    error: [path] already exists

then use the ``-f/--force`` flag::

    $ apigee apis pull -e [env] -n [name] -r [revision] --force

.. _`Getting API proxy revisions that are actively deployed`:

------------------------------------------------------
Getting API proxy revisions that are actively deployed
------------------------------------------------------

To get actively deployed revisions for an API Proxy, run::

    $ apigee deps get -r -n [name]

This will output a table like so::

    name    revision
    dev     ['32']

The table can be formatted by specifiying ``--tablefmt``::

    $ apigee deps get -r -n [name] --tablefmt fancy_grid --showindex

This will output a table like so::

    ╒══════╤════════╤════════════╕
    │   id │ name   │ revision   │
    ╞══════╪════════╪════════════╡
    │    0 │ dev    │ ['32']     │
    ╘══════╧════════╧════════════╛

Supported table formats are (default is ``plain``)::

    --tablefmt {plain,simple,github,grid,fancy_grid,pipe,orgtbl,jira,presto,psql,rst,mediawiki,moinmoin,youtrack,html,latex,latex_raw,latex_booktabs,textile}

See the ``tabulate`` package for more info.

To output as JSON, specify the ``-j/--json`` argument::

    $ apigee deps get -r -n [name] -j

This will output the table like so::

    [{"name": "dev", "revision": ["3", "5"]}, {"name": "test", "revision": ["3"]}]

.. _`Deleting all undeployed revisions of an API proxy`:

-------------------------------------------------
Deleting all undeployed revisions of an API proxy
-------------------------------------------------

To delete all undeployed revisions for an API Proxy, run::

    $ apigee apis clean -n [name]

To preserve the ``N`` most recent revisions, run::

    $ apigee apis clean -n [name] --save-last [N]

To see which revisions will be deleted but not delete anything, run::

    $ apigee apis clean -n [name] --dry-run

.. _`Managing Key value maps (KVMs)`:

------------------------------
Managing Key value maps (KVMs)
------------------------------

The following commands are supported::

    usage: apigee kvms [-h]
                       {create,create-keyvaluemap-in-an-environment,delete,delete-keyvaluemap-from-an-environment,delete-entry,delete-keyvaluemap-entry-in-an-environment,get,get-keyvaluemap-in-an-environment,get-value,get-a-keys-value-in-an-environment-scoped-keyvaluemap,list,list-keyvaluemaps-in-an-environment,update,update-keyvaluemap-in-an-environment,create-entry,create-an-entry-in-an-environment-scoped-kvm,update-entry,update-an-entry-in-an-environment-scoped-kvm,list-keys,list-keys-in-an-environment-scoped-keyvaluemap,push,push-keyvaluemap}
                       ...

    positional arguments:
      {create,create-keyvaluemap-in-an-environment,delete,delete-keyvaluemap-from-an-environment,delete-entry,delete-keyvaluemap-entry-in-an-environment,get,get-keyvaluemap-in-an-environment,get-value,get-a-keys-value-in-an-environment-scoped-keyvaluemap,list,list-keyvaluemaps-in-an-environment,update,update-keyvaluemap-in-an-environment,create-entry,create-an-entry-in-an-environment-scoped-kvm,update-entry,update-an-entry-in-an-environment-scoped-kvm,list-keys,list-keys-in-an-environment-scoped-keyvaluemap,push,push-keyvaluemap}
        create (create-keyvaluemap-in-an-environment)
                            Creates a key value map in an environment.
        delete (delete-keyvaluemap-from-an-environment)
                            Deletes a key/value map and all associated entries
                            from an environment.
        delete-entry (delete-keyvaluemap-entry-in-an-environment)
                            Deletes a specific key/value map entry in an
                            environment by name, along with associated entries.
        get (get-keyvaluemap-in-an-environment)
                            Gets a KeyValueMap (KVM) in an environment by name,
                            along with the keys and values.
        get-value (get-a-keys-value-in-an-environment-scoped-keyvaluemap)
                            Gets the value of a key in an environment-scoped
                            KeyValueMap (KVM).
        list (list-keyvaluemaps-in-an-environment)
                            Lists the name of all key/value maps in an environment
                            and optionally returns an expanded view of all
                            key/value maps for the environment.
        update (update-keyvaluemap-in-an-environment)
                            Note: This API is supported for Apigee Edge for
                            Private Cloud only. For Apigee Edge for Public Cloud
                            use Update an entry in an environment-scoped KVM.
                            Updates an existing KeyValueMap in an environment.
                            Does not override the existing map. Instead, this
                            method updates the entries if they exist or adds them
                            if not. It can take several minutes before the new
                            value is visible to runtime traffic.
        create-entry (create-an-entry-in-an-environment-scoped-kvm)
                            Note: This API is supported for Apigee Edge for the
                            Public Cloud only. Creates an entry in an existing
                            KeyValueMap scoped to an environment. A key (name)
                            cannot be larger than 2 KB. KVM names are case
                            sensitive.
        update-entry (update-an-entry-in-an-environment-scoped-kvm)
                            Note: This API is supported for Apigee Edge for the
                            Public Cloud only. Updates an entry in a KeyValueMap
                            scoped to an environment. A key cannot be larger than
                            2 KB. KVM names are case sensitive. Does not override
                            the existing map. It can take several minutes before
                            the new value is visible to runtime traffic.
        list-keys (list-keys-in-an-environment-scoped-keyvaluemap)
                            Note: This API is supported for Apigee Edge for the
                            Public Cloud only. Lists keys in a KeyValueMap scoped
                            to an environment. KVM names are case sensitive.
        push (push-keyvaluemap)
                            Push KeyValueMap to Apigee. This will create
                            KeyValueMap/entries if they do not exist, update
                            existing KeyValueMap/entries, and delete entries on
                            Apigee that are not present in the request body.

    optional arguments:
      -h, --help            show this help message and exit


^^^^^^^^
Examples
^^^^^^^^

For example, to create a key value map in an environment, create the request body::

    $ body='{
     "name" : "Map_name",
     "encrypted" : "true",
     "entry" : [
      {
       "name" : "Key1",
       "value" : "value_one"
      },
      {
       "name" : "Key2",
       "value" : "value_two"
      }
     ]
    }'

Then run::

    $ apigee kvms create -e [env] -b "$body"

To ``push`` a key value map in a file to Apigee Edge, run::

    $ apigee kvms push -e dev -f test_kvm.json

This will display a loading bar output like so::

    Updating entries in test-kvm
    100%|██████████████████████████████████████████████| 2/2 [00:00<00:00, 10143.42it/s]
    Deleting entries in test-kvm
    100%|█████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.70it/s]

As you can see, this command will update existing entries and delete those that are not present in the request body.
If the key value map or entry does not exist, a new one will be created.

The ``push`` subcommand is also available for ``targetservers``, ``caches``, ``products`` and ``maskconfigs``.


.. _`Getting permissions for a role`:

------------------------------
Getting permissions for a role
------------------------------

To get permissions for a role, run::

    $ apigee perms get -n [role] #--showindex --tablefmt fancy_grid

This will output a table like so::

    organization    path             permissions
    myorg           /                ['delete', 'get', 'put']
    myorg           /environments    ['get']
    myorg           /environments/*  ['get']
    myorg           /apimonitoring   ['delete', 'get', 'put']

To output as JSON, specify the ``-j/--json`` argument.

.. _`Setting permissions for a role`:

------------------------------
Setting permissions for a role
------------------------------

To set permissions for a role, run::

    $ apigee perms create -n [role] -b [request_body]

To see how the ``[request_body]`` is constructed, see:

* `Permissions reference`_
* `Add permissions to testing role`_

There is also the ``apigee perms template`` command, which sets permissions for a team role using a template file::

    $ apigee perms template -n [role] -f [template_file] --placeholder-key [placeholder_string] --placeholder-value [placeholder_value]

where ``[template_file]`` contains the ``resourcePermission`` and looks something like this::

    {
      "resourcePermission" : [ {
        "organization" : "myorg",
        "path" : "/",
        "permissions" : [ "get", "put", "delete" ]
      } ]
    }

If ``--placeholder-key`` is specified, then all instances of the placeholder string will be replaced with the ``--placeholder-value`` (default is an empty string).

.. _`Importing modules`:

-----------------
Importing modules
-----------------

To import and make API calls using the modules, do the following::

    from apigee.api.apis import Apis

    class ApigeeAuth:
        def __init__(self, username, password, mfa_secret):
            self.username = username
            self.password = password
            self.mfa_secret = mfa_secret

    auth = ApigeeAuth('[username]', '[password]', '[mfa_secret]')
    apis = Apis(auth, '[org]', '[api_name]')

    print(apis.list_api_proxy_revisions().text)

.. _`Restoring Developer Apps`:

------------------------
Restoring Developer Apps
------------------------

To restore a developer app, run::

    $ apigee apps restore -f [app_file]

This will create the app specified in the ``[app_file]`` and restore the credentials.

To get a developer app in the first place, run::

    $ apigee apps get -d [developer] -n [app_file]

.. _`Suppressing retry messages`:

--------------------------
Suppressing retry messages
--------------------------

To suppress the retry message and response from printing to the console, set the following environment variables::

    APIGEE_CLI_SUPPRESS_RETRY_MESSAGE=True
    APIGEE_CLI_SUPPRESS_RETRY_RESPONSE=True

This is useful if you want to reliably redirect JSON output to a file without retry messages showing up from time to time.

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
