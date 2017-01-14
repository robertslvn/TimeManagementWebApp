from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
import datetime

class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    

class Group(models.Model):
    name = models.CharField(max_length=100, unique=False)
    owner = models.ForeignKey(User, unique=False)
    admins = models.ManyToManyField(User, related_name='adminOf')
    members = models.ManyToManyField(User, related_name='groupsIn')
    requestsToJoin = models.ManyToManyField(User, related_name='pendingGroupRequests')
#     tasks = models.ManyToManyField(GroupTask)
    
    def isOwner(self, user):
        return self.owner == user
    
    def isMemberOf_ByUsername(self, username):
        return self.isMemberOf_ByUser(username=username)
    def isMemberOf_ByUser(self, user):
        return self.members.filter(username=user.username).exists()
    
    def addMember(self, user):
        self.members.add(user)
        
    def removeMember(self, user):
        self.members.remove(user)
    
    def addAdmin(self, user):
        self.admins.add(user)
        
    def removeAdmin(self, user):
        self.admins.remove(user)
    
    def isAdmin(self, user):
        return self.isOwner(user) or self.admins.filter(username=user.username).exists() 
    
    def hasHigherPrivileges(self, user1, user2):
        return self.isOwner(user1) or (self.isAdmin(user1) and not self.isAdmin(user2))
    
    def addTask(self, task):
        self.tasks.add(task)
    
    def changeName(self, newName):
        self.name = newName
        self.save()
        
        
class GroupInvite(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invitedBy = models.ForeignKey(User)

    
class GroupTask(MPTTModel):
    name = models.CharField(max_length=50, unique=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    created_by = models.ForeignKey(User, null=True, blank=True, db_index=True)
    completed = models.BooleanField(default=False)
    duedate = models.DateField(blank=True, null=True)
    urgent = models.BooleanField(default=False) # Checkbox Field
    important = models.BooleanField(default=False) # Checkbox Field
    description = models.TextField(blank=True) #Like a TEXT field
    assignees = models.ManyToManyField(User, related_name='assignedTo', blank=True)
    group = models.ForeignKey(Group, related_name='tasks')
    
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
    
