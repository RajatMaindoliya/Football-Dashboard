from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('', index, name='index'),
]

#https://apiv3.apifootball.com/?action=get_events&from=2023-04-05&to=2023-04-24&league_id=152&APIkey=9c9749f2a2029cae173b134f0587a2761af39a48300c0627414b0181e7a32251