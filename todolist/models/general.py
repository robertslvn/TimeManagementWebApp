from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User 
from mptt.models import MPTTModel, TreeForeignKey
import datetime

# class Task(models.Model): #Table name, has to wrap models.Model to get the functionality of Django.
#          
#     name = models.CharField(max_length=99) #Like a VARCHAR field
#     description = models.TextField(blank=True) #Like a TEXT field
#     created = models.DateTimeField(blank=True) #Like a DATETIME field
#     created_by = models.ForeignKey(User, null=True, blank=True)
#     parent = models.ForeignKey('self', null=True, blank=True, related_name='childTasks')
#     sort_order = models.IntegerField(default=0)
#     urgent = models.BooleanField(default=False) # Checkbox Field
#     important = models.BooleanField(default=False) # Checkbox Field
# 
#     def __unicode__(self): #Tell it to return as a unicode string (The name of the to-do item) rather than just Object.
#         return self.name

class taskp(MPTTModel):
    name = models.CharField(max_length=30, unique=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    created_by = models.ForeignKey(User, null=True, blank=True, db_index=True)
    completed = models.BooleanField(default=False)
    duedate = models.DateField(blank=True, null=True)
    urgent = models.BooleanField(default=False) # Checkbox Field
    important = models.BooleanField(default=False) # Checkbox Field
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    
    class MPTTMeta:
        order_insertion_by = ['created_by']
        
    def __unicode__(self):
        return self.name
    
    def getDaysLeft(self):
        daysLeft = self.duedate - datetime.datetime.now().date()
        daysLeft = daysLeft.days
        if daysLeft < 0:
            daysLeft = 'past due date'
        elif daysLeft == 0:
            daysLeft = 'in < 1 day'
        elif daysLeft == 1:
            daysLeft = 'in 1 day'
        else:
            daysLeft = 'in ' + str(daysLeft) + ' days'
        return daysLeft
