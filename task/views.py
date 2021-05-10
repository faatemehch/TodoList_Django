from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Task
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    FormView,
    CreateView,
    DeleteView,
    UpdateView
)


# show all user's task
class TaskList( LoginRequiredMixin, ListView ):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        context['tasks'] = Task.objects.filter( user=self.request.user )
        context['complete_task_count'] = Task.objects.filter( user=self.request.user, complete=True ).count
        search_value = self.request.GET.get( 'search_value' ) or ''
        if search_value:
            # context['title'] =
            context['tasks'] = Task.objects.filter( user=self.request.user, title_task__icontains=search_value )
        return context


# login
class CustomLoginView( LoginView ):
    template_name = 'task/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy( 'task_list' )


# register
class RegisterView( FormView ):
    template_name = 'task/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy( 'task_list' )

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect( 'task_list' )
        return super( RegisterView, self ).get( *args, **kwargs )

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login( self.request, user )
        return super( RegisterView, self ).form_valid( form )


# add new task
class CreatTask( LoginRequiredMixin, CreateView ):
    model = Task
    fields = ['title_task']
    context_object_name = 'task'
    # template_name = 'task/task_form.html'
    success_url = reverse_lazy( 'task_list' )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super( CreatTask, self ).form_valid( form )


# delete Task
class DeleteTask( LoginRequiredMixin, DeleteView ):
    model = Task
    success_url = reverse_lazy( 'task_list' )


# update task
class UpdateTask( LoginRequiredMixin, UpdateView ):
    model = Task
    fields = ['title_task', 'complete']
    success_url = reverse_lazy( 'task_list' )


# change username
class UpdateUser( LoginRequiredMixin, UserPassesTestMixin, UpdateView ):
    model = User
    # form_class = PasswordChangeForm
    fields = ['username']
    success_url = reverse_lazy( 'task_list' )

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


# handle page not found error
def handler404(request, exception):
    return render( request, 'task/404.html', {} )
