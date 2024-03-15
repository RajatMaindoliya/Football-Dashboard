from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
import requests
from django.contrib.auth.decorators import login_required

today = datetime.today()
week_ago = today - timedelta(days=7)
week_ago_formatted = week_ago.strftime('%y-%m-%d')
today_formatted = today.strftime('%y-%m-%d')

@login_required(login_url="login")
def display_dashboard(request):
    #Retrieve the current user
    user = request.user
    
    #Retrieve the user's favourite team
    favourite_team = user.team_name
    
    print("Favourite Team:", favourite_team)
    
    # Make API call to fetch league standings data
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    standings_response = requests.get(standings_url)
    standings_data = standings_response.json()
    
    # make API call to get events data
    events_url = "https://apiv3.apifootball.com/?action=get_events&from=2024-01-05&to="+today_formatted+"&team_id="+favourite_team+"&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    events_response = requests.get(events_url)
    events_data = events_response.json() #turning the text result into json (array)
    
    latest_match_id = events_data[-1]['match_id']
    
    # Make API call to get top scorer data
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()
    
    # Make API call to get favourite team data
    favouriteTeam_url = "https://apiv3.apifootball.com/?action=get_teams&team_id="+favourite_team+"&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    favouriteTeam_response = requests.get(favouriteTeam_url)
    favouriteTeam_data = favouriteTeam_response.json()
    
    
    return render(request, 'Dashboard/dashboard.html', {'standings_data': standings_data, 'events_data': events_data, 'topScorer_data': topScorer_data, 'favouriteTeam_data': favouriteTeam_data})


def display_stats(request):
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()
    
    # Make API call to fetch league standings data
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    standings_response = requests.get(standings_url)
    standings_data = standings_response.json()
    
    # Prepare data for the composite bar chart
    team_names = [team['team_name'] for team in standings_data]
    goals_for = [team['overall_league_GF'] for team in standings_data]
    goals_against = [team['overall_league_GA'] for team in standings_data]
    
    return render(request, 'Dashboard/topscorer.html', {
        'team_names': team_names,
        'goals_for': goals_for,
        'goals_against': goals_against,
        'topScorer_data': topScorer_data,
    })

def display_fixtures(request):
    fixtures_url = "https://apiv3.apifootball.com/?action=get_events&from="+week_ago_formatted+"&to="+today_formatted+"&league_id=152&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    fixtures_response = requests.get(fixtures_url)
    fixtures_data = fixtures_response.json()
    
    return render(request, 'Dashboard/fixtures.html', {'fixtures_data': fixtures_data})

def display_match_details(request, match_id):
    match_details_url = "https://apiv3.apifootball.com/?action=get_events&match_id="+match_id+"&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    match_details_response = requests.get(match_details_url)
    match_details_data = match_details_response.json()
    return render(request, 'Dashboard/match_details.html', {'match_details_data': match_details_data})

def display_team_details(request, team_id):
    team_details_url = "https://apiv3.apifootball.com/?action=get_teams&team_id="+team_id+"&APIkey=13a784d9a73d9914e594fe99be25adc491c307684840f6fa89be23ba2206fa06"
    team_details_response = requests.get(team_details_url)
    team_details_data = team_details_response.json()
    return render(request, 'Dashboard/team_details.html', {'team_details_data': team_details_data})

    
