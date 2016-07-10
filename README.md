# ovirtctl
ovirtctl is managment utility for ovirt

ovirtctl is management utilitiy which allows you easily to automate the process of creation of new virtual DCs, clusters; addition of new; hosts to existing clusters; creation and modification of Virtual Machines using the ovirt management Python API.

# usage
```
usage: ovirtctl.py [-h] [--createdc] [--createclu] [--addhosts] [--URL URL ]
                   [--user USER] [--passwd PASSWD] [--config CONFIG]

ovirt opensource management tool

optional arguments:
  -h, --help       show this help message and exit
  --createdc       create new data center; requires config.json file
  --createclu      create new cluster; requires config.json file
  --addhosts       add new host(s) to cluster; requires config.json file
  --URL URL        API URL
  --user USER      user to login with
  --passwd PASSWD  the user password
  --config CONFIG  the config file to be used
```

# examples
create new DC
```
ovirtctl.py --createdc --URL 'https://example.com:8443/api' --user 'johnd' --passwd 'pass123' --config ./config.json
```
create new cluster
```
ovirtctl.py --createclu --URL 'https://example.com:8443/api' --user 'johnd' --passwd 'pass123' --config ./config.json
```
