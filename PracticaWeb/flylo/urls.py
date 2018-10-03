from django.conf.urls import url

from . import views
listOfAddresses = ["127.0.0.1","127.0.0.1"]
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^flights/()$', views.flights, name='flights'),
    url(r'^flights/(?P<departure>.*)/(?P<number>.*)/$', views.detailFlight, name='detailFlight'),
    url(r'^flights/(?P<departure>.*)/$', views.flights, name='flights'),
    url(r'^shoppingcart/$', views.shoppingcart, name='shoppingcart'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^postBuy/$', views.postBuy, name='postBuy'),
    url(r'^returnTRIPS/$', views.flights_r, name='flights_r'),
    url(r'^postcheckIn/$', views.postCheckIn, name='postCheckIn'),
    url(r'^checkIn/(?P<number>.*)/$', views.checkIn, name='checkIn'),
    url(r'^checkIn/$', views.preCheckIn, name='checkIn'),
    url(r'^accounts/profile/$',views.index,name = 'profile'),
    url(r'^comparator$', views.comparator, {'ips': listOfAddresses},name = 'comparator'),
]
