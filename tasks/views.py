from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    return render(request, 'tasks/home.html')


@login_required(login_url='login')
def task_list(request):
    # Get status and priority parameters from the request
    status = request.GET.get('status', None)
    priority = request.GET.get('priority', None)

    # Fetch tasks based on the authenticated user and optional status/priority parameters
    tasks = Task.objects.filter(user=request.user)

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'status': status, 'priority': priority})


@login_required(login_url='login')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.user != request.user:
        return redirect('task_list')  # Redirect to task list if not the owner
    task.delete()
    return redirect('task_list')  # Redirect to task list after deletion


@login_required(login_url='login')
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/update_task.html', {'form': form, 'task': task})


def task_details(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_details.html', {'task': task})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Automatically log in the user
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth_login(request, user)

            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'tasks/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Extract username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                auth_login(request, user)  # Use the renamed login function
                # Redirect to a success page
                return redirect('home')
            else:
                # User authentication failed
                form.add_error(None, 'Invalid username or password')

    else:
        form = AuthenticationForm(request)

    return render(request, 'tasks/login.html', {'form': form})
