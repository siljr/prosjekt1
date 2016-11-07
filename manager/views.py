from django.shortcuts import render, redirect, reverse
from band_booking.models import Technical_needs, Band
from band_booking.forms import ChangeTechnicalneedsForm


def changeTechnicalneed(request):
    """
    Renders page for changing technical needs of the manager's band.
    """
    if request.method == 'POST':
        form = ChangeTechnicalneedsForm(request.POST)
        if form.is_valid():
            technical_need = form.save(commit=False)
            try:
                band = Band.objects.filter(manager=request.user)[:1].get()
                technical_need.band = band
            except Band.DoesNotExist:
                return redirect(reverse('band_booking:index'))
            # hvis dette fungerer går jeg tilbake til listen over behov.. Kanskje
            # return HttpResponseRedirect(reverse('changeNeeds'))
            technical_need.save()
            return redirect(reverse('manager:technical_requirements'))

    else:
        form = ChangeTechnicalneedsForm()

    context = {'form': form}

    return render(request, 'manager/technicalneeds.html', context=context)


def technical_requirements(request):
    """
    Renders page with technical requirements information for the user's band.
    """
    try:
        band = Band.objects.get(manager=request.user)
    except Band.DoesNotExist:
        return render(request, 'band_booking/error.html', {'error': "Du er ikke tilknyttet et band som manager."})
    equipment = Technical_needs.objects.filter(band=band)
    equipment_information = []
    for current_equipment in equipment:
        equipment_information.append({
            'pk': current_equipment.pk,
            'name': current_equipment.equipment_name,
            'number': current_equipment.amount,
        })
    return render(request, 'manager/equipment_collection.html', {'equipmentCollection': equipment_information,
                                                                 'band': band})


def update_technical_requirements(request):
    """
    Deletes technical requirement based on request data.
    Renders page with updated list of requirements for the manager's (user's) band
    """
    equipment_number = request.POST.getlist('equipment_number')
    equipment_pk = request.POST.getlist('pk')
    equipment_name = request.POST.getlist('equipment_name')
    delete = request.POST.getlist('delete')
    for index in range(len(equipment_number)):
        try:
            equipment = Technical_needs.objects.get(pk=equipment_pk[index])
            if equipment.band.manager != request.user:
                continue
            if delete[index] == '1':
                equipment.delete()
                continue
            if int(equipment_number[index]) < 1 or len(equipment_name[index]) < 1:
                continue
            equipment.equipment_name = equipment_name[index]
            equipment.amount = int(equipment_number[index])
            equipment.save()
        except Technical_needs.DoesNotExist:
            continue
    return redirect('manager:technical_requirements')
