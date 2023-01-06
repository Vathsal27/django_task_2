from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        return render(request, "userAuth/home.html")
    else:
        return redirect("login")

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.warning(request, "Login Failed due to invalid credentials")
            return render(request, 'userAuth/login.html')
    return render(request, 'userAuth/login.html')

def logoutUser(request):
    logout(request)
    return redirect ("login")

def registerUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username = username).exists():
            messages.warning(request, "User exists")
            return redirect("register")
        else:
            if password1 == password2 and len(username)>3 and len(email)>4:
                user = User.objects.create_user(username = username, email = email, password = password1)
                user.save()
                messages.success(request, 'User registration successful!')
                return redirect("login")
            else:
                messages.warning(request, 'Registration failed due to invalid credentials!')
                return redirect("register")
    return render(request, 'userAuth/register.html')