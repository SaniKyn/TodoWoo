from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'from': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'from': UserCreationForm(),
                               'error': 'Такой пользователь существует. Пожалуйста задайте новое значение.'})
        else:
            return render(request, 'todo/signupuser.html',
                          {'from': UserCreationForm(), 'error': 'Пароль не совпадал'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'from': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'from': AuthenticationForm(), 'error': 'Неверный логин или пароль'})
        else:
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'from': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'from': TodoForm(), 'error': 'Пераданые неверные данные'})


def currenttodos(request):
    todos = {
        'todos': Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    }
    return render(request, 'todo/currenttodos.html', todos)
