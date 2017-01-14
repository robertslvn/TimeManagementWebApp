from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    
    url(r'^tasks/$', views.taskpView, name='tasks'),
    url(r'^matrix_tasks/$', views.matrix_tasks, name='matrix_tasks'),
    url(r'^add_todo/$', views.add_todo, name='add_todo'),
    url(r'^delete_task/$', views.deletetask, name='delete_task'),
    url(r'^add_todo/(?P<added>[\w]+)$', views.add_todo, name='add_todo'),
    url(r'^updateName/$', views.updateName, name='update_name'),
    url(r'^toggleTaskFlag/$', views.toggleTaskFlag, name='toggleTaskFlag'),
    url(r'^updateDate/$', views.updateDate, name='update_date'),
    
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/(?P<message>[\w]+)/$', views.login, name='login'),
    url(r'^account/$', views.account, name='account'),
    url(r'^account/(?P<message>[\w]+)$', views.account, name='account'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^friends/(?P<message>[\w]+)/$', views.friends, name='friends'),
    url(r'^friends/(?P<message>[\w]+)/(?P<requestUsername>[\w\W]+)/$', views.friends, name='friends'),
    url(r'^friend/(?P<friendName>[\w]+)/$', views.viewFriend, name='viewFriend'),
    url(r'^handleFriendRequest/$', views.handleFriendRequest, name='handleFriendRequest'),
    
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^group/(?P<groupId>[\d]+)/$', views.viewGroup, name='viewGroup'),
    url(r'^removeUser/$', views.removeUserFromGroup, name='removeUserFromGroup'),
    url(r'^makeAdmin/$', views.makeGroupAdmin, name='makeGroupAdmin'),
    url(r'^demoteAdmin/$', views.demoteGroupAdmin, name='demoteGroupAdmin'),
    url(r'^addGroupTask/$', views.addGroupTask, name='addGroupTask'),
    url(r'^deleteGroupTask/$', views.deleteGroupTask, name='deleteGroupTask'),
    url(r'^toggleGroupTaskFlag/$', views.toggleGroupTaskFlag, name='toggleGroupTaskFlag'),
    url(r'^updateGroupTaskDate/$', views.updateGroupTaskDate, name='updateGroupTaskdate'),
    
    url(r'^habit_tracker', views.ListHabitView.as_view(), 
        name='habits-list',), 
    url(r'^newweekly$', views.CreateHabitView.as_view(),
        name='habits-new',),
    url(r'^newdaily$', views.CreateHabitView2.as_view(),
        name='habits-new2',),
    url(r'^newtype$', views.CreateHabitViewType.as_view(),
        name='habits-new-type',),
    url(r'^delete/(?P<pk>\d+)$', views.DeleteHabitView.as_view(),
        name='habits-delete',),
    url(r'^(?P<pk>\d+)', views.HabitView.as_view(),
        name='habits-view',),
    url(r'^friendHabit/(?P<pk>\d+)/$', views.HabitFriendView.as_view(),
        name='habits-friend-view',),
    
]
