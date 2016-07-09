#!/usr/bin/env python3

import argparse
#from ovirtsdk.api import API
#from ovirtsdk.xml import params

#VERSION = params.Version(major='3', minor='0')

# define Parser for the cli arguments

parser = argparse.ArgumentParser(description='ovirt opensource management tool')
parser.add_argument('--createdc', help='create new data center')
parser.add_argument('--createclu', help='create new cluster')
parser.add_argument('--addhosts', help='add new host(s) to cluster')

args = parser.parse_args()



