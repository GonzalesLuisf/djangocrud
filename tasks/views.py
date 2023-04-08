from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import TaskForm
from .models import Task
# Create your views here.


def home(request):
    return render(request, 'home.html', {
    })


def signup(request):
    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                # return HttpResponse('User created succesfully')
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                })

            """
            except:
                # return HttpResponse('Already exist')
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                })
            """
        else:
            # return HttpResponse('Passwords do not match')
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'Password do not match'
            })
        # print(request.POST)
        # print('obteniendo datos')

@login_required
def tasks(request):
    #tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html',{
                  'tasks': tasks,
                  'task_pending': "Task_pending"
                  })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html',{
                  'tasks': tasks
                  })

@login_required
def task_detail(request, task_id):
    #print(task_id)
    #task = Task.objects.get(pk=task_id)
    if request.method == 'GET':
        task = get_object_or_404(Task, pk = task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{
            'task' : task,
            'form': form
        })
    else:
        #print(request.POST)
        try:
            task = get_object_or_404(Task, pk = task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{
            'task' : task,
            'form': form,
            'error': "Error updating task"
            })

@login_required        
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

        # return render(request, 'signin.html', {
        #   'form': AuthenticationForm
        # })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            # print(request.POST)
            form = TaskForm(request.POST)
            # print(form)
            new_task = form.save(commit=False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valide data'
            })
        """
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
        """


"""
def helloworld(request):
    #return HttpResponse('<h1>Hello world</h1>')
    #title = 'Hello world'

    return render(request,'signup.html',{
       # 'mytitle': title
       'form' : UserCreationForm
    })
"""
