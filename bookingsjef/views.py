from django.shortcuts import render, get_object_or_404, redirect
from band_booking.models import Concert, Booking
from .actions.concert_overview_term import get_information_this_term


def economic_result_concert(request, concert_id):
    concert = get_object_or_404(Concert, pk=concert_id)
    context = {
        'title': concert.concert_title,
        'date': concert.date.strftime('%d.%m.%Y'),
        'attendance': concert.attendance,
        'bands': [band.band_name for band in concert.bands.all()],
        'economic_result': '%.2f kr' % concert.economic_result,
        'expenses': {
            'Guards': '%.2f kr' % concert.GUARD_EXPENSE,
            'Drift scene': '%.2f kr' % concert.scene.expenditure,
            'Band': '%.2f kr' % concert.booking_price,
        },
        'income': {
            'Tickets': '%.2f kr' % (concert.ticket_price * concert.attendance),
        },
    }
    return render(request, 'bookingsjef/economic_result.html', context)


def approve_booking_offer(request, offer_id, approved=False):
    try:
        offer = Booking.objects.get(pk=offer_id)
        if offer.status not in [Booking.UNDECIDED, Booking.NOT_APPROVED]:
            return redirect('bookingansvarlig:bookings')
        if not approved:
            offer.change_status(Booking.NOT_APPROVED)
        else:
            offer.change_status(Booking.APPROVED)
        offer.save()
        return redirect('bookingansvarlig:bookings')
    except Booking.DoesNotExist:
        print('does not exist')
        return redirect('bookingansvarlig:bookings')


def booking_information_term(request):
    return render(request, "bookingsjef/booking_information_term.html", get_information_this_term())
