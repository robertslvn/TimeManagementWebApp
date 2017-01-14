from django import forms
from django.forms import ModelForm
from models import taskp, GroupTask, Group
from django.contrib.admin import widgets 
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
from models import Habit

from functools import partial



class RegisterForm(forms.Form):
    userName = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput())
    confirmPassword = forms.CharField(label='Confirm Password', max_length=50, widget=forms.PasswordInput())
    
class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label="Email")
    
class ChangePasswordForm(forms.Form):
    oldPassword = forms.CharField(label='Old Password', max_length=50, widget=forms.PasswordInput())
    newPassword = forms.CharField(label='New Password', max_length=50, widget=forms.PasswordInput())
    confirmPassword = forms.CharField(label='Confirm New Password', max_length=50, widget=forms.PasswordInput())
    
    
class AddFriendForm(forms.Form):
    friendUserName = forms.CharField(label='', max_length=50)

    
class AddToDoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        DateInput = partial(forms.DateInput, {'class': 'datepicker'})
        if kwargs.has_key('request'):
            request = kwargs.pop('request')
            super(AddToDoForm, self).__init__(*args, **kwargs)
            self.fields['created_by'].initial = request.user
            self.fields['created_by'].widget = forms.HiddenInput()
            self.fields['parent'].queryset = taskp.objects.filter(created_by=request.user)
            self.fields['duedate'].label = 'Due date (MM/DD/YYYY)'
            self.fields['duedate'] = forms.DateField(widget=DateInput(), required=False)
            self.fields['public'].label="Allow friends to view"
            self.fields['parent'].label = "Subtask of"
        else:
            super(AddToDoForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = taskp
        exclude = ['completed']
        
        
class AddGroupTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        DateInput = partial(forms.DateInput, {'class': 'datepicker'})
        if kwargs.has_key('request') and kwargs.has_key('group'):
            request = kwargs.pop('request')
            group = kwargs.pop('group')
            super(AddGroupTaskForm, self).__init__(*args, **kwargs)
            self.fields['created_by'].initial = request.user
            self.fields['created_by'].widget = forms.HiddenInput()
            self.fields['parent'].queryset = GroupTask.objects.filter(pk__in=group.tasks.all())
            self.fields['parent'].label = "Parent Task"
            self.fields['parent'].empty_label = "None"
            self.fields['assignees'].widget = CheckboxSelectMultiple()
            self.fields['assignees'].queryset = User.objects.filter(id__in=group.members.all())
            self.fields['duedate'].label = 'Due date (MM/DD/YYYY)'
            self.fields['duedate'] = forms.DateField(widget=DateInput(), required=False)
            self.fields['group'].initial = group.pk
            self.fields['group'].widget = forms.HiddenInput()
            
        else:
            super(AddGroupTaskForm, self).__init__(*args, **kwargs)
            
    
    class Meta:
        model = GroupTask
        exclude = ['completed']
        
class CreateGroupForm(forms.Form):
    name = forms.CharField(label='Group Name', max_length=100)

class AddToGroupForm(forms.Form):
    username = forms.CharField(label='', max_length=50)

class ChangeGroupNameForm(forms.Form):
    newName = forms.CharField(label='', max_length=100)

##form for weekly habits
class HabitForm(forms.ModelForm):


    DateInput = partial(forms.DateInput, {'class': 'datepicker'})

    
    startdate = forms.DateField(widget=DateInput())
    enddate = forms.DateField(widget=DateInput())
    
    monday = forms.DecimalField(
        initial='0',
        label="Number of times each Monday",
        required=True,
        min_value=0
    )
    tuesday = forms.DecimalField(
        initial='0',
        label="Number of times each Tuesday",
        required=True,
        min_value=0
    )
    wednesday = forms.DecimalField(
        initial='0',
        label="Number of times each Wednesday",
        required=True,
        min_value=0
    )
    thursday = forms.DecimalField(
        initial='0',
        label="Number of times each Thursday",
        required=True,
        min_value=0
    )
    friday = forms.DecimalField(
        initial='0',
        label="Number of times each Friday",
        required=True,
        min_value=0
    )
    saturday = forms.DecimalField(
        initial='0',
        label="Number of times each Saturday",
        required=True,
        min_value=0
    )
    sunday = forms.DecimalField(
        initial='0',
        label="Number of times each Sunday",
        required=True,
        min_value=0
    )
    
    ##override clean method, check if end date > start date and at habit occurs at least one day a week
    def clean(self):
        cleaned_data = super(HabitForm, self).clean()
        if not self._errors:
            start_date = cleaned_data.get("startdate")
            end_date = cleaned_data.get("enddate")
            mon = cleaned_data.get("monday")
            tue = cleaned_data.get("tuesday")
            wed = cleaned_data.get("wednesday")
            thu = cleaned_data.get("thursday")
            fri = cleaned_data.get("friday")
            sat = cleaned_data.get("saturday")
            sun = cleaned_data.get("sunday")
            if end_date < start_date:
                msg = "End date must be greater than start date."
                self.add_error('enddate', msg)
            if mon == 0 and tue ==0 and wed==0 and thu==0 and fri==0 and sat==0 and sun==0:
                msg = "You must perform this habit at least once per week."
                self.add_error('sunday', msg)
        else:
            return cleaned_data


    class Meta:
        model = Habit
        exclude = ['created_by']

##form for daily habits
class HabitForm2(forms.ModelForm):


    DateInput = partial(forms.DateInput, {'class': 'datepicker'})

    
    startdate = forms.DateField(widget=DateInput())
    enddate = forms.DateField(widget=DateInput())
    
    ##all days of the week are set to = monday in the habit view
    monday = forms.DecimalField(
        initial='0',
        label="Number of times each day",
        required=True,
        min_value=1
    )
    
    tuesday = forms.DecimalField(required=False)
    wednesday = forms.DecimalField(required=False)
    thursday = forms.DecimalField(required=False)
    friday = forms.DecimalField(required=False)
    saturday = forms.DecimalField(required=False)
    sunday = forms.DecimalField(required=False)
    
   
    
    
    ##override clean method, check if end date > start date
    def clean(self):
        cleaned_data = super(HabitForm2, self).clean()
        if not self._errors:
            start_date = cleaned_data.get("startdate")
            end_date = cleaned_data.get("enddate")
            if end_date < start_date:
                msg = "End date must be greater than start date."
                self.add_error('enddate', msg)
        else:
            return cleaned_data


    class Meta:
        model = Habit
        exclude = ['created_by']

