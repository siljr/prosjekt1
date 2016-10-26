from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

from band_booking.forms import ChangeTechnicalneedsForm

# Create your views here.
def ChangeTechnicalneed(request):
    if request.method == 'POST':
        form = ChangeTechnicalneedsForm(request.POST)
        if form.is_valid():
            form.save
            # hvis dette fungerer går jeg tilbake til listen over behov.. Kanskje
            return HttpResponseRedirect(reverse('changeNeeds'))
    else:
        form = ChangeTechnicalneedsForm()

    context = {'form': form}

    return render(request, 'manager/technicalneeds.html', context=context)
