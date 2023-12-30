# tasks/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, task_list, create_task, task_details, update_task, delete_task, signup, login

urlpatterns = [
    path('', home, name='home'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', task_details, name='task_details'),
    path('tasks/<int:task_id>/update/', update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('login/', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', signup, name='signup'),
]

