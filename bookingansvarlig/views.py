from django.views import generic
from band_booking.models import Scene, Concert, Booking
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re


def get_queries(request_method, queries, default=None):
    return [request_method.get(query, default) for query in queries]


def concert(request):
    def build_concert(concert):
        """
        :param concert: The concert object to build information about
        :return: A dictionary of information about the given concert
        """
        return {
            'pk': concert.pk,
            'name': concert.concert_title,
            'bands': [band.band_name for band in concert.bands.all()],
            'date': concert.date.strftime("%d.%m.%Y"),
            'ticket_price': concert.ticket_price,
            'genre': list(set([band.genre for band in concert.bands.all()])),
            'attendance': concert.attendance,
            'scene': concert.scene.scene_name,
        }

    def get_genres():
        """
        Finds a list of all the genre for concerts on Samfundet
        :return: All genres to be played on Samfundet
        """
        genres = []
        for concert in Concert.objects.all():
            genres += [band.genre for band in concert.bands.all()]
        return sorted(list(set(genres)))

    concerts = Concert.objects.all()

    # Collects the required query restrictions if they exist
    band_name_query, genre_query, scene_query = get_queries(request.GET, ['band_name', 'genre', 'scene'], '')

    # Finds all concerts that fulfill the search parameters
    filtered_concerts = []
    for concert in concerts.filter(scene__scene_name__icontains=scene_query, date__lte=timezone.now()).order_by('-date'):
        # Check if a band with the given band name exists in the query
        queryset_list_name = concert.bands.filter(band_name__icontains=band_name_query)
        if not queryset_list_name and band_name_query != "":
            continue

        # Check if one of the bands in the concert has the given genre
        queryset_list_genre = concert.bands.filter(genre=genre_query)
        if queryset_list_genre or genre_query == "":
            filtered_concerts.append(concert)

    # Builds the context of the view
    context = {
        'genres': get_genres(),
        'concerts': [build_concert(concert) for concert in filtered_concerts],
        'genre': genre_query,
        'scene': scene_query,
        'band_name': band_name_query,
        'scenes': [scene.scene_name for scene in Scene.objects.all()]
    }

    return render(request, 'bookingansvarlig/concert_scene.html', context)


def update_booking_offer(request, offer_id=None):
    """
    Updates the booking offer with the given ID, if no ID a new booking offer is created instead.
    Also creates a new booking offer if the user does not have permissions to edit the current booking offer
    :param request: The HTTP request
    :param offer_id: The id of the offer if the offer has an id
    :return: A redirect to the edit page
    """
    def create_new_offer(title, email, text, user, date, scene):
        """
        :param title: The title of the booking offer
        :param email: The recipient email address of the booking offer
        :param text: The booking offer text
        :param user: The user creating the offer
        :param date: The date of the offered concert
        :param scene: The scene of the offered concert
        :return: A redirect to the offer editing page
        """
        new_booking_offer = Booking(sender=user, title_name=title, recipient_email=email, email_text=text, date=date, scene=Scene.objects.get(scene_name__icontains=scene))
        new_booking_offer.save()
        request.session['saved-offer'] = True
        return redirect('bookingansvarlig:create_booking_offer', offer_id=new_booking_offer.pk)

    # Collect the POST request
    title, text, recipient_email, date, scene = get_queries(request.POST, ['title', 'message', 'email', 'date', 'scene'])
    # If one of the three fields are not set, then we return the user to the create booking offer view, as the HTML
    # requires the user to fill in all three fields.
    if title is None or text is None or recipient_email is None or date is None or scene is None:
        return redirect('bookingansvarlig:create_booking_offer')

    # Checks if the email is in a valid format, if not the user is returned
    # to the offer creation page with an error message
    try:
        validators.validate_email(recipient_email)
    except ValidationError:
        context = {'link': reverse('bookingansvarlig:update_booking_offer'),
                   'offer': {'title_name': title, 'recipient_email': recipient_email},
                   'error': "Email is not valid",
                   'email_text': text,
                   'date': date,
                   'scene': scene,
                   }
        if offer_id is not None:
            context['link'] = reverse('bookingansvarlig:update_booking_offer', kwargs={'offer_id': offer_id})
        return render(request, 'bookingansvarlig/create_booking_offer.html', context)

    # If no offer ID is given, then we create a new booking offer
    if offer_id is None:
        return create_new_offer(title, recipient_email, text, request.user, date, scene)

    try:
        # Find the booking offer
        booking_offer = Booking.objects.get(pk=offer_id)

        # If the user isn't allowed the view the booking_offer, it isn't allowed to edit it either. That is
        # a new booking offer is created instead.
        if not booking_offer.user_allowed_to_view(request.user):
            return create_new_offer(title, recipient_email, text, request.user, date, scene)

        # Update the information in the booking offer
        booking_offer.email_text = text
        booking_offer.title_name = title
        booking_offer.recipient_email = recipient_email
        booking_offer.date = date
        booking_offer.scene = Scene.objects.get(scene_name__icontains=scene)
        booking_offer.save()
        request.session['saved-offer'] = True
        return redirect('bookingansvarlig:create_booking_offer', offer_id=booking_offer.pk)

    # If no booking offer exist for the given offer ID, we create a new booking offer.
    except Booking.DoesNotExist:
        return create_new_offer(title, recipient_email, text, request.user)


