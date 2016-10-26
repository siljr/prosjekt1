from django.utils import timezone
from django.shortcuts import reverse
from band_booking.models import Booking, Concert, Scene
from calendar import monthrange


def django_date(year, month, day):
    return timezone.datetime.strptime(str(year) + "-" + "%02d" % month + "-" + "%02d" % day, '%Y-%m-%d')


def get_current_term():
    current_date = timezone.now()
    return get_term(current_date.month, current_date.year)


def get_term(month, year):
    if month <= 6:
        return django_date(year, 1, 15), django_date(year, 5, 15)
    return django_date(year, 8, 15), django_date(year, 11, 30)


def get_number_of_booking_offers_sent_this_term(scene):
    start_term, end_term = get_current_term()
    return len(Booking.objects.filter(date__lt=end_term, date__gt=start_term, scene__scene_name__icontains=scene))


def get_number_of_booked_dates_this_term(scene):
    start_term, end_term = get_current_term()
    return Concert.objects.filter(scene__scene_name__icontains=scene, date__lt=end_term, date__gt=start_term).values('date').distinct().count()


def get_number_of_unbooked_dates_this_term(scene):
    start_term, end_term = get_current_term()
    return (end_term - start_term).days - get_number_of_booked_dates_this_term(scene)


def get_information_this_term():
    term = get_current_term()
    return {
        'scenes': [{
            'name': scene[1].title(),
            'booked': get_number_of_booked_dates_this_term(scene[1]),
            'unbooked': get_number_of_unbooked_dates_this_term(scene[1]),
            'offers': get_number_of_booking_offers_sent_this_term(scene[1]),
            'calendar': reverse('bookingsjef:calendar', kwargs={'year': term[0].year, 'month': term[0].month, 'scene': scene[1]})
        } for scene in Scene.SCENE_CHOICES],
    }


def build_information_month(year, month, scene):
    start, days_in_month = monthrange(year, month)
    term = get_term(month, year)
    information = {
        'scene': scene[0].upper() + scene[1:],
        'empty_dates': list(range(start)),
        'empty_dates_end': list(range(7 - (start + days_in_month) % 7)),
        'dates': [{'date': date + 1} for date in range(days_in_month)],
        'month': ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"][month-1],
    }

    remove = []
    for index, date in enumerate(information['dates']):
        concerts_date = Concert.objects.filter(date=django_date(year, month, date['date']), scene__scene_name__icontains=scene)
        if concerts_date:
            date['booked'] = 'booked'
            date['band'] = concerts_date[0].bands.all()[0].band_name
            continue
        booking_offers = Booking.objects.filter(date=django_date(year, month, date['date']), scene__scene_name__icontains=scene)
        if booking_offers:
            date['booked'] = 'offer-sent'
            continue
        if [month, date['date']] < [term[0].month, term[0].day]:
            remove.append(index)
            information['empty_dates'].append(0)
        if [month, date['date']] > [term[1].month, term[1].day]:
            remove.append(index)
            information['empty_dates_end'].append(0)
        date['booked'] = 'not-booked'
    for index in remove[::-1]:
        del information['dates'][index]
    if term[0].month != month:
        information["previous"] = reverse('bookingsjef:calendar', kwargs={'year': year, 'month': month - 1, 'scene': scene})
    if term[1].month != month:
        information["next"] = reverse('bookingsjef:calendar', kwargs={'year': year, 'month': month + 1, 'scene': scene})
    return information

