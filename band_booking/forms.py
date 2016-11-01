from django import forms
from .models import Technical_needs

class ChangeTechnicalneedsForm(forms.ModelForm):
    # henter modellen og har nå alle feltene, husk at man må importere den i toppen for å ha tilgang
    class Meta:
        model = Technical_needs
        # må alltid ha en include eller en exclude, den kan være tom
        exclude = ['band']

