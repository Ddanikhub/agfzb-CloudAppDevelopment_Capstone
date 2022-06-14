from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model=CarModel
    extra=3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display=["car_Make", "name", "dealerID", "car_model_choices", "year"]  

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display=["name", "description"]
    inlines=[CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
