from todolist.models import ExtendUser, taskp, GroupTask, Habit
from todolist.forms import AddToDoForm
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
import urllib
import json, re
import time
import datetime


def index(request): 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)
    week = today + datetime.timedelta(days=7)
    tasks = taskp.objects.filter(created_by=request.user, completed=False).all()
    grouptasks = request.user.assignedTo.filter(completed=False).all()
    habits = Habit.objects.filter(created_by=request.user).all()
    
    upcoming = {}
    upcoming['today'] = {
        'tasks': tasks.filter(duedate=today),
        'grouptasks': grouptasks.filter(duedate=today),
        'habits': [],
    }
    for habit in habits:
        if habit.isOnDate(today):
            upcoming['today']['habits'].append(habit)
    
    upcoming['tomorrow'] = {
        'tasks': tasks.filter(duedate=tomorrow),
        'grouptasks': grouptasks.filter(duedate=tomorrow),
        'habits': [],
    }
    for habit in habits:
        if habit.isOnDate(tomorrow):
            upcoming['tomorrow']['habits'].append(habit)
    
    upcoming['week'] = {
        'tasks': tasks.filter(duedate__gt=tomorrow, duedate__lte=week),
        'grouptasks': grouptasks.filter(duedate__gt=tomorrow, duedate__lte=week),
        'habits': [],
    }
    for habit in habits:
        if habit.isInRange(tomorrow, week):
            upcoming['week']['habits'].append(habit)
    
    return render(request, 'index.html', {'upcoming': upcoming})


def add_todo(request, added=False):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.POST:
        if 'namej' in request.POST:
            nameOfTaskToAdd = request.POST.get('namej')
            saveToTheDB = taskp.objects.create(name=nameOfTaskToAdd, created_by=request.user, parent=None)
            reqData = {}
            reqData['savepk'] = saveToTheDB.pk 
            return JsonResponse(reqData)
            
            
    form = AddToDoForm(request.POST)
    if form.is_valid():
        newTask = form.save(commit=False)
        newTask.save()
        return HttpResponseRedirect(reverse('add_todo', kwargs={'added': True}))
    else:
        form = AddToDoForm(request=request)

    return render(request, 'add_todo.html', locals())


def matrix_tasks(request):  # Define our function, accept a request
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    urg_imp = taskp.objects.filter(urgent=True, important=True, created_by=request.user)
    urg_Nimp = taskp.objects.filter(urgent=True, important=False, created_by=request.user)
    Nurg_imp = taskp.objects.filter(urgent=False, important=True, created_by=request.user)
    Nurg_Nimp = taskp.objects.filter(urgent=False, important=False, created_by=request.user)

    return render(request, 'matrix_tasks.html', {'urg_imp': urg_imp, 'urg_Nimp': urg_Nimp, 'Nurg_imp': Nurg_imp, 'Nurg_Nimp': Nurg_Nimp})

@ensure_csrf_cookie
def taskpView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'GET':
        tasks = taskp.objects.filter(created_by=request.user).all()
        return render(request, 'taskp.html', {'nodes': tasks})
    if request.method == 'POST':
        taskUpdatePostHandler(request, taskp)
        return HttpResponse("OK")
    if request.method == 'PUT':
        splitRequestData = re.split('&|=',request.body)
        completedz = splitRequestData[1]
        completedID = splitRequestData[3]
        if int(completedz) == 1:
            print taskp.objects.filter(pk=completedID).update(completed=True)
        else:
            print taskp.objects.filter(pk=completedID).update(completed=False)

        return HttpResponse("OK")
@ensure_csrf_cookie    
def taskUpdatePostHandler(request, TaskClass):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    print request.body
    splitRequestData = re.split('&|=',request.body)
    actual_id = int(splitRequestData[1])
    parent_id = int(splitRequestData[3])
    prev_id = int(splitRequestData[7])
    next_id = int(splitRequestData[9])

        
    if(parent_id>0):
        if(prev_id>0):
            TaskClass.objects.move_node(TaskClass.objects.get(pk=actual_id), TaskClass.objects.get(pk=prev_id), position='right')
        else:
            TaskClass.objects.move_node(TaskClass.objects.get(pk=actual_id), TaskClass.objects.get(pk=parent_id), position='first-child')
    else:
        if(prev_id>0):
            TaskClass.objects.move_node(TaskClass.objects.get(pk=actual_id), TaskClass.objects.get(pk=prev_id), position='right')
        else:
            TaskClass.objects.move_node(TaskClass.objects.get(pk=actual_id), TaskClass.objects.get(pk=next_id), position='left')

def updateName(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        splitRequestData = re.split('&|=',request.body)
        ids = int(splitRequestData[1])
        newname = urllib.unquote(splitRequestData[3])
        newnamedecode = urllib.unquote(newname)
        
        if taskp.objects.get(pk=ids).created_by != request.user:
            return HttpResponseForbidden()
        
        taskp.objects.filter(pk=ids).update(name=newnamedecode)
        return HttpResponse("OK")
        
def deletetask(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        splitRequestData = re.split('&|=',request.body)
        ids = int(splitRequestData[1])
        
        if taskp.objects.get(pk=ids).created_by != request.user:
            return HttpResponseForbidden()
        
        taskp.objects.get(pk=ids).get_descendants(include_self=True).delete();
        return HttpResponse("OK")
    
def toggleTaskFlag(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        splitRequestData = re.split('&|=', request.body)
        id = int(splitRequestData[1])
        field = splitRequestData[3]
        
        if taskp.objects.get(pk=id).created_by != request.user:
            return HttpResponseForbidden()
        
        task = taskp.objects.get(pk=id)
        if field == 'urgent':
            task.urgent = not task.urgent
        elif field == 'important':
            task.important = not task.important
        elif field == 'public':
            task.public = not task.public
        else:
            return HttpResponseBadRequest()
        task.save()
        return HttpResponse("OK")
    else:
        return HttpResponseForbidden()
        
def updateDate(request):
    if request.method == 'POST':
        splitRequestData = re.split('&|=',request.body)
        if len(splitRequestData) >=3:
	    if splitRequestData[2] != 'groupId':
		    ids = int(splitRequestData[1])
		    changedate = splitRequestData[3]
		    taskp.objects.filter(pk=ids).update(duedate=changedate)
        return HttpResponse("OK")
        
