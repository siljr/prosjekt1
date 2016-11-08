from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logout_user
from django.shortcuts import render, redirect, reverse
from datetime import datetime

from band_booking.artist_information_collectors.artist_information import get_artist_information
from band_booking.artist_information_collectors.songkick_collector import get_past_events


def login_page(request, error=None):
    """
    :param request: The HTTP request
    :param error: Any possible error code
    :return: A render of the login view or if the user is already logged in a redirect to the index page.
    """
    if request.user.is_authenticated:
        return redirect('band_booking:index')
    return render(request, 'band_booking/login.html', {'error': error})


def login_authenticate(request):
    """
    :param request: The HTTP request
    :return: A redirect to either the index page or the login page based on if the the login was successful.
    Authenticates the user and login if the username and password are correct, else the user is redirected to the login
    page with an error
    """
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('band_booking:index')
    else:
        return redirect('login/error')


def logout(request):
    """
    :param request: The HTTP request
    :return: A redirect to the login page
    Logs the user out.
    """
    logout_user(request)
    return redirect('band_booking:login')


def artist(request, name):
    """
    :param request: The HTTP request
    :param name: The name of the artist to search for
    :return: The artist information page for the given artist
    Retrieves artist information and renders page with this information
    """
    return render(request, 'band_booking/artist.html', get_artist_information(name))


def artist_load(request, name):
    """
    :param request: The HTTP request
    :param name: The name of the artist to search for
    :return: A loading page for searching for the given artist
    Renders loading page while artist information is retrieved
    """
    return render(request, 'band_booking/loading_artist.html', {'name': name})


def event_load(request, name):
    """
    :param request: The HTTP request
    :param name: The name of the artist for which to find events
    :return: A page of events for the given artist
    Retrieves past events information for given artist and renders it on the page
    """
    return render(request, 'band_booking/artist_information_events.html', get_past_events(name))


def index(request):
    """
    :param request: The HTTP request
    :return: An index page based on the role of the user containing links to the pages of the given user
    Creates a role specific user index page
    """
    # The pages available to the different roles
    pages = {
        'Bookingansvarlig': [
            {'title': 'Bookingtilbud', 'link': reverse('bookingansvarlig:bookings')},
            {'title': 'Tidligere konserter', 'link': reverse('bookingansvarlig:concerts')},
            {'title': 'Artistinformasjon', 'link': reverse('bookingansvarlig:search_for_artist')},
            {'title': 'Konserter dette semesteret', 'link': reverse('arrangør:concerts')},
        ],
        'Bookingsjef': [
            {'title': 'Tidligere konserter', 'link': reverse('bookingansvarlig:concerts')},
            {'title': 'Bookingtilbud', 'link': reverse('bookingansvarlig:bookings')},
            {'title': 'Billettprisgenerator', 'link': reverse('bookingsjef:generator_input')},
            {'title': 'Bookingoversikt', 'link': reverse('bookingsjef:booking_information_term')}
        ],
        'Arrangør': [
            {'title': 'Konserter dette semesteret', 'link': reverse('arrangør:concerts')},
        ],
        'Tekniker': [
            {'title': 'Mine konserter', 'link': reverse('tekniker:myconcerts')}
        ],
        'Manager': [
            {'title': 'Utstyrsliste', 'link': reverse('manager:technical_requirements')}
        ],
        'Bandmedlem': [
            {'title': 'Konserter', 'link': reverse('bandmedlem:calendar', kwargs={'year': datetime.now().year, 'month': datetime.now().month})},
            {'title': 'Tilbud', 'link': reverse('bandmedlem:bookings')},
        ]
    }

    # If the user is a superuser it should see all the pages
    if request.user.is_superuser:
        super_user_pages = []
        for user_group_pages in pages.values():
            super_user_pages += user_group_pages
        # Removes duplicate links from the admin view
        super_user_pages = list({page['link']: page for page in super_user_pages}.values())
        return render(request, 'band_booking/index.html', {'pages': super_user_pages})

    # Finds the pages for all of the user groups of the user
    user_groups = request.user.groups.all()
    user_pages = []
    for user_group in user_groups:
        if user_group.name in pages:
            user_pages += pages[user_group.name]
    # Remove duplicates caused by users with several groups
    user_pages = list({page['link']: page for page in user_pages}.values())
    return render(request, 'band_booking/index.html', {'pages': user_pages})
