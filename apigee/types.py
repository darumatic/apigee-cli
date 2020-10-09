APIS = {
    'apis',
    'keyvaluemaps',
    'targetservers',
    'caches',
    'developers',
    'apiproducts',
    'apps',
    'userroles',
}


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def empty_snapshot():
    return Struct(
        apis={},
        keyvaluemaps={},
        targetservers={},
        caches={},
        developers=[],
        apps={},
        apiproducts=[],
        userroles=[],
    )
