from django.shortcuts import render, redirect
from band_booking.models import Technical_needs, Band
# Create your views here.


def technical_requirements(request):
    try:
        band = Band.objects.get(manager=request.user)
    except Band.DoesNotExist:
        # TODO: Add error message
        return redirect('band_booking:index')
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
            equipment.Equipment_name = equipment_name[index]
            equipment.amount = int(equipment_number[index])
            equipment.save()
        except Technical_needs.DoesNotExist:
            continue
    return redirect('manager:technical_requirements')
