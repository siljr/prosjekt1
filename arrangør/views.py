from django.shortcuts import render, redirect
from django.views import generic
from band_booking.models import Concert, Technical_needs


# Create your views here.

class ConcertsView(generic.ListView):
    template_name = 'arrangør/concert_overview.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        concerts = Concert.objects.filter(date__range=["2016-08-16", "2016-11-28"])
        return concerts


def overview_concert(request, id):
    """
    Returns an overview page for the concert of the given ID. If there is no concert with this ID or the user does not
    have the necessary requirements to view the page the user will be redirected to the concert_overview page.
    """

    def build_equipment(concert):
        """
        Finds the amount of equipment needed for all the bands of the concert, especially it combines the requirements
        with same names such that it is easier for the user to read through the list
        """
        equipment = {}
        for band in concert.bands.all():
            # Find equipment needed by the given band
            band_equipment = Technical_needs.objects.filter(band=band)
            for current_equipment in band_equipment:
                # Combine the needs of similar equipment for different bands
                if current_equipment.equipment_name in equipment:
                    equipment[current_equipment.equipment_name] += current_equipment.amount
                else:
                    equipment[current_equipment.equipment_name] = current_equipment.amount
        return equipment

    # Try to find a concert with the given ID
    try:
        concert = Concert.objects.get(pk=id)
    except Concert.DoesNotExist:
        return redirect('arrangør:concerts')

    # Check if user is allowed to view the given concert
    if not request.user.is_superuser and request.user != concert.organizer:
        return redirect('arrangør:concerts')

    # Render the page
    return render(request, 'arrangør/concert.html', {'concert': concert, 'equipment': build_equipment(concert)})
