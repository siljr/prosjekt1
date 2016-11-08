from django.shortcuts import render, redirect
from django.views import generic
from band_booking.models import Concert, Technical_needs
from bookingsjef.actions.concert_overview_term import get_current_term


# Create your views here.

class ConcertsView(generic.ListView):
    """
    Generates a view for the query set of the current term
    """
    template_name = 'arrangør/concert_overview.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        """
        :return: The concerts of the current term
        """
        start_term, end_term = get_current_term()
        concerts = Concert.objects.filter(date__range=[start_term, end_term])
        return concerts


def overview_concert(request, id):
    """
    :param request: The HTTP request
    :param id: The id of the concert
    :return: An overview page for the given concert, if the user has the required permissions. Else a redirect.

    Returns an overview page for the concert of the given ID. If there is no concert with this ID or the user does not
    have the necessary requirements to view the page the user will be redirected to the concert_overview page.
    """

    def build_equipment(concert):
        """
        Finds the amount of equipment needed for all the bands of the concert, especially it combines the requirements
        with the same names such that it is easier for the user to read through the list
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
