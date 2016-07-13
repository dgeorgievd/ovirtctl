from __future__ import unicode_literals

from django.db import models

class DC(models.Model):
    name = models.CharField(max_length=30)
    storage_datastore = ForeignKey(StorageDatastore)
    clusters = ForeignKey(Clusters)
      
    
    
    
class StorageDatastore(models.Model):
    storage_datastore = models.CharField(max_length=50)
    host_name = models.CharField(max_length=30)
    storage_type = models.CharField(max_length=10)
    storage_name = models.CharField(max_length=50)
    storage_address = models.CharField(max_length=15)
    target_name = models.CharField(max_length=25)
    lun_guid = models.CharField(max_length=30)


class Clusters(models.Model):
    name = models.CharField(max_length=20)
    hosts = models.ForeignKey(Hosts)

class Hosts(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=15)
    rootpasswd = models.CharField(widget=forms.PasswordInput)