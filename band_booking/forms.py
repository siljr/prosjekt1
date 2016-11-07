from django import forms
from .models import Technical_needs, Band, Concert, User


class ChangeTechnicalneedsForm(forms.ModelForm):
    # henter modellen og har nå alle feltene, husk at man må importere den i toppen for å ha tilgang
    class Meta:
        model = Technical_needs
        # må alltid ha en include eller en exclude, den kan være tom
        exclude = ['band']


class CreateBandForm(forms.ModelForm):
    """
    A form for creation of bands
    """
    def __init__(self, *args, **kwargs):
        """
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: An instance
        Creates an instance with restrictions to the managers that are not already managers for bands
        """
        super(CreateBandForm, self).__init__(*args, **kwargs)
        if self.instance:
            managers = User.objects.all().filter(groups__name='Manager')
            select_able_managers = []
            for manager in managers:
                try:
                    Band.objects.get(manager=manager)
                except Band.DoesNotExist:
                    select_able_managers.append((manager.pk, manager))
            self.fields['manager'].widget.choices = select_able_managers

    class Meta:
        model = Band
        exclude = ['band_member', 'booking_price', 'streaming_numbers']


class CreateConcertForm(forms.ModelForm):
    """
    A form for creation of concerts
    """
    class Meta:
        model = Concert
        exclude = ['personnel', 'attendance', 'organizer', 'status']
