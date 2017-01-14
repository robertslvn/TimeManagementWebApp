from todolist.models import ExtendUser, Group, Habit, GroupTask, taskp
from todolist.forms import AddFriendForm, CreateGroupForm, AddToGroupForm, AddGroupTaskForm, ChangeGroupNameForm
from todolist.views import taskUpdatePostHandler
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
import re

def friends(request, message='', requestUsername=''):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            try:
                requestUsername = form.cleaned_data['friendUserName']
                friend = ExtendUser.objects.get(user=User.objects.get(username=requestUsername))
                currUser = ExtendUser.objects.get(user=request.user)
                if friend == currUser:
                    # can't friend self
                    return HttpResponseRedirect(reverse('friends', kwargs={'message': 'friendSelf'}))
                
                if currUser.isFriend(requestUsername):
                    # already friends
                    return HttpResponseRedirect(reverse('friends', kwargs={'message': 'alreadyFriends', 'requestUsername': requestUsername}))
                
                if friend.requestExists(request.user.username):
                    # request already sent
                    return HttpResponseRedirect(reverse('friends', kwargs={'message': 'alreadySent', 'requestUsername': requestUsername}))
                
                if currUser.requestExists(requestUsername):
                    # other user already requested. just accept
                    request.user.extenduser.addFriend(requestUsername)
                    request.user.extenduser.deleteFriendRequest(requestUsername)
                    return HttpResponseRedirect(reverse('friends'))

                # send request
                friend.addFriendRequest_ByUser(currUser.user)
                return HttpResponseRedirect(reverse('friends', kwargs={'message': 'requestSent', 'requestUsername': requestUsername}))
            
            except User.DoesNotExist:
                # user not found
                return HttpResponseRedirect(reverse('friends', kwargs={'message': 'userNotFound', 'requestUsername': requestUsername}))
    
    # otherwise GET
    form = AddFriendForm()
    friendsList = request.user.extenduser.friends.all()
    return render(request, 'social/friends.html', {'addFriendForm': form, 'friendsList': friendsList, 'message': message, 'requestUsername': requestUsername})
    
def handleFriendRequest(request):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        accept = bool(request.POST['accept'])
        request.user.extenduser.deleteFriendRequest(request.POST['friend'])
        if accept:
            request.user.extenduser.addFriend(request.POST['friend'])
        return HttpResponseRedirect(reverse('friends'))
    else:
        return HttpResponseRedirect(reverse('friends'))
    
def viewFriend(request, friendName):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse('index'))

    if not request.user.extenduser.isFriend(friendName):
        return HttpResponseRedirect(reverse('friends'))

    friendUser = User.objects.get(username=friendName)
    
    if request.method == "POST" and "unfriend=" in request.body:
        request.user.extenduser.removeFriend(friendUser)
        return HttpResponseRedirect(reverse('friends'))
    
    tasks = taskp.objects.filter(created_by=friendUser, public=True).all()
    habits = Habit.objects.filter(created_by=friendUser, viewable_by_friends=True).all()
    return render(request, 'social/friendProfile.html', {'friend': friendUser, 'nodes': tasks, 'habits': habits, 'viewingFriend': True})


def groups(request, message=''):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        if request.POST['formName'] == 'createGroup':
            form = CreateGroupForm(request.POST)
            if form.is_valid():
                newGroup = Group(name=form.cleaned_data['name'], owner=request.user)
                newGroup.save()
                newGroup.addMember(request.user)
                return HttpResponseRedirect(reverse('groups')) 
    else:
        return render(request, 'social/groups.html', {'createGroupForm': CreateGroupForm(), 'message': message})
    
def viewGroup(request, groupId):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse('index'))

    try:
        group = Group.objects.get(pk=groupId)
    
        if request.method == 'POST':
            if "newName=" in request.body: # add user handling
                form = ChangeGroupNameForm(request.POST)
                if form.is_valid():
                    group.changeName(form.cleaned_data['newName'])
                return HttpResponseRedirect(reverse('viewGroup', kwargs={'groupId': group.pk}))
            elif "username=" in request.body: # add user handling
                form = AddToGroupForm(request.POST)
                if form.is_valid():
                    try:
                        addUser = User.objects.get(username=form.cleaned_data['username'])
                        if request.user.extenduser.isFriend(addUser.username):
                            group.members.add(addUser)
                        else:
                            return render(request, 'social/groupPage.html', {'group': group, 'nodes': group.tasks.all(), 'addUserForm': AddToGroupForm(),
                                                                             'changeGroupNameForm': ChangeGroupNameForm(), 'message': 'userNotFound', 
                                                                             'addUsername': form.cleaned_data['username'], 'viewingGroup': True})
                    except User.DoesNotExist:
                        # user not found
                        return render(request, 'social/groupPage.html', {'group': group, 'nodes': group.tasks.all(), 'addUserForm': AddToGroupForm(), 
                                                                         'changeGroupNameForm': ChangeGroupNameForm(), 'message': 'userNotFound', 
                                                                         'addUsername': form.cleaned_data['username'], 'viewingGroup': True})
            elif "deleteGroup=" in request.body:
                group.delete()
                return HttpResponseRedirect(reverse('groups'))
            else:       # save task ordering
                taskUpdatePostHandler(request, GroupTask)
        
        elif request.method == 'PUT':
            splitRequestData = re.split('&|=',request.body)
            completed = splitRequestData[1]
            completedID = splitRequestData[3]
            if int(completed) == 1:
                print GroupTask.objects.filter(pk=completedID).update(completed=True)
            else:
                print GroupTask.objects.filter(pk=completedID).update(completed=False)
            return HttpResponse("OK")
    except Group.DoesNotExist:
        return HttpResponseRedirect(reverse('groups'))
    
    # otherwise GET
    if not group.isMemberOf_ByUser(request.user):
        return HttpResponseRedirect(reverse('groups'))
    return render(request, 'social/groupPage.html', {'group': group, 'nodes': group.tasks.all(), 'addUserForm': AddToGroupForm(), 'changeGroupNameForm': ChangeGroupNameForm(), 
                                                     'message': '', 'viewingGroup': True})

