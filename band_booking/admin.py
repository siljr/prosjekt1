from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Scene)
admin.site.register(Concert)
admin.site.register(Band)
admin.site.register(Booking)
admin.site.register(Technical_needs)

