from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
import requests

today = datetime.today()
week_ago = today - timedelta(days=7)
week_ago_formatted = week_ago.strftime('%y-%m-%d')
today_formatted = today.strftime('%y-%m-%d')

def display_dashboard(request):
    # Make API call to fetch league standings data
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    standings_response = requests.get(standings_url)
    standings_data = standings_response.json()
    
    team_id = 102
    
    # make API call to get events data
    events_url = "https://apiv3.apifootball.com/?action=get_events&from=2024-02-15&to=2024-02-22&league_id=152&team_id=102&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    events_response = requests.get(events_url)
    events_data = events_response.json() #turning the text result into json (array)
    
    # Make API call to get top scorer data
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()

    
    return render(request, 'Dashboard/dashboard.html', {'standings_data': standings_data, 'events_data': events_data, 'topScorer_data': topScorer_data})


def display_topscorer_list(request):
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()
    
    return render(request, 'Dashboard/topscorer.html', {'topScorer_data': topScorer_data})

def display_fixtures(request):
    fixtures_url = "https://apiv3.apifootball.com/?action=get_events&from="+week_ago_formatted+"&to="+today_formatted+"&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    fixtures_response = requests.get(fixtures_url)
    fixtures_data = fixtures_response.json()
    
    return render(request, 'Dashboard/fixtures.html', {'fixtures_data': fixtures_data})

    
