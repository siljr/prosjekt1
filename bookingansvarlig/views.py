from django.views import generic
from band_booking.models import Scene, Concert, Band, Booking
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError


class ScenesListView(generic.ListView):
    """
    Retrieves list of all the scenes from database (ordered by scene_name) and renders scenes page.
    """
    template_name = 'bookingansvarlig/scenes_list.html'
    context_object_name = 'scenes_list'

    def get_queryset(self):
        scenes = Scene.objects.order_by('scene_name')
        return scenes


def concert(request):
    def build_concert(concert):
        """
        Builds the information about a concert from the concert model
        """
        return {
            'pk': concert.pk,
            'name': concert.concert_title,
            'bands': [band.band_name for band in concert.bands.all()],
            'date': concert.date.strftime("%d.%m.%Y"),
            'ticket_price': concert.ticket_price,
            'genre': [band.genre for band in concert.bands.all()],
            'attendance': concert.attendance,
            'scene': concert.scene.scene_name,
        }

    def get_genres(concerts):
        """
        Finds all possible genres from bands that have played at Samfundet
        """
        genres = []
        for concert in concerts:
            for band in concert.bands.all():
                if band.genre not in genres:
                    genres.append(band.genre)
        return genres

    concerts = Concert.objects.all()

    # Adds the search functions
    band_name_query, genre_query, scene_query = request.GET.get('band_name', ''), request.GET.get('genre', ''), request.GET.get('scene', '')
    filtered_concerts = []
    for concert in concerts.filter(scene__scene_name__icontains=scene_query).filter(date__lte=timezone.now()).order_by('-date'):
        queryset_list_name = concert.bands.filter(band_name__icontains=band_name_query)
        if not queryset_list_name and band_name_query != "":
            continue
        queryset_list_genre = concert.bands.filter(genre__icontains=genre_query)
        if queryset_list_genre or genre_query == "":
            filtered_concerts.append(concert)

    context = {
        'genres': get_genres(concerts),
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
    """

    def create_new_offer(title, email, text, user):
        """
        Creates a new booking offer given the title, email, text and user.
        """
        new_booking_offer = Booking(sender=user, title_name=title, recipient_email=email, email_text=text)
        new_booking_offer.save()
        request.session['saved-offer'] = True
        return redirect('bookingansvarlig:create_booking_offer', offer_id=new_booking_offer.pk)

    title, text, recipient_email = request.POST.get('title'), request.POST.get('message'), request.POST.get('email')

    # If one of the three fields are not set, then we return the user to the create booking offer view, as the HTML
    # requires the user to fill in all three fields.
    if title is None or text is None or recipient_email is None:
        return redirect('bookingansvarlig:create_booking_offer')

    # Checks if the email is in a valid format, if not the user is returned
    # to the offer creation page with an error message
    try:
        validators.validate_email(recipient_email)
    except ValidationError:
        context = {'link': reverse('bookingansvarlig:update_booking_offer'),
                   'offer': {'title_name': title, 'recipient_email': recipient_email, 'email_text': text},
                   'error': "Email is not valid",
                   }
        if offer_id is not None:
            context['link'] = reverse('bookingansvarlig:update_booking_offer', kwargs={'offer_id': offer_id})
        return render(request, 'bookingansvarlig/create_booking_offer.html', context)

    # If no offer ID is given, then we create a new booking offer
    if offer_id is None:
        return create_new_offer(title, recipient_email, text, request.user)

    try:
        # Find the booking offer
        booking_offer = Booking.objects.get(pk=offer_id)

        # If the user isn't allowed the view the booking_offer, it isn't allowed to edit it either. That is
        # a new booking offer is created instead.
        if not booking_offer.user_allowed_to_view(request.user):
            return create_new_offer(title, recipient_email, text, request.user)

        # Update the information in the booking offer
        booking_offer.email_text = text
        booking_offer.title_name = title
        booking_offer.recipient_email = recipient_email
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
                      {'link': reverse('bookingansvarlig:update_booking_offer')})

    try:
        booking_offer = Booking.objects.get(pk=offer_id)
    except Booking.DoesNotExist:
        return redirect('band_booking:index')

    # Check if the user is allowed to view the booking offer, else redirect it the overview of the booking
    if not booking_offer.user_allowed_to_view(request.user):
        return redirect('band_booking:index')

    context = {'offer': booking_offer, 'saved': saved,
               'status': booking_offer.get_status_message(),
               'link': reverse('bookingansvarlig:update_booking_offer', kwargs={'offer_id': offer_id}),
               }

    return render(request, 'bookingansvarlig/create_booking_offer.html', context)
