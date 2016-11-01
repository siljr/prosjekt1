from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from band_booking.models import Band

from band_booking.forms import ChangeTechnicalneedsForm

# Create your views here.
def changeTechnicalneed(request):
    if request.method == 'POST':
        form = ChangeTechnicalneedsForm(request.POST)
        if form.is_valid():
            technical_need = form.save(commit=False)
            try:
                band = Band.objects.filter(manager=request.user)[:1].get()
                technical_need.band = band
            except Band.DoesNotExist:
                return redirect('/technical_needs/')
            # hvis dette fungerer går jeg tilbake til listen over behov.. Kanskje
            # return HttpResponseRedirect(reverse('changeNeeds'))
            technical_need.save()
            return redirect('/technical_needs/')

    else:
        form = ChangeTechnicalneedsForm()

    context = {'form': form}

    return render(request, 'manager/technicalneeds.html', context=context)