def create_booking_offer(request, offer_id=None):
    """
    Either displays the information about the current booking offer
    """
    saved = request.session.pop('saved-offer', False)

    # If no offer ID is given, a new booking offer is to be created
    if offer_id is None:
        return render(request, 'bookingansvarlig/create_booking_offer.html',
                      {'link': reverse('bookingansvarlig:update_booking_offer'), 'scenes': [scene.scene_name for scene in Scene.objects.all()]})

    try:
        booking_offer = Booking.objects.get(pk=offer_id)
    except Booking.DoesNotExist:
        return redirect('band_booking:index')

    # Check if the user is allowed to view the booking offer, else redirect it the overview of the booking
    if not booking_offer.user_allowed_to_view(request.user):
        return redirect('band_booking:index')

    try:
        scene_name = booking_offer.scene.scene_name
    except ObjectDoesNotExist:
        scene_name = ""

    context = {'offer': booking_offer, 'saved': saved,
               'status': booking_offer.get_status_message(),
               'link': reverse('bookingansvarlig:update_booking_offer', kwargs={'offer_id': offer_id}),
               'email_text': booking_offer.email_text,
               'date': "%04d-%02d-%02d" % (booking_offer.date.year, booking_offer.date.month, booking_offer.date.day),
               'scene': scene_name,
               'scenes': [scene.scene_name for scene in Scene.objects.all()]
               }

    return render(request, 'bookingansvarlig/create_booking_offer.html', context)


class BookingListView(generic.ListView):
    template_name = 'bookingansvarlig/bookings_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return [booking for booking in Booking.objects.all() if booking.user_allowed_to_view(self.request.user)]


# Makes a page with just the filtered view of just the status sent
class BookingFilteredListView(generic.ListView):
    template_name = 'bookingansvarlig/bookings_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return [booking for booking in Booking.objects.filter(status="S") if booking.user_allowed_to_view(self.request.user)]


def search_for_artist(request):
    artist_name = request.GET.get('name', None)
    if artist_name is None or artist_name == "":
        return render(request, 'bookingansvarlig/search_artist.html', {})
    if re.match("^[A-Za-z0-9 ]+$", artist_name):
        return redirect('band_booking:artist_load', name=artist_name)
    return render(request, 'bookingansvarlig/search_artist.html', {'name': artist_name, 'error': 'Artist navnet inneholder karakterer som ikke er støttet. Støttede karakterer er mellomrom, bokstavene fra A til Z og tall'})
