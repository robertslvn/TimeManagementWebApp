from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from social import FriendRequest, Group, GroupInvite

class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self')
    requests = models.ManyToManyField(FriendRequest)
    # groupsIn attribute on User
    groupInvites = models.ManyToManyField(GroupInvite)
    
    def requestExists(self, friendUsername):
        friendUser = User.objects.get(username=friendUsername)
        return self.requests.filter(user=friendUser).exists()
        
    def addFriendRequest_ByUser(self, friendUser):
        if self.requests.filter(user=friendUser).exists():
            return False
        friendRequest = FriendRequest(user=friendUser)
        friendRequest.save()
        self.save()
        self.requests.add(friendRequest)
        return True
    def addFriendRequest_ByUsername(self, friendUsername):
        friendUser = User.objects.get(username=friendUsername)
        return self.addFriendRequest_ByUser(friendUser)
        
    def deleteFriendRequest(self, friendUsername):
        friendRequests = FriendRequest.objects.filter(user=User.objects.get(username=friendUsername)).all()
        for friendRequest in friendRequests:
            self.requests.remove(friendRequest)
            friendRequest.delete()
    
    def addFriend(self, friendUsername):
        self.friends.add(ExtendUser.objects.get(user=User.objects.get(username=friendUsername)))
        
    def isFriend(self, friendUsername):
        friendUser = User.objects.get(username=friendUsername)
        return self.friends.filter(user=friendUser).exists()
    
    def removeFriend(self, friendUser):
        self.friends.remove(friendUser.extenduser)
    
    # invited by is a user object
    def inviteToGroup(self, groupName, invitedBy):
        group = Group.objects.get(name=groupName)
        self.groupInvites.add(GroupInvite(group, invitedBy))