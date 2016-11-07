from django.shortcuts import render, reverse, redirect
from bookingsjef.actions.concert_overview_term import build_basic_information_month, django_date
from band_booking.models import Band, Concert, Booking


def concerts_band(request, year, month):
    """
    Retrieves information about bookings for the user's band and renders calendar view with this information.
    If the user does not belong to a band error page is rendered.
    """
    band = Band.get_bandmedlems_band(user=request.user)
    if band is None:
        return render(request, 'band_booking/error.html', {'error': "Du er ikke tilknyttet et band som medlem."})

    month, year = int(month), int(year)
    information = build_basic_information_month(year, month, band.band_name + " - " + str(year))

    for index, date in enumerate(information['dates']):
        concerts_date = Concert.objects.filter(date=django_date(year, month, date['date']), bands=band)
        if concerts_date:
            date['booked'] = 'booked'
            continue
        booking_offers = Booking.objects.filter(date=django_date(year, month, date['date']), recipient_email=band.manager.email)
        if booking_offers:
            date['booked'] = 'offer-sent'
            continue
        date['booked'] = 'not-booked'

    information["previous"] = reverse('bandmedlem:calendar', kwargs={'year': year - (month == 1), 'month': range(1, 13)[(month - 2) % 12]})
    information["next"] = reverse('bandmedlem:calendar', kwargs={'year': year + (month == 12), 'month': range(1, 13)[month % 12]})
    return render(request, 'bookingsjef/booking-overview-term.html', information)
