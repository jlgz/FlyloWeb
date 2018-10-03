from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db import transaction, IntegrityError
from .models import ShoppingCart, Airline, Flight, Aircraft, Client, Item
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import FlightSerializer, AirlineSerializer, AircraftSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import detail_route, api_view, permission_classes
from rest_framework.response import Response

#from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.
#@ensure_csrf_cookie
#@login_required


def user_is_registered(user):
    return user.is_authenticated()
def index(request):
    print not request.user.is_authenticated()
    context = {
        'notlog': not request.user.is_authenticated(),
        'flights':Flight.objects.values("location_departure").distinct()
    }
    return render(request,'flylo/HLP.html', context)
def flights(request,departure):
    flights_by_departure = Flight.objects.filter(location_departure=departure)
    for f in flights_by_departure:
        f.setPrice()
    context = {
        'notlog': not request.user.is_authenticated(),
        'flights':flights_by_departure, #show flights with disponible seats
        'departure':departure,
        'c' : True,
    }
    return render(request, 'flylo/flights.html', context)
def detailFlight(request,departure,number):
    flight = Flight.objects.get(flight_number=number)
    context = {
        'flight':flight,
        'notlog': not request.user.is_authenticated()
    }
    return render(request, 'flylo/detailFlight.html', context)
def shoppingcart(request):
      s=ShoppingCart()
      s.start()
      retrn = False
      airlins = Airline.objects.all().values_list('id',flat = True)
      for key in request.POST:
            if key.startswith("checkbox"):
                    if  request.POST[key] == "return": retrn = True
                    else:
                        airlines_seats = []
                        for i  in airlins:
                            val = request.POST.get("quantity economic"+str(request.POST[key])+str(i))
                            if val != None and val != '0' and val != '':
                                airlines_seats.append((i,"e",val))
                            val = request.POST.get("quantity bussines" + str(request.POST[key]) + str(i))
                            if val != None and val != '0' and val != '':
                                airlines_seats.append((i, "b", val))
                        if len(airlines_seats) != 0:
                            s.add(request.POST[key],airlines_seats)
      request.session["selectedFligths"] = s
      if retrn:return HttpResponseRedirect(reverse('flylo:flights_r'))
      else: return HttpResponseRedirect(reverse('flylo:buy'))
@login_required
def buy(request):
    if request.user.is_authenticated():
        items = []
        try :
            s = request.user.client.shop
        except ObjectDoesNotExist:
            c = Client(money=500)
            c.user = request.user
            c.save()
            s = request.session["selectedFligths"]
            s.user = c
            s.save()
            s = c.shop
        for item in request.session["selectedFligths"].getItems():
            item.cart = s
            item.save()
        for i in s.item_set.all():
            if not i.bought:
                items.append(i)
        s = ShoppingCart()
        s.start()
    else: items=  request.session["selectedFligths"].getItems()
    context = {
        'money': request.user.client.money,
        'items': items, #pasar seats eco buss airline ect y bought == false
        'notlog': not request.user.is_authenticated()
    }
    return render(request,'flylo/buy.html',context)
@login_required
def postBuy(request):
    try:
        s = request.user.client.shop
    except ObjectDoesNotExist:
        c = Client(money=500)
        c.user = request.user
        c.save()
        s = request.session["selectedFligths"]
        s.user= c
        s.save()
        s = c.shop
        for item in request.session["selectedFligths"].getItems():
            item.cart  = s
            item.save()
    with transaction.atomic():
        cost = 0
        cond = True
        s = request.user.client.shop
        target = s.item_set.all().filter(bought=False)
        if len(target) == 0:return HttpResponseRedirect(reverse('flylo:buy'))
        for i in target:
            f = i.flight
            f.setPrice()
            if (i.category == "e"):
                price = f.pricee
            else:
                price = f.priceb
            cost += price*i.seats
            if (i.category == "b" and i.flight.nbussiness_free < i.seats)or (i.category == "e" and i.flight.neconomic_free< i.seats):
                cond = False
        if cost<= request.user.client.money and cond == True:
            c = request.user.client
            c.money -= cost
            c.save()
            for i in target:
                i.bought = True
                i.save()
                f = Flight.objects.get(id=i.flight.id)
                if i.category == "b":
                    f.nbussiness_free -= i.seats
                if i.category == "e":
                    f.neconomic_free -= i.seats
                f.save()
                return render(request, 'flylo/successBuy.html')
        else:
            return render(request, 'flylo/errorBuy.html')
