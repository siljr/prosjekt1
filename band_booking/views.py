from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logout_user
from django.shortcuts import render, redirect, reverse

from band_booking.artist_information_collectors.artist_information import get_artist_information
from band_booking.artist_information_collectors.songkick_collector import get_past_events


def login_page(request, error=None):
    '''
    Displays the login page if the user is not logged in, else it redirects to the index page. Displays an informative
    error message if the error argument is set.
    '''
    if request.user.is_authenticated:
        return redirect('band_booking:index')
    return render(request, 'band_booking/login.html', {'error': error})


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


def artist(request, name):
    return render(request, 'band_booking/artist.html', get_artist_information(name))


def artist_load(request, name):
    return render(request, 'band_booking/loading_artist.html', {'name': name})


def event_load(request, name):
    return render(request, 'band_booking/artist_information_events.html', get_past_events(name))


def index(request):
    """
    Creates a role specific user page
    """
    pages = {
        "Bookingansvarlig": [
            {"title": "Bookingsoversikt", "link": reverse('bookingansvarlig:bookings')},
            {"title": "Tidligere konserter", "link": reverse('bookingansvarlig:concerts')},
            {"title": "Artist informasjon", "link": reverse('bookingansvarlig:search_for_artist')}
        ],
        "Bookingsjef": [
            {"title": "Tidligere konserter", "link": reverse('bookingansvarlig:concerts')},
        ],
        "Arrangør": [],
        "Tekniker": [],
    }

    if request.user.is_superuser:
        super_user_pages = []
        for user_group_pages in pages.values():
            super_user_pages += user_group_pages
        # Removes duplicate links from the admin view
        super_user_pages = list({page['link']: page for page in super_user_pages}.values())
        return render(request, "band_booking/index.html", {'pages': super_user_pages})

    user_groups = request.user.groups.all()
    user_pages = []
    for user_group in user_groups:
        if user_group.name in pages:
            user_pages += pages[user_group.name]
    return render(request, "band_booking/index.html", {'pages': user_pages})
