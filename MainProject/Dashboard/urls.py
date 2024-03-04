from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.display_dashboard, name='dashboard'),
    path('topscorer', views.display_topscorer_list, name='topscorer'),
    path('fixtures', views.display_fixtures, name='fixtures')
]
