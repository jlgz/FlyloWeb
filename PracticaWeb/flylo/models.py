from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='client')
    money = models.IntegerField(null = True)

class Airline(models.Model):
    airline_code = models.CharField(max_length=3,null = True)
    offer_categories =  models.IntegerField(null = True) #0 economic 1bussines 2 both

    def __str__(self):
        return self.airline_code
class Aircraft(models.Model):
    aircraft_number = models.CharField(max_length=4,null = True)
    seats_bussines_id = models.CharField(max_length =100,null = True)
    seats_economic_id = models.CharField(max_length = 100,null = True)
    neconomic = models.IntegerField(null = True)
    nbussines = models.IntegerField(null = True)
    def __str__(self):
        return self.aircraft_number
class Flight(models.Model):
    flight_number = models.CharField(max_length=8,null = True)
    estimated_time_departure =  models.DateTimeField(null = True)
    estimated_time_arrival =  models.DateTimeField(null = True)
    location_departure =  models.CharField(max_length=3,null = True)
    location_arrival = models.CharField(max_length=3,null = True)
    airline = models.ManyToManyField(Airline)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    status = models.CharField(max_length=40,null = True)
    seats_bussines_free = models.CharField(max_length =100,null = True)
    seats_economic_free = models.CharField(max_length = 100,null = True)
    neconomic_free =models.IntegerField(null = True)
    nbussiness_free = models.IntegerField(null = True)
    owner = models.ForeignKey(User, null=True, blank=True)
    price = models.FloatField(default = 100, null=True)
    def setStrDate(self):
        self.strDate = str(self.estimated_time_arrival)
    def __str__(self):
        return "["+self.flight_number+"] "+ self.location_departure +"-"+ self.location_arrival + " : "+ str(self.estimated_time_departure) + " / " + str(self.estimated_time_arrival) + " ["+ self.status +"]"
    def setPrice(self):
        dt = self.estimated_time_departure.date() - datetime.now().date()
        self.update = dt.days > 0
        self.priceb = round(160.0 + 50.0 * (1-(float(self.nbussiness_free)/self.aircraft.nbussines)) +100.0*10.0 / (0.01+float(dt.days)),2)
        self.pricee = round(80.0 + 50.0 * (1-(float(self.neconomic_free)/self.aircraft.neconomic)) +  100.0*10.0 / (0.01+float(dt.days)),2)
class ShoppingCart(models.Model):
    def start(self):
        self.itemlist = []
        self.flights = []
        self.nseats = []
        self.bought = False
    def getFlights(self):
        return self.flights
    def getItems(self):
        return self.itemlist
    def buy(self):
        self.bought = True 
    def add(self,flight,seats):
        self.flights.append(flight)
        self.nseats.append(seats)
        for i in seats:
            self.itemlist.append(Item(category = i[1],seats = i[2],flight = Flight.objects.get(id=flight))) #[0] air lane
            self.itemlist[len(self.itemlist) -1].setSet(False)
    def remove(self,flight):
        ind = self.flights.index(flight)
        self.flights.pop(ind)
        self.nseats.pop(ind)
    #flights = models.CommaSeparatedIntegerField()
    #idUser = seats_economic = models.IntegerField()
    user = models.OneToOneField(Client,related_name ='shop')
class Item(models.Model):
    def setSeatsId(self):
        self.nseats = range(1, int(self.seats) + 1)

    def setSet(self,val):
        self.set = val
    category = models.CharField(max_length = 2,null = True)
    nseats = []
    flight = models.ForeignKey(Flight)
    cart = models.ForeignKey(ShoppingCart)
    bought = models.BooleanField(default= False)
    checked =models.BooleanField(default = False)
    seats = models.IntegerField(null = True)
    idseats = models.CharField(max_length = 100,default = "")
