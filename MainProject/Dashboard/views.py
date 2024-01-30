from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

import requests

def index(request):
    # Make API call to fetch league standings data
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=9c9749f2a2029cae173b134f0587a2761af39a48300c0627414b0181e7a32251"
    standings_response = requests.get(standings_url)
    standings_data = standings_response.json()
    
    team_id = 102
    today = datetime.today().strftime('%y-%m-%d')
    
    events_url = "https://apiv3.apifootball.com/?action=get_events&from=2024-01-22&to=2024-01-22&league_id=152&APIkey=9c9749f2a2029cae173b134f0587a2761af39a48300c0627414b0181e7a32251"
    events_response = requests.get(events_url)
    events_data = events_response.json() #turning the text result into json (array)
    
    return render(request, 'Dashboard/index.html', {'standings_data': standings_data, 'events_data': events_data})
