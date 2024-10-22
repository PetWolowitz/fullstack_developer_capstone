# from django.contrib import admin
# from .models import related models


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
# djangoapp/admin.py

from django.contrib import admin
from .models import CarMake, CarModel

# Registra i modelli
admin.site.register(CarMake)
admin.site.register(CarModel)
