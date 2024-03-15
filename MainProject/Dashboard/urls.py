from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.display_dashboard, name='dashboard'),
    path('stats', views.display_stats, name='stats'),
    path('fixtures', views.display_fixtures, name='fixtures'),
    path('match_details/<str:match_id>/', views.display_match_details, name='match_details'),
    path('team_details/<str:team_id>/', views.display_team_details, name='team_details'),
]
