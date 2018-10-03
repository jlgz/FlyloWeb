
from .models import Flight, Airline, Aircraft
from rest_framework import serializers

class FlightSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Flight
        fields = ('url', 'flight_number', 'location_departure','location_arrival','airline','aircraft','estimated_time_departure','estimated_time_arrival','status','seats_bussines_free','seats_economic_free','neconomic_free','nbussiness_free', 'owner', 'price')

class AirlineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Airline
        fields = ('url', 'airline_code','offer_categories')

class AircraftSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aircraft
        fields = ('url','aircraft_number','seats_bussines_id','seats_economic_id')