def flights_r(request): #mejorar los returntrip
    try:
        flights = Flight.objects.filter(id__in=request.session["selectedFligths"].getFlights())
    except:
        flights = Flight.objects.filter(id__in=[])
    arrival = flights.values('location_arrival').distinct()
    for f in flights:
        f.setPrice()
    flights_v2 = Flight.objects.filter(location_departure__in = arrival)
    for f in flights_v2:
        f.setPrice()
    context = {
        'notlog': not request.user.is_authenticated(),
        'flights_v1':flights,
        'flights_v2': flights_v2,
        'c' : False,
    }
    return render(request, 'flylo/flights.html', context)
@login_required
def preCheckIn(request):
    try:
        s = request.user.client.shop
    except ObjectDoesNotExist:
        c = Client(money=500)
        c.user = request.user
        c.save()
        s = request.session["selectedFligths"]
        s.user = c
        s.save()
        s = c.shop
        for item in request.session["selectedFligths"].getItems():
            item.cart = s
            item.save()
    flights = []
    for i in s.item_set.all():
        if (not i.checked) and (not i.flight in flights):
            flights.append(i.flight)  # just flights, create other method
    context = {
        'notlog': not request.user.is_authenticated(),
        'flights': flights,
    }
    return render(request, 'flylo/preCheckIN.html', context)
def checkIn(request,number):
    flight = Flight.objects.get(id=number)
    s = request.user.client.shop
    it = []
    for i in s.item_set.all():
        if i.flight.id == flight.id:
            i.setSeatsId()
            it.append(i)
    context = {
        'bussinesIds':flight.seats_bussines_free.split(','),
        'economicIds':flight.seats_economic_free.split(','),
        'items': it,
        'notlog': not request.user.is_authenticated(),
        'flights': flights,
    }
    return render(request,'flylo/checkIN.html', context)
def postCheckIn(request):
    try:
        with transaction.atomic():
            for key in request.POST:
                if key.startswith("combo"):
                    if request.POST[key] == "":
                        raise IntegrityError()
                    else:
                        item = Item.objects.get(id = str(key)[5:str(key).index('X')])
                        item.idseats += request.POST[key] + ","
                        f = item.flight
                        item.checked = True
                        item.save()
                        if item.category == 'b':
                            l = f.seats_bussines_free.split(',')
                            l.remove(request.POST[key])
                            f.seats_bussines_free = ','.join(l)
                        if item.category == 'e':
                            l = f.seats_economic_free.split(',')
                            l.remove(request.POST[key])
                            f.seats_economic_free = ','.join(l)
                        f.save()
        return HttpResponseRedirect(reverse('flylo:index'))
    except IntegrityError:
        return HttpResponseRedirect(reverse('flylo:index'))
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/flylo")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
def comparator(request,ips):
    flights = Flight.objects.all()
    for f in flights:
        f.setStrDate()
    context = {
        'ips': ips,
        'flights': flights,
    }
    return render(request,'flylo/Comparator.html',context)

"""def user_can_download(user):
    return user.is_authenticated() and user.have_id_card()

@user_passes_test(user_can_download, login_url="/login/")
def buy(request):
    # Code here can assume a logged-in user with the correct permission.
   <head>
    {% if notlog %}
    <a href="{% url 'login' %}">Log in</a>
    <a href="{% url 'logout' %}">Log out</a>
    <a href="{% url 'register' %}">register</a>
    {% else %}
    <p>{{userh}}</p>
    {% endif %}
</head>
next_page extra parameter in view log out
http://127.0.0.1:8000/flylo/accounts/login/?next=/flylo/flights/ get next to log in
    """


def is_comercial_test(user):
    return user.groups.filter(name='Comercial').exists()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # We always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only commercial users can POST new flights (or staff)
        if request.method == 'POST':
            return is_comercial_test(request.user) or request.user.is_staff
        # Write permissions are only allowed to the owner (or staff)
        return obj.owner == request.user or request.user.is_staff

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

class FlightViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Flights to be viewed or edited.
    """
    serializer_class = FlightSerializer
    queryset = Flight.objects.all().order_by('flight_number')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, ]

    def get_queryset(self):
        queryset = Flight.objects.all().order_by('flight_number')

        departure = self.request.query_params.get('departure', None)
        arrival = self.request.query_params.get('arrival', None)
        departure_time = self.request.query_params.get('departure_time', None)
        arrival_time = self.request.query_params.get('arrival_time', None)

        if departure is not None:
            queryset = queryset.filter(location_departure=departure)
        if arrival is not None:
            queryset = queryset.filter(location_arrival=arrival)
        if departure_time is not None:
            queryset = queryset.filter(estimated_time_departure=departure_time)
        if arrival_time is not None:
            queryset = queryset.filter(estimated_time_arrival=arrival_time)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AirlineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Flights to be viewed or edited.
    """
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAdminOrReadOnly, ]

class AircraftViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Flights to be viewed or edited.
    """
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_classes = [IsAdminOrReadOnly, ]

