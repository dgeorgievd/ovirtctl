#!/usr/bin/env python2.7

import argparse
import json
from time import sleep
from ovirtsdk.api import API
from ovirtsdk.xml import params

VERSION = params.Version(major='3', minor='6')

#
# define Parser for the cli arguments
#

parser = argparse.ArgumentParser(description='ovirt opensource management tool')
parser.add_argument('--setup', help='create new data center with cluster and add hosts to cluster; requires config.json file', action='store_true')
parser.add_argument('--createdc', help='create new data center; requires config.json file', action='store_true')
parser.add_argument('--createclu', help='create new cluster; requires config.json file', action='store_true')
parser.add_argument('--addhosts', help='add new host(s) to cluster; requires config.json file', action='store_true')
parser.add_argument('--URL', help='API URL')
parser.add_argument('--user', help='user to login with')
parser.add_argument('--passwd', help='the user password')
parser.add_argument('--config', help='the config file to be used')
parser.add_argument('--insecure', help='defines if the connection is secure or insecure - values: true or false')

args = parser.parse_args()

URL =           args.URL
USERNAME =      args.user
PASSWORD =      args.passwd
INSECURE =      args.insecure
CONFIGFILE =    args.config

#
# read the config.json file and load it in dictionary object
#

config_dict = json.loads(open(CONFIGFILE).read())

#
# initiate api connection
#

def connectAPI(url, username, password, insecure):
    api_connection = API(url, username, password, insecure=insecure)
    return api_connection

#
# define method to create data center object
#    if operation not successful throw an exception
#

def createDC(config_dict, VERSION, api):
    for dc in config_dict:
        try:
            if api.datacenters.add(params.DataCenter(name=config_dict[dc]['name'],
                                                     storage_type=config_dict[dc]['storage_type'], version=VERSION)):
                print 'Data Center was created successfully'
                print 'Starting procedure to add iSCSI Domain'
#                createISCSIdomain(config_dict)
        except Exception as e:
            print 'Failed to create Data Center:\n%s' % str(e)
            
#
# define method to create iSCSI storage domain to Data Center
#     if operation not successful throw an exception
#

# def createISCSIdomain(config_dict):
#     for dc in config_dict:
#     	for dstore in config_dict[dc]['storage_datastores']:
#     	    for store in config_dict[dc]['storage_datastores'][dstore]:
#                 storDomParams = params.StorageDomain(name=config_dict[dc]['storage_datastores'][dstore]['storage_name'],
#                                                      data_center=api.datacenters.get(config_dict[dc]['name']),
#                                                      storage_format='v2',
#                                                      type_='data',
#                                                      host=api.hosts.get(config_dict[dc]['storage_datastores'][dstore]['host_name']),
#                                                      storage = params.Storage(type_=config_dict[dc]['storage_datastores'][dstore]['storage_type'],
#                                                                               volume_group=params.VolumeGroup(logical_unit=[params.LogicalUnit(id=config_dict[dc]['storage_datastores'][dstore]['lun_guid'],
#                                                                                                                                                address=config_dict[dc]['storage_datastores'][dstore]['storage_address'],
#                                                                                                                                                port=3260,
#                                                                                                                                                target=config_dict[dc]['storage_datastores'][dstore]['target_name'])])))
# 
#                 try:
#                     if api.storagedomains.add(storDomParams):
#                         print 'iSCSI Storage Domain was created successfully'
#                 except Exception as e:
#                     print 'Failed to create iSCSI Storage Domain:\n%s' % str(e)
#     
#                 try:
#                     if api.datacenters.get(name=config_dict[dc]['name']).storagedomains.add(api.storagedomains.get(name=config_dict[dc]['storage_datastores'][dstore]['storage_name'])):
#                         print 'iSCSI Storage Domain was attached successfully'
#                 except Exception as e:
                        print 'Failed to attach iSCSI Storage Domain:\n%s' % str(e)

#
# define method to create cluster object
#    if operation not successful throw an exception
#

def createClu(config_dict, VERSION, api):
    for dc in config_dict:
        for clu in config_dict[dc]['clusters']:
            try:
                if api.clusters.add(params.Cluster(name=config_dict[dc]['clusters'][clu]['name'],
                                                   cpu=params.CPU(id=config_dict[dc]['clusters'][clu]['CPU']),
                                                   data_center=api.datacenters.get(config_dict[dc]['name']), version=VERSION)):
                    print 'Cluster %s created!' % str(clu)
            except Exception as e:
                print 'Failed to create Cluster:\n%s' % str(e)

#
# define method to add new host in existing cluster
#    if operation not successful throw an exception
#

def addHosts(config_dict, api):
    for dc in config_dict:
        for clu in config_dict[dc]['clusters']:
            for host in config_dict[dc]['clusters'][clu]['hosts']:
                try:
                    if api.hosts.add(params.Host(name=config_dict[dc]['clusters'][clu]['hosts'][host]['name'],
                                                 address=config_dict[dc]['clusters'][clu]['hosts'][host]['address'],
                                                 cluster=api.clusters.get(config_dict[dc]['clusters'][clu]['name']),
                                                 root_password=config_dict[dc]['clusters'][clu]['hosts'][host]['rootpasswd'])):
                        print 'Host installed '
                        print 'Waiting for host to reach operational status'
                        while api.hosts.get(config_dict[dc]['clusters'][clu]['hosts'][host]['name']).status.state != 'up':
                            sleep(1)
                        print "Host is up and running!"
                except Exception as e:
                    print 'Failed to install Host:\n%s' % str(e)

def setup(config_dict, VERSION, api):
    createDC(config_dict, VERSION, api)
    createClu(config_dict, VERSION, api)
    addHosts(config_dict)

if __name__ == "__main__":
    api = connectAPI(URL, USERNAME, PASSWORD, True)
    if args.setup:
        setup(config_dict, VERSION, api)
    if args.createdc:
        createDC(config_dict, VERSION, api)
    elif args.createclu:
        createClu(config_dict, VERSION, api)
    elif args.addhosts:
        addHosts(config_dict, api)
    else:
        print "Execute ovirtctl.py -h for more information"
