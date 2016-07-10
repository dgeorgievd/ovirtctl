#!/usr/bin/env python2.7

import argparse
import json
from ovirtsdk.api import API
from ovirtsdk.xml import params

VERSION = params.Version(major='3', minor='6')

#
# define Parser for the cli arguments
#

parser = argparse.ArgumentParser(description='ovirt opensource management tool')
parser.add_argument('--createdc', help='create new data center; requires config.json file', action='store_true')
parser.add_argument('--createclu', help='create new cluster; requires config.json file', action='store_true')
parser.add_argument('--addhosts', help='add new host(s) to cluster; requires config.json file', action='store_true')
parser.add_argument('--URL', help='API URL')
parser.add_argument('--user', help='user to login with')
parser.add_argument('--passwd', help='the user password')
parser.add_argument('--config', help='the config file to be used')

args = parser.parse_args()

URL =           args.URL
USERNAME =      args.user
PASSWORD =      args.passwd
CONFIGFILE =    args.config

#
# read the config.json file and load it in dictionary object
#

config_dict = json.loads(open(CONFIGFILE).read())

#
# initiate api connection
#

def connectAPI(url, username, password, insecure):
    api_connection = API(url, username, password, insecure)
    return api_connection

#
# define method to create cluster
#

def createdc(DCNAME, DCSTORAGETYPE, VERSION):
    try:
        if api.datacenters.add(params.DataCenter(name=DCNAME, storage_type=DCSTORAGETYPE, version=VERSION)):
            print 'iSCSI Data Center was created successfully'
    except Exception as e:
        print 'Failed to create iSCSI Data Center:\n%s' % str(e)





