==========
apigee-cli
==========

This package provides a command-line interface for the Apigee Management API with easy-to-use OAuth2 authentication. ::

    usage: apigee [-h] [-V]
                  {test,get-access-token,configure,apis,deployments,deps,kvms,keyvaluemaps,developers,devs,apps,products,prods,ts,targetservers,mask,maskconfigs,perms,permissions,prepend,prefix}
                  ...

    Apigee Management API command-line interface with easy-to-use OAuth2
    authentication

    positional arguments:
      {test,get-access-token,configure,apis,deployments,deps,kvms,keyvaluemaps,developers,devs,apps,products,prods,ts,targetservers,mask,maskconfigs,perms,permissions,prepend,prefix}
        test (get-access-token)
                            test get access token
        configure           configure credentials
        apis                apis
        deployments (deps)  see apis that are actively deployed
        kvms (keyvaluemaps)
                            keyvaluemaps
        developers (devs)   developers
        apps                developer apps
        products (prods)    api products
        ts (targetservers)  target servers
        mask (maskconfigs)  data masks
        perms (permissions)
                            manage permissions for a role
        prepend (prefix)    prepend all matching strings with a prefix in all
                            files in the specified directory (rudimentary stream
                            editor). this is potentially VERY DANGEROUS. make sure
                            you have version control such as Git to revert any
                            changes in the target directory.

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit


The apigee-cli package works on Python versions:

* 3.5.x and greater
* 3.6.x and greater
* 3.7.x and greater


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
    Apigee username (email) [None]: my_email
    Apigee password [None]: my_pass
    Apigee MFA key (recommended) [None]: my_key
    Default Apigee organization (recommended) [None]: my_org
    Default team/resource prefix (recommended) [None]: apt


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


---------------------------------
Getting an OAuth 2.0 Access Token
---------------------------------

To get an OAuth 2.0 access token, configure an MFA key, then run::

    $ apigee test

This will return ``None`` if an MFA key is not set.

-------------------
Listing API Proxies
-------------------

To list all APIs in an organization, run::

    $ apigee apis list

To only list APIs that start with a prefix, run::

    $ apigee apis list --prefix apt

This will list all APIs within an organization that start with ``apt``. To change
the organization, specify ``-o/--organization``.

----------------------
Deploying an API Proxy
----------------------

To seamless deploy an API Proxy, run::

    $ apigee apis deploy --seamless-deploy -d [path] -n [name] -e [env]

----------------------
Exporting an API Proxy
----------------------

To export an API Proxy revision, run::

    $ apigee apis export -n [name] -r [revision]

This will export to ``[name].zip``.

To export to specific file, run::

    $ apigee apis export -n [name] -r 2 -O [new_name].zip

This will export to ``[new_name].zip``.

------------------------------------------------------
Getting API proxy revisions that are actively deployed
------------------------------------------------------

To get actively deployed revisions for an API Proxy, run::

    $ apigee deps get -r -n [name]

This will output a table like so::

       name revision
    0   dev   [3, 5]
    1  test      [3]

To output as JSON, specify the ``-j/--json`` argument::

    $ apigee deps get -r -n [name] -j

This will output the table like so::

    [{"name": "dev", "revision": ["3", "5"]}, {"name": "test", "revision": ["3"]}]

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

    Updating existing entries in test-kvm                                                              |
    100% |#############################################################################################|
    Updating deleted entries in test-kvm                                                               |
    100% |#############################################################################################|

As you can see, this command will update existing entries and delete those that are not present in the request body.
If the key value map or entry does not exist, a new one will be created.

------------------------------
Getting permissions for a role
------------------------------

To get permissions for a role, run::

    $ apigee perms get -n testing --max-colwidth 80

This will output a table like so::

        organization                                                         path         permissions
    0          myorg                                                            /               [get]
    1          myorg                                                           /*                  []
    2          myorg                                                  /developers               [get]
    3          myorg                                                 /apiproducts               [get]
    4          myorg                                                /applications               [get]
    5          myorg                                            /apiproducts/apt*  [get, delete, put]
    6          myorg                                           /applications/apt*  [get, delete, put]
    7          myorg                                           /developers/*/apps               [get]
    8          myorg                                       /environments/*/caches               [get]
    9          myorg                                    /apiproxies/*/maskconfigs               [get]
    10         myorg                                      /developers/*/apps/apt*  [get, delete, put]
    11         myorg                                 /apiproxies/apt*/maskconfigs  [get, delete, put]
    12         myorg                                 /environments/*/keyvaluemaps               [get]
    13         myorg                                  /environments/*/caches/apt*  [get, delete, put]
    14         myorg                                /environments/*/targetservers               [get]
    15         myorg                            /environments/*/keyvaluemaps/apt*  [get, delete, put]
    16         myorg  /environments/*/applications/apt*/revisions/*/debugsessions  [get, delete, put]

To output as JSON, specify the ``-j/--json`` argument.

------------------------------
Setting permissions for a role
------------------------------

To set permissions for a role, run::

    $ apigee perms create -n [role] -b [request_body]

To see how the ``[request_body]`` is constructed, see:

* `Permissions reference`_
* `Add permissions to testing role`_

There is also the ``apigee perms team`` command, which sets default permissions for a team role based on a template::

    $ apigee permissions team -n [role] --team apt

This will set the following permissions::

        organization                                                         path         permissions
    0          myorg                                                            /               [get]
    1          myorg                                                           /*                  []
    2          myorg                                                  /developers               [get]
    3          myorg                                                 /apiproducts               [get]
    4          myorg                                                /applications               [get]
    5          myorg                                            /apiproducts/apt*  [get, delete, put]
    6          myorg                                           /applications/apt*  [get, delete, put]
    7          myorg                                           /developers/*/apps               [get]
    8          myorg                                       /environments/*/caches               [get]
    9          myorg                                    /apiproxies/*/maskconfigs               [get]
    10         myorg                                      /developers/*/apps/apt*  [get, delete, put]
    11         myorg                                 /apiproxies/apt*/maskconfigs  [get, delete, put]
    12         myorg                                 /environments/*/keyvaluemaps               [get]
    13         myorg                                  /environments/*/caches/apt*  [get, delete, put]
    14         myorg                                /environments/*/targetservers               [get]
    15         myorg                            /environments/*/keyvaluemaps/apt*  [get, delete, put]
    16         myorg  /environments/*/applications/apt*/revisions/*/debugsessions  [get, delete, put]

The important thing to note here is that some resources start with ``apt*``. This means that
users with the role ``[role]`` will only be able to access those resources which start with ``apt``.
This is useful for the use case where many teams are working together on the same platform.


------------
Getting Help
------------

* `Apigee Product Documentation`_
* `Permissions reference`_
* `Add permissions to testing role`_
* This ``README`` is based on the `Universal Command Line Interface for Amazon Web Services`_ ``README``



.. _`Apigee Product Documentation`: https://apidocs.apigee.com/management/apis
.. _`Permissions reference`: https://docs.apigee.com/api-platform/system-administration/permissions
.. _`Add permissions to testing role`: https://docs.apigee.com/api-platform/system-administration/managing-roles-api#addpermissionstotestingrole
.. _pip: http://www.pip-installer.org/en/latest/
.. _`Universal Command Line Interface for Amazon Web Services`: https://github.com/aws/aws-cli
