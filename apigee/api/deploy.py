#!/usr/bin/env python

# Copyright 2019 Matthew Delotavo
# Copyright 2015 Apigee Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import base64
import getopt
import http.client
import json
import os
import re
import sys
import urllib.parse
import xml.dom.minidom
import zipfile

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import mfa_with_pyotp

ApigeeHost = APIGEE_ADMIN_API_URL
UserPW = None
Directory = None
Organization = None
Environment = None
Name = None
BasePath = '/'
ShouldDeploy = True
ShouldOverride = False
GracePeriod = 15
AccessToken = None

url = urllib.parse.urlparse(ApigeeHost)
httpScheme = url[0]
httpHost = url[1]

body = None

def httpCall(verb, uri, headers, body):
    if httpScheme == 'https':
        conn = http.client.HTTPSConnection(httpHost)
    else:
        conn = http.client.HTTPConnection(httpHost)

    if headers == None:
        hdrs = dict()
    else:
        hdrs = headers

    if AccessToken:
        hdrs['Authorization'] = 'Bearer %s' % AccessToken
    else:
        hdrs['Authorization'] = 'Basic %s' % base64.b64encode(UserPW.encode()).decode()
    conn.request(verb, uri, body, hdrs)

    return conn.getresponse()


def getElementText(n):
    c = n.firstChild
    str = io.StringIO()

    while c != None:
        if c.nodeType == xml.dom.Node.TEXT_NODE:
            str.write(c.data)
        c = c.nextSibling

    return str.getvalue().strip()


def getElementVal(n, name):
    c = n.firstChild

    while c != None:
        if c.nodeName == name:
            return getElementText(c)
        c = c.nextSibling

    return None


# Return TRUE if any component of the file path contains a directory name that
# starts with a "." like '.svn', but not '.' or '..'
def pathContainsDot(p):
    c = re.compile('\.\w+')

    for pc in p.split('/'):
        if c.match(pc) != None:
            return True

    return False


def getDeployments():
    # Print info on deployments
    hdrs = {'Accept': 'application/xml'}
    resp = httpCall('GET',
                    '/v1/organizations/%s/apis/%s/deployments' \
                    % (Organization, Name),
                    hdrs, None)

    if resp.status != 200:
        return None

    ret = list()
    deployments = xml.dom.minidom.parse(resp)
    environments = deployments.getElementsByTagName('Environment')

    for env in environments:
        envName = env.getAttribute('name')
        revisions = env.getElementsByTagName('Revision')
        for rev in revisions:
            revNum = int(rev.getAttribute('name'))
            error = None
            state = getElementVal(rev, 'State')
            basePaths = rev.getElementsByTagName('BasePath')

            if len(basePaths) > 0:
                basePath = getElementText(basePaths[0])
            else:
                basePath = 'unknown'

            # svrs = rev.getElementsByTagName('Server')
            status = {'environment': envName,
                      'revision': revNum,
                      'basePath': basePath,
                      'state': state}

            if error != None:
                status['error'] = error

            ret.append(status)

    return ret


def printDeployments(dep):
    for d in dep:
        print('Environment: %s' % d['environment'])
        print('  Revision: %i BasePath = %s' % (d['revision'], d['basePath']))
        print('  State: %s' % d['state'])
        if d['state'] != 'deployed':
            sys.exit(1)
        if 'error' in d:
            print('  Error: %s' % d['error'])

