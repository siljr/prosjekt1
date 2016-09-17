from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logout_user


def login_page(request, error=None):
    '''
    Displays the login page if the user is not logged in, else it redirects to the index page. Displays an informative
    error message if the error argument is set.
    '''
    if request.user.is_authenticated:
        return redirect('band_booking:index')
    return render(request, 'band_booking/login.html', {"error": error})


def login_authenticate(request):
    '''
    Authenticates the user and login if the username and password are correct, else the user is redirected to the login
    page with an error
    '''
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('band_booking:index')
    else:
        return redirect('login/error')


def logout(request):
    '''
    Logs the user out, redirects to the login page
    '''
    logout_user(request)
    return redirect('band_booking:login')
