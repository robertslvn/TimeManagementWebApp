from todolist.models import ExtendUser
from todolist.forms import RegisterForm, ChangeEmailForm, ChangePasswordForm
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse
import re

def login(request, message=''):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {'form': AuthenticationForm(request), 'message': message})
    else:
        loginResult = auth_views.login(request)
        if type(loginResult) != HttpResponseRedirect:
            return render(request, 'registration/login.html', {'form': AuthenticationForm(request), 'message': 'invalidLogin'})
        return loginResult


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if not re.match('^[\w]+$', form.cleaned_data['userName']):
                return render(request, 'registration/register.html', {'form': form, 'message': 'invalidUserName'})
            if form.cleaned_data['password'] != form.cleaned_data['confirmPassword']:
                return render(request, 'registration/register.html', {'form': form, 'message': 'passwordsNotMatching'})
            try:
                User.objects.get_by_natural_key(username=form.cleaned_data['userName'])
                return render(request, 'registration/register.html', {'form': form, 'message': 'userNameTaken'})
            except User.DoesNotExist:
                newUser = User.objects.create_user(form.cleaned_data['userName'], None, form.cleaned_data['password'])
                newExtendUser = ExtendUser()
                newExtendUser.user = newUser
                newUser.save()
                newExtendUser.save()
                return HttpResponseRedirect(reverse('login', kwargs={'message': 'fromRegister'}))
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form, 'message': ''})


def account(request, message=''):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return HttpResponseRedirect(reverse('account', kwargs={'message': 'emailSuccess'}))
        
        passwordForm = ChangePasswordForm(request.POST)
        if passwordForm.is_valid():
            if not request.user.check_password(passwordForm.cleaned_data['oldPassword']):
                # wrong old password
                return HttpResponseRedirect(reverse('account', kwargs={'message': 'incorrectOldPassword'}))

            if passwordForm.cleaned_data['newPassword'] == passwordForm.cleaned_data['confirmPassword']:
                # valid
                request.user.set_password(passwordForm.cleaned_data['newPassword'])
                request.user.save()
                return HttpResponseRedirect(reverse('login', kwargs={'message': 'passwordChanged'}))
            else:
                # passwords don't match
                return HttpResponseRedirect(reverse('account', kwargs={'message': 'passwordsNotMatching'}))
                
            
    else:
        form = ChangeEmailForm(initial={'email': request.user.email})
        passwordForm = ChangePasswordForm()
        return render(request, 'registration/account.html', {'form': form, 'passwordForm': passwordForm, 'message': message})
