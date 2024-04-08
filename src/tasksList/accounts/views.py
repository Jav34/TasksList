from django.shortcuts import render, redirect, get_list_or_404
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.aut.decorators import login_required
from .models import Task, Project
from .forms import TaskForm, ProjectForm

# definicja strony rejestracji użytkownika
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# definicja panelu logowania
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') #tu następuje przekierowanie usera po zalogowaniu
        else:
            messages.error(request, 'Nieprawidłowa nazwa użytkownika lub hasło.')
    return render(request, 'registration/login.html')

#Poniżej definicja widoków dla task_list, task detail, task_create, task_update, task_delate

# model Task

@login_required
def task_list(request):
    task = Task.objects.all()
    return render(request, 'task_list.html', {'task': task})

@login_required
def task_details(request, task_id):
    task = get_list_or_404(Task, id=task_id)
    return render(request, 'task_details.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_update(request, task_id):
    task = get_list_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_form.html', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

# model Project

@login_required
def project_list(request):
    project = Project.objects.all()
    return render(request, 'project_list.html', {'project': project})

@login_required
def project_details(request, project_id):
    project = get_list_or_404(Project, id=project_id)
    return render(request, 'project_details.html', {'project': project})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectFormForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_update(request, project_id):
    project = get_list_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_form.html', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'project_confirm_delete.html', {'project': project})