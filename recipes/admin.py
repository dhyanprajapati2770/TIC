from django.contrib import admin

# Register your models here.

from .models import recipes,requestrecipe

admin.site.register(recipes)
admin.site.register(requestrecipe)