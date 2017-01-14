from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User 
from django.db import models

class Habit(models.Model):

  
    name = models.CharField(
        max_length=255,
    )
    startdate = models.DateField(

    )
    enddate = models.DateField(
    )
   
    monday = models.CharField(
        max_length=255,)
    tuesday = models.CharField(
        max_length=255,)
    wednesday = models.CharField(
        max_length=255,)
    thursday = models.CharField(
        max_length=255,)
    friday = models.CharField(
        max_length=255,)
    saturday = models.CharField(
        max_length=255,)
    sunday = models.CharField(
        max_length=255,)

    successes = models.IntegerField(
        editable=False,
        default=0,)
    fails = models.IntegerField(
        editable=False,
        default=0,)
    
    created_by = models.ForeignKey(User)
    
    passthrough = models.BooleanField(default = False, editable=False) #used in extras_c.py to mark if the css attributes for each day have been generated for the habit
    
    viewable_by_friends = models.BooleanField(default=True)
    
    def __str__(self):

        return self.name
    
    def getid(self):

        return self.id

    def get_absolute_url(self):

        return reverse('habits-view', kwargs={'pk': self.id})
    
    def get_absolute_url_friend(self):

        return reverse('habits-friend-view', kwargs={'pk': self.id})

    def getTimesPerDay(self):
        return {
            0: int(self.monday),
            1: int(self.tuesday),
            2: int(self.wednesday),
            3: int(self.thursday),
            4: int(self.friday),
            5: int(self.saturday),
            6: int(self.sunday),
        }

    def isOnDate(self, datetime):
        dayOfWeek = datetime.weekday()
        onDays = self.getTimesPerDay()
        return datetime >= self.startdate and datetime <= self.enddate and onDays[dayOfWeek] > 0
    
    def isInRange(self, startExcl, endIncl):
        return startExcl > self.startdate or endIncl <= self.enddate


class cssnumbers(models.Model):
    def getid(self):

        return self.id
    
    habits = models.ManyToManyField(Habit)
    number = models.IntegerField()
    isgreen = models.BooleanField(default = False)
    isred = models.BooleanField(default = False)
    