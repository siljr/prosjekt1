from django.shortcuts import render, get_object_or_404, redirect, reverse
from band_booking.models import Concert, Booking, Scene
from .actions.concert_overview_term import get_information_this_term, build_information_month
from bookingsjef.algorithms.ticket_price import get_ticket_prices_for_scenes
from django.http import HttpResponse
from band_booking.forms import CreateBandForm, CreateConcertForm
from datetime import datetime


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


def calendar(request, year, month, scene):
    return render(request, "bookingsjef/booking-overview-term.html", build_information_month(int(year), int(month), scene))


def booking_information_term(request):
    return render(request, "bookingsjef/booking_information_term.html", get_information_this_term())


def generator_input(request):
    context = {

    }
    return render(request, 'bookingsjef/generator_input.html', context)


def price_generator(request):
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


def create_concert(request, date=None, scene=None):
    """
    :param request: The HTTP request
    :param date: The date
    :param scene: The scene
    :return: A redirect or render depending on the validity of the form
    """
    if request.method == 'POST':
        form = CreateConcertForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            form.save()
            return redirect(reverse('bookingsjef:booking_information_term'))
        return render(request, 'bookingsjef/create_concert.html', context={'form': form})

    # Try selecting a valid scene
    if scene:
        try:
            scene = Scene.objects.get(scene_name__icontains=scene)
        except Scene.DoesNotExist:
            scene = None

    # Create the context of the request
    context = {'form': CreateConcertForm(initial={'date': (date or datetime.now()), 'scene': scene})}
    return render(request, 'bookingsjef/create_concert.html', context=context)


def create_band(request):
    """
    :param request: The HTTP request
    :return: A redirect to an error page if there are no available managers or to the concert creation page if the form is correct.
            Else a render of the creation page
    """
    if request.method == 'POST':
        form = CreateBandForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            form.save()
            return redirect(request.POST.get('url'))

    # Create the context of the request
    context = {'form': CreateBandForm(request.POST), 'url': (request.POST.get('url') or reverse('bookingsjef:create_concert'))}

    # Check if there are any choices of managers
    if not context['form'].fields['manager'].widget.choices:
        return render(request, 'band_booking/error.html', {'error': "Ingen ledige managers i systemet. Kontakt system administratoren for å få registrert nye managers"})
    return render(request, 'bookingsjef/create_band.html', context=context)
