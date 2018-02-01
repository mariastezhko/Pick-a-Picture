from __future__ import unicode_literals
import re
from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/media/img')

class Criteria(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return "id: " + str(self.id) + "name: " + self.name

class Subcategory(models.Model):
     name = models.CharField(max_length=255)
     criteria = models.ForeignKey(Criteria, related_name = "subcategories", null=True)
     created_at = models.DateTimeField(auto_now_add = True)
     updated_at = models.DateTimeField(auto_now = True)

     def __unicode__(self):
         return "id: " + str(self.id) + "name: " + self.name

class Image(models.Model):
    name = models.CharField(max_length=255)
    #image = models.ImageField(upload_to='img', null=True, blank=True)
    image = models.ImageField(upload_to='static/img', null=True, blank=True)
    #image = models.ImageField(storage=fs, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, related_name = "images", null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return "id: " + str(self.id) + "name: " + self.name
