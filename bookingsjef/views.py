from django.shortcuts import render, get_object_or_404, redirect
from band_booking.models import Concert, Booking
from .actions.concert_overview_term import get_information_this_term, build_information_month
from bookingsjef.algorithms.ticket_price import get_ticket_prices_for_scenes
from django.http import HttpResponse


def economic_result_concert(request, concert_id):
    """
    Renders a page with economic results of the concert
    """
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
    """
    Changes booking status to APPROVED.
    """
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


def calendar(request, year, month, scene):
    """
    Renders calendar page with booking overview for the month and scene based on input parameter.
    """
    return render(request, "bookingsjef/booking-overview-term.html", build_information_month(int(year), int(month), scene))


def booking_information_term(request):
    """
    Renders page with booking information for the current semester.
    """
    return render(request, "bookingsjef/booking_information_term.html", get_information_this_term())


def generator_input(request):
    """
    Renders page that allow the user to generate ticket prices for specific band and booking price.
    """
    context = {

    }
    return render(request, 'bookingsjef/generator_input.html', context)


def price_generator(request):
    """
    Generates band prices for all the scenes
    """
    bandname = request.POST.get('band', '')
    price = int(request.POST.get('price', ''))
    price_generated = get_ticket_prices_for_scenes(bandname, price)
    info = []
    try:
        for list in price_generated:
            name = list[0].scene_name
            price = list[1]

            info.append({
                'name': name,
                'price': price

            })
        context = {
            'info': info,
        }
        return render(request, 'bookingsjef/generate_price.html', context)
    except TypeError:
        return HttpResponse('Bandet eksisterer ikke i våre databaser')
