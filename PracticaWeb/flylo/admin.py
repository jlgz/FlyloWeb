from django.contrib import admin
from .models import Airline, Client, Flight, Aircraft, ShoppingCart, Item
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from  .models import Client

# Register your models here.

class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'client'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ClientInline, )

class AirlineInline(admin.StackedInline):
    model = Flight.airline.through
    extra = 3
class AirlineAdmin(admin.ModelAdmin):
    inlines =[AirlineInline]
class FlightAdmin(admin.ModelAdmin):
    inlines = [AirlineInline]
admin.site.register(Airline,AirlineAdmin)
admin.site.register(Flight, FlightAdmin)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Aircraft)
admin.site.register(ShoppingCart)
admin.site.register(Client)
admin.site.register(Item)
