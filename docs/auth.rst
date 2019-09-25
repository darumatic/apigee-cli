auth
====

The API modules read Apigee credentials from a single object that can be defined
as follows::

    class Struct:
        def __init__(self, **entries): self.__dict__.update(entries)
    auth = Struct(username='[username]', password='[password]', mfa_secret='[mfa_secret]')

or you can define it this way::

    auth = type('', (), dict(username='[username]', password='[password]', mfa_secret='[mfa_secret]'))()

The resulting ``auth`` object can then be passed to API methods like so::

    from apigee.api.apis import Apis

    apis = Apis(auth, '[org]', '[api_name]')

    print(apis.list_api_proxy_revisions('[api_name]').text)
