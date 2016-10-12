from django.shortcuts import render, get_object_or_404
from band_booking.models import Concert
from bookingsjef.algorithms.ticket_price import get_ticket_prices_for_scenes

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

def generator_input(request):
    context = {

    }
    return render(request, 'bookingsjef/generator_input.html', context)

def price_generator(request):
    bandname = request.POST.get('band', '')
    price = request.POST.get('price', '')
    price_generated = get_ticket_prices_for_scenes(bandname, price)
    info=[]
    for list in price_generated:
        name = list[0].scene_name
        price = list[1]

        info.append({
        'name': name,
        'price': price

        })
    context = {'info': info}
    return render(request, 'bookingsjef/generate_price.html', context)