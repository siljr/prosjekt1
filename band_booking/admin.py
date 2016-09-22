from django.contrib import admin
from .models import Person, Scene, Band, Album, Concert

# Register your models here.


admin.site.register(Person)
admin.site.register(Scene)
admin.site.register(Band)
admin.site.register(Album)
admin.site.register(Concert)
