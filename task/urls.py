from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (
    TaskList,
    CustomLoginView,
    RegisterView,
    CreatTask,
    DeleteTask,
    UpdateTask,
    UpdateUser
)

from django.conf.urls import handler404

urlpatterns = [
    path( '', TaskList.as_view(), name='task_list' ),
    path( 'login', CustomLoginView.as_view(), name='login' ),
    path( 'register', RegisterView.as_view(), name='register' ),
    path( 'logout', LogoutView.as_view( next_page='login' ), name='logout' ),
    path( 'update_user/<int:pk>/', UpdateUser.as_view(), name='user-update' ),

    path( 'create', CreatTask.as_view(), name='create_task' ),
    path( 'delete/<int:pk>/', DeleteTask.as_view(), name='task-delete' ),
    path( 'update/<int:pk>/', UpdateTask.as_view(), name='task-update' ),

]
handler404 = 'task.views.handler404'
