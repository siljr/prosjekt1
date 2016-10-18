from django.utils import timezone
from band_booking.models import Booking, Concert, Scene


def django_date(year, month, day):
    return timezone.datetime.strptime(str(year) + "-" + "%02d" % month + "-" + "%02d" % day, '%Y-%m-%d')


def get_current_term():
    current_date = timezone.now()

    if current_date.month <= 6:
        return django_date(current_date.year, 1, 1), django_date(current_date.year, 6, 31)
    return django_date(current_date.year, 7, 1), django_date(current_date.year, 12, 31)


def get_number_of_booking_offers_sent_this_term():
    start_term, end_term = get_current_term()
    return len(Booking.objects.filter(date__lt=end_term, date__gt=start_term))


def get_number_of_booked_dates_this_term(scene):
    start_term, end_term = get_current_term()
    return Concert.objects.filter(scene__scene_name__icontains=scene, date__lt=end_term, date__gt=start_term).values('date').distinct().count()


def get_number_of_unbooked_dates_this_term(scene):
    start_term, end_term = get_current_term()
    return (end_term - start_term).days - get_number_of_booked_dates_this_term(scene)


def get_information_this_term():
    return {
        'booking_offers': get_number_of_booking_offers_sent_this_term(),
        'scenes': [{
            'name': scene[1].title(),
            'booked': get_number_of_booked_dates_this_term(scene[1]),
            'unbooked': get_number_of_unbooked_dates_this_term(scene[1]),
        } for scene in Scene.SCENE_CHOICES],
    }
