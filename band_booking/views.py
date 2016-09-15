from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    return render(request, 'band_booking/login.html')


def login_authenticate(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        pass
    else:
        return redirect('login')


def logout_logic(request):
    logout(request)
    return redirect('login', {})

