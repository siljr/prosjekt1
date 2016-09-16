from django.contrib import admin
from .models import Scene, Band, Concert

# Register your models here.

admin.site.register(Scene)
admin.site.register(Band)
admin.site.register(Concert)