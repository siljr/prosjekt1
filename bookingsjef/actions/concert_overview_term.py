from django.utils import timezone
from django.shortcuts import reverse
from band_booking.models import Booking, Concert, Scene, Band
from calendar import monthrange


def django_date(year, month, day):
    """
    Returns date in following string format: yyyy-mm-dd based on input parameters.
    """
    return timezone.datetime.strptime(str(year) + "-" + "%02d" % month + "-" + "%02d" % day, '%Y-%m-%d')


def get_current_term():
    """
    Returns starting end ending date for the current semester.
    """
    current_date = timezone.now()
    return get_term(current_date.month, current_date.year)


def get_term(month, year):
    """
    Returns starting end ending date for the semester based on year and month.
    """
    if month <= 6:
        return django_date(year, 1, 15), django_date(year, 5, 15)
    return django_date(year, 8, 15), django_date(year, 11, 30)


def get_number_of_booking_offers_sent_this_term(scene):
    """
    Returns number of bookings for the scene in current semester.
    Args:
        scene: Scene object instance.
    """
    start_term, end_term = get_current_term()
    return len(Booking.objects.filter(date__lt=end_term, date__gt=start_term, scene__scene_name__icontains=scene))


def get_number_of_booked_dates_this_term(scene):
    """
    Returns number of concerts for the scene in current semester.
    Args:
        scene: Scene object instance.
    """
    start_term, end_term = get_current_term()
    return Concert.objects.filter(scene__scene_name__icontains=scene, date__lt=end_term, date__gt=start_term).values(
        'date').distinct().count()


def get_number_of_unbooked_dates_this_term(scene):
    """
    Returns number of unbooked_dates for the scene in current semester.
    Args:
        scene: Scene object instance.
    """
    start_term, end_term = get_current_term()
    return (end_term - start_term).days - get_number_of_booked_dates_this_term(scene)


def get_information_this_term():
    """
    Returns information in JSON format about bookings for every scene in current semester.
    Renders calendar html page with this information for every scene.
    """
    term = get_current_term()
    return {
        'scenes': [{
                       'name': scene[1].title(),
                       'booked': get_number_of_booked_dates_this_term(scene[1]),
                       'unbooked': get_number_of_unbooked_dates_this_term(scene[1]),
                       'offers': get_number_of_booking_offers_sent_this_term(scene[1]),
                       'calendar': reverse('bookingsjef:calendar',
                                           kwargs={'year': term[0].year, 'month': term[0].month, 'scene': scene[1]})
                   } for scene in Scene.SCENE_CHOICES],
    }


def build_basic_information_month(year, month, scene):
    """
    Returns JSON with basic information about days in month and scene based on input parameters.
    """
    start, days_in_month = monthrange(year, month)
    return {
        'scene': scene[0].upper() + scene[1:],
        'empty_dates': list(range(start)),
        'empty_dates_end': list(range(6 - (start + days_in_month - 1) % 7)),
        'dates': [{'date': date + 1} for date in range(days_in_month)],
        'month':
            ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November",
             "Desember"][month - 1],
    }


def build_information_month(year, month, scene):
    """
    Returns JSON with detailed booking information for the given scene and month based on input parameters.
    Renders calendar html page with this information and includes it in JSON.
    """
    information = build_basic_information_month(year, month, scene)
    term = get_term(month, year)

    for index, date in enumerate(information['dates']):
        concerts_date = Concert.objects.filter(date=django_date(year, month, date['date']),
                                               scene__scene_name__icontains=scene)
        if concerts_date:
            date['booked'] = 'booked'
            date['band'] = concerts_date[0].bands.all()[0].band_name
            continue
        booking_offers = Booking.objects.filter(date=django_date(year, month, date['date']),
                                                scene__scene_name__icontains=scene)
        if booking_offers:
            date['booked'] = 'offer-sent'
            try:
                date['band'] = Band.objects.filter(manager__email=booking_offers[0].recipient_email)[:1].get().band_name
            except Band.DoesNotExist:
                date['email'] = booking_offers[0].recipient_email
            continue
        if [month, date['date']] < [term[0].month, term[0].day] or [month, date['date']] > [term[1].month, term[1].day]:
            date['greyed'] = True
        date['booked'] = 'not-booked'
    if term[0].month != month:
        information["previous"] = reverse('bookingsjef:calendar',
                                          kwargs={'year': year, 'month': month - 1, 'scene': scene})
    if term[1].month != month:
        information["next"] = reverse('bookingsjef:calendar', kwargs={'year': year, 'month': month + 1, 'scene': scene})
    return information
