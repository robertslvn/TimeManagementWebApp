from django.shortcuts import render
from django.http import Http404
# Create your views here.
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from todolist import forms
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect

from todolist.models import Habit

##the list of all habits
class ListHabitView(ListView):

    model = Habit
    template_name = 'habit_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(ListHabitView, self).dispatch(request, *args, **kwargs)

    
##choose what type of habit to create
class CreateHabitViewType(ListView):

    model = Habit
    template_name = 'choosehabittype.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(CreateHabitViewType, self).dispatch(request, *args, **kwargs)
    
##detail view of 1 habit (with modify/delete options)
##userpassestestmixin makes sure this view can only be accessed by the user who created it
class HabitView(UserPassesTestMixin, DetailView):

    model = Habit
    template_name = 'habit.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(HabitView, self).dispatch(request, *args, **kwargs)
    
    def get_login_url(self):
        raise Http404()
    
    def test_func(self):
        orde = self.kwargs.get('pk')
        print orde
        tempe = get_object_or_404(Habit, pk=orde)
        return self.request.user == tempe.created_by

##detail view of 1 habit (friend mode - read only)
class HabitFriendView(DetailView):

    model = Habit
    template_name = 'habit-friend.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(HabitFriendView, self).dispatch(request, *args, **kwargs)


##view for creating a new weekly habit
class CreateHabitView(CreateView):

    model = Habit
    template_name = 'edit_habit.html'

    form_class = forms.HabitForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(CreateHabitView, self).dispatch(request, *args, **kwargs)
    
    ##get the current user as the user who created the habit
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(CreateHabitView, self).form_valid(form)

    ##redirect to the newly created habit (if successful creation)
    def get_success_url(self):
        return reverse('habits-view', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):

        context = super(CreateHabitView, self).get_context_data(**kwargs)
        context['action'] = reverse('habits-new')

        return context
    
##view for creating a new daily habit
class CreateHabitView2(CreateView):

    model = Habit
    template_name = 'edit_habit2.html'

    form_class = forms.HabitForm2
    
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(CreateHabitView2, self).dispatch(request, *args, **kwargs)
    
    ##get the current user as the user who created the habit and set all days to equal the user's input choice per day
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.tuesday = form.instance.monday
        form.instance.wednesday = form.instance.monday
        form.instance.thursday = form.instance.monday
        form.instance.friday = form.instance.monday
        form.instance.saturday = form.instance.monday
        form.instance.sunday = form.instance.monday
        return super(CreateHabitView2, self).form_valid(form)

    ##redirect to the newly created habit (if successful creation)
    def get_success_url(self):
        return reverse('habits-view', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):

        context = super(CreateHabitView2, self).get_context_data(**kwargs)
        context['action'] = reverse('habits-new2')

        return context

##view for deleting a habit
##userpassestestmixin makes sure this view can only be accessed by the user who created it
class DeleteHabitView(UserPassesTestMixin, DeleteView):

    model = Habit
    template_name = 'delete_habit.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(DeleteHabitView, self).dispatch(request, *args, **kwargs)
    
    def get_login_url(self):
        raise Http404()
    
    def test_func(self):
        orde = self.kwargs.get('pk')
        print orde
        tempe = get_object_or_404(Habit, pk=orde)
        return self.request.user == tempe.created_by

    def get_success_url(self):
        return reverse('habits-list')
