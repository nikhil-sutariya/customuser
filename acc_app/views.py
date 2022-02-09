from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserAdminCreationForm

def index(request):
    return render(request, 'index.html')

def login_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(email,'-----',password)
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def signup(request):
    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'signup.html', {'form': form})