def deploy(args):
    global UserPW
    global Directory
    global Organization
    global Environment
    global Name
    global ShouldDeploy
    global ShouldOverride
    global AccessToken

    # ApigeeHost = 'https://api.enterprise.apigee.com'
    UserPW = args.username + ':' + args.password
    Directory = args.directory
    Organization = args.org
    Environment = args.environment
    Name = args.name
    # BasePath = '/'
    ShouldDeploy = not args.import_only
    ShouldOverride = args.seamless_deploy
    # GracePeriod = 15
    AccessToken = mfa_with_pyotp.get_access_token(args)

    # if UserPW == None or \
    #         (Directory == None and ZipFile == None) or \
    #         Environment == None or \
    #         Name == None or \
    #         Organization == None:
    #     print """Usage: deploy -n [name] (-d [directory name] | -z [zipfile])
    #               -e [environment] -u [username:password] -o [organization]
    #               [-p [base path] -h [apigee API url] -i]
    #     base path defaults to "/"
    #     Apigee URL defaults to "https://api.enterprise.apigee.com"
    #     -i denotes to import only and not actually deploy
    #     """
    #     sys.exit(1)

    # url = urlparse.urlparse(ApigeeHost)
    # httpScheme = url[0]
    # httpHost = url[1]
    #
    # body = None

    if Directory != None:
        # Construct a ZIPped copy of the bundle in memory
        tf = io.BytesIO()
        zipout = zipfile.ZipFile(tf, 'w')

        dirList = os.walk(Directory)
        for dirEntry in dirList:
            if not pathContainsDot(dirEntry[0]):
                for fileEntry in dirEntry[2]:
                    if not fileEntry.endswith('~'):
                        fn = os.path.join(dirEntry[0], fileEntry)
                        en = os.path.join(
                            os.path.relpath(dirEntry[0], Directory),
                            fileEntry)
                        print('Writing %s to %s' % (fn, en))
                        zipout.write(fn, en)

        zipout.close()
        body = tf.getvalue()
    elif ZipFile != None:
        f = open(ZipFile, 'r')
        body = f.read()
        f.close()

    # Upload the bundle to the API
    hdrs = {'Content-Type': 'application/octet-stream',
            'Accept': 'application/json'}
    uri = '/v1/organizations/%s/apis?action=import&name=%s' % \
          (Organization, Name)
    resp = httpCall('POST', uri, hdrs, body)

    if resp.status != 200 and resp.status != 201:
        print('Import failed to %s with status %i:\n%s' % \
              (uri, resp.status, resp.read().decode()))
        sys.exit(2)

    deployment = json.loads(resp.read().decode())
    revision = int(deployment['revision'])

    print('Imported new proxy version %i' % revision)

    if ShouldDeploy and not ShouldOverride:
        # Undeploy duplicates
        deps = getDeployments()
        for d in deps:
            if d['environment'] == Environment and \
                    d['basePath'] == BasePath and \
                    d['revision'] != revision:
                print('Undeploying revision %i in same environment and path:' % \
                      d['revision'])
                conn = http.client.HTTPSConnection(httpHost)
                resp = httpCall('POST',
                                ('/v1/organizations/%s/apis/%s/deployments' +
                                 '?action=undeploy' +
                                 '&env=%s' +
                                 '&revision=%i') % \
                                (Organization, Name, Environment, d['revision']),
                                None, None)
                if resp.status != 200 and resp.status != 204:
                    print('Error %i on undeployment:\n%s' % \
                          (resp.status, resp.read().decode()))

        # Deploy the bundle
        hdrs = {'Accept': 'application/json'}
        resp = httpCall('POST',
                        ('/v1/organizations/%s/apis/%s/deployments' +
                         '?action=deploy' +
                         '&env=%s' +
                         '&revision=%i' +
                         '&basepath=%s') % \
                        (Organization, Name, Environment, revision, BasePath),
                        hdrs, None)

        if resp.status != 200 and resp.status != 201:
            print('Deploy failed with status %i:\n%s' % (resp.status, resp.read().decode()))
            sys.exit(2)

    if ShouldOverride:
        # Seamless Deploy the bundle
        print('Seamless deploy %s' % Name)
        hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = httpCall('POST',
                        ('/v1/organizations/%s/environments/%s/apis/%s/revisions/%s/deployments' +
                         '?override=true' +
                         '&delay=%s') % \
                        (Organization, Environment, Name, revision, GracePeriod),
                        hdrs, None)

        if resp.status != 200 and resp.status != 201:
            print('Deploy failed with status %i:\n%s' % (resp.status, resp.read().decode()))
            sys.exit(2)

    deps = getDeployments()
    printDeployments(deps)

def main():
    pass

if __name__ == '__main__':
    main()
