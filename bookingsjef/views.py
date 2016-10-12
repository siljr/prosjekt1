from django.shortcuts import render, get_object_or_404
from band_booking.models import Concert, Scene


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

def generator_input(request):
    context = {

    }
    return render(request, 'bookingsjef/generator_input.html', context)

#def price_generator(request, Scene):
    #context = {
        #'scene_name' = [Scene.scene_name for Scene.objects.all()],
        #'scene_size' = [Scene.expenditure for Scene.objects.all()]
    #}