import json

from tabulate import tabulate


class DeploymentsSerializer:
    def serialize_details(self, deployment_details, format, showindex=False, tablefmt='plain'):
        if format == 'text':
            return deployment_details.text
        revisions = []
        for i in deployment_details.json()['environment']:
            revisions.append(
                {
                    'name': i['name'],
                    'revision': [j['name'] for j in i['revision']],
                    'state': [j['state'] for j in i['revision']],
                }
            )
        if format == 'json':
            return json.dumps(revisions)
        elif format == 'table':
            table = [[rev['name'], rev['revision'], rev['state']] for rev in revisions]
            headers = []
            if showindex == 'always' or showindex is True:
                headers = ['id', 'name', 'revision', 'state']
            elif showindex == 'never' or showindex is False:
                headers = ['name', 'revision', 'state']
            return tabulate(table, headers, showindex=showindex, tablefmt=tablefmt)
        else:
            raise ValueError(format)
        return deployment_details
