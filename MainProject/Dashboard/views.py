from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests

def index(request):
    # Make API call to fetch league standings data
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=99c096fc17be683fe159341eb603465beca42fd6fe0df1843e51191b47f67d1d"
    standings_response = requests.get(standings_url)
    standings_data = standings_response.json()
    
    team_id = 102
    today = datetime.today().strftime('%y-%m-%d')
    
    # make API call to get events data
    events_url = "https://apiv3.apifootball.com/?action=get_events&from=2024-01-22&to=2024-01-22&league_id=152&APIkey=99c096fc17be683fe159341eb603465beca42fd6fe0df1843e51191b47f67d1d"
    events_response = requests.get(events_url)
    events_data = events_response.json() #turning the text result into json (array)
    
    # Make API call to get top scorer data
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=99c096fc17be683fe159341eb603465beca42fd6fe0df1843e51191b47f67d1d"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()

    
    return render(request, 'Dashboard/index.html', {'standings_data': standings_data, 'events_data': events_data, 'topScorer_data': topScorer_data})
