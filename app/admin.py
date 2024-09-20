from django.contrib import admin
from .models import Melody, Tab, Image, URL, Type

# Register your models here.
admin.site.register(Melody)
admin.site.register(Tab)
admin.site.register(Image)
admin.site.register(URL)
admin.site.register(Type)
