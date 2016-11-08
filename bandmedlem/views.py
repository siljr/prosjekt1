from django.shortcuts import render, reverse, redirect
from bookingsjef.actions.concert_overview_term import build_basic_information_month, django_date
from band_booking.models import Band, Concert, Booking
from datetime import datetime


def band_offers(request):
    band = Band.get_users_band(request.user)
    if not band:
        return render(request, 'band_booking/error.html', {'error': 'Du er ikke medlem av noe band'})
    bookings = band.get_band_manager_bookings().filter(date__gte=datetime.now())
    if bookings:
        return render(request, 'bandmedlem/view_for_offers.html', {'bookings': bookings, 'band': band})
    return render(request, 'band_booking/error.html', {'error': 'Ditt band har ikke noen bookingtilbud'})


def concerts_band(request, year, month):
    """
    :param request: The HTTP request
    :param year: The year to view
    :param month: The month to view
    :return: A rendering of the calendar page
    """
    band = Band.get_users_band(user=request.user)
    # Check if the user is a member of a band
    if band is None:
        return render(request, 'band_booking/error.html', {'error': "Du er ikke medlem av et band"})

    # Find the basic information for the given concert
    month, year = int(month), int(year)
    information = build_basic_information_month(year, month, band.band_name + " - " + str(year))

    # Fill dates with information
    for index, date in enumerate(information['dates']):
        concerts_date = Concert.objects.filter(date=django_date(year, month, date['date']), bands=band)
        # Set if concert for date
        if concerts_date:
            date['booked'] = 'booked'
            continue

        booking_offers = Booking.objects.filter(date=django_date(year, month, date['date']), recipient_email=band.manager.email, status='S')
        # Set if booking offer sent for date
        if booking_offers:
            date['booked'] = 'offer-sent'
            continue
        date['booked'] = 'not-booked'

    # Find next and previous month
    information["previous"] = reverse('bandmedlem:calendar', kwargs={'year': year - (month == 1), 'month': range(1, 13)[(month - 2) % 12]})
    information["next"] = reverse('bandmedlem:calendar', kwargs={'year': year + (month == 12), 'month': range(1, 13)[month % 12]})
    return render(request, 'bookingsjef/booking-overview-term.html', information)