def removeUserFromGroup(request):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse('index'))
   
    try:
        group = Group.objects.get(pk=request.POST['groupId'])
        if request.method == 'POST':
            try:
                removeUser = User.objects.get(username=request.POST['username'])
                if group.hasHigherPrivileges(request.user, removeUser):
                    group.removeMember(removeUser)
            except User.DoesNotExist:
                 pass
    except:
        return HttpResponseRedirect(reverse('groups'))
    
    # otherwise get group page
    return HttpResponseRedirect(reverse('viewGroup', kwargs={'groupId': request.POST['groupId']}))
   
def makeGroupAdmin(request):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse('index'))
   
    try:
        group = Group.objects.get(pk=request.POST['groupId'])
    
        if request.method == 'POST':
            try:
                adminUser = User.objects.get(username=request.POST['username'])
                if group.isOwner(request.user):
                    group.addAdmin(adminUser)
            except User.DoesNotExist:
                 pass
    except:
        return HttpResponseRedirect(reverse('groups')) 
    # otherwise get group page
    return HttpResponseRedirect(reverse('viewGroup', kwargs={'groupId': request.POST['groupId']}))
   
def demoteGroupAdmin(request):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse('index'))

    try:
        group = Group.objects.get(pk=request.POST['groupId'])
        
        if request.method == 'POST':
             try:
                 adminUser = User.objects.get(username=request.POST['username'])
                 if group.isOwner(request.user):
                     group.removeAdmin(adminUser)
             except User.DoesNotExist:
                 pass
    except:
        return HttpResponseRedirect(reverse('groups'))
    # otherwise get group page
    return HttpResponseRedirect(reverse('viewGroup', kwargs={'groupId': request.POST['groupId']}))


def addGroupTask(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        try:
            group = Group.objects.get(id=request.POST['groupId'])
        except:
            return HttpResponseRedirect(reverse('groups'))
        if 'namej' in request.POST:
            saveToTheDB = GroupTask.objects.create(name=request.POST.get('namej'), group=group, created_by=request.user, parent=None)
            reqData = {}
            reqData['savepk'] = saveToTheDB.pk 
            return JsonResponse(reqData)
        
        form = AddGroupTaskForm(request.POST)
        if form.is_valid() and group.isAdmin(request.user):
            newTask = form.save()
            group.addTask(newTask)
            return HttpResponseRedirect(reverse('viewGroup', kwargs={'groupId': request.POST['groupId']}))
    elif request.method == 'GET':
        group = Group.objects.get(id=request.GET['groupId'])
        return render(request, 'social/addGroupTask.html', {'form': AddGroupTaskForm(group=group, request=request), 'groupId': group.pk})
    else:
        return HttpResponseRedirect(reverse('groups'))
    
def deleteGroupTask(request):
    if request.method == 'POST':
        splitRequestData = re.split('&|=',request.body)
        ids = int(splitRequestData[1])
        GroupTask.objects.get(pk=ids).get_descendants(include_self=True).delete();
        return HttpResponse("OK")
    
def toggleGroupTaskFlag(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        splitRequestData = re.split('&|=',request.body)
        id = int(splitRequestData[1])
        field = splitRequestData[3]
        groupId = splitRequestData[5]
        
        group = Group.objects.get(id=groupId)
        
        if not group.isAdmin(request.user):
            return HttpResponseForbidden()
        
        task = GroupTask.objects.get(pk=id)
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
    
def updateGroupTaskDate(request):
    if request.method == 'POST':
        splitRequestData = re.split('&|=',request.body)
        if len(splitRequestData) >=3:
            id = int(splitRequestData[1])
            changedate = splitRequestData[3]
            groupId = splitRequestData[5]
            
            group = Group.objects.get(id=groupId)
        
            if not group.isAdmin(request.user):
                return HttpResponseForbidden()
            
            task = GroupTask.objects.get(pk=id)
            task.duedate = changedate
            task.save()
        return HttpResponse("OK")
