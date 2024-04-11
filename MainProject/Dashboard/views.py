from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
import requests
from django.contrib.auth.decorators import login_required
import joblib
from Predictions.models import FootballPredictor
import pandas as pd

today = datetime.today()
week_ago = today - timedelta(days=7)
week_ago_formatted = week_ago.strftime('%y-%m-%d')
today_formatted = today.strftime('%y-%m-%d')

@login_required(login_url="login")
def display_dashboard(request):
    #Retrieve the current user
    user = request.user
    
    #Retrieve the users favourite team
    favourite_team = user.team_name
    
    print("Favourite Team:", favourite_team)
    
    # Make API call to fetch league standings data
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    standings_response = requests.get(standings_url)
    standings_data = standings_response.json()
    
    # make API call to get events data
    events_url = "https://apiv3.apifootball.com/?action=get_events&from=2024-01-05&to="+today_formatted+"&team_id="+favourite_team+"&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    events_response = requests.get(events_url)
    events_data = events_response.json() #turning the text result into json (array)
    
    latest_match_id = events_data[-1]['match_id']
    
    # Make API call to get top scorer data
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()
    
    # Make API call to get favourite team data
    favouriteTeam_url = "https://apiv3.apifootball.com/?action=get_teams&team_id="+favourite_team+"&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    favouriteTeam_response = requests.get(favouriteTeam_url)
    favouriteTeam_data = favouriteTeam_response.json()
    
    
    return render(request, 'Dashboard/dashboard.html', {'standings_data': standings_data, 'events_data': events_data, 'topScorer_data': topScorer_data, 'favouriteTeam_data': favouriteTeam_data})


def display_stats(request):
    # Make API call to fetch league standings data
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    standings_response = requests.get(standings_url)
    standings_data = standings_response.json()
    
    # Prepare data for the composite bar chart
    team_names = [team['team_name'] for team in standings_data]
    goals_for = [team['overall_league_GF'] for team in standings_data]
    goals_against = [team['overall_league_GA'] for team in standings_data]
    league_positions = [team['overall_league_position'] for team in standings_data]
    wins = [team['overall_league_W'] for team in standings_data]
    draws = [team['overall_league_D'] for team in standings_data]
    losses = [team['overall_league_L'] for team in standings_data]
    home_wins = [team['home_league_W'] for team in standings_data]
    home_draws = [team['home_league_D'] for team in standings_data]
    home_losses = [team['home_league_L'] for team in standings_data]
    away_wins = [team['away_league_W'] for team in standings_data]
    away_draws = [team['away_league_D'] for team in standings_data]
    away_losses = [team['away_league_L'] for team in standings_data]
    
    return render(request, 'Dashboard/topscorer.html', {
        'team_names': team_names,
        'goals_for': goals_for,
        'goals_against': goals_against,
        'league_positions': league_positions,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'home_wins': home_wins,
        'home_draws': home_draws,
        'home_losses': home_losses,
        'away_wins': away_wins,
        'away_draws': away_draws,
        'away_losses': away_losses,
    })

def display_fixtures(request):
    # Calculate dates for past matches and upcoming fixtures
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    today_formatted = today.strftime("%Y-%m-%d")
    week_ago_formatted = week_ago.strftime("%Y-%m-%d")

    # Fetch past matches
    past_fixtures_url = "https://apiv3.apifootball.com/?action=get_events&from=" + week_ago_formatted + "&to=" + today_formatted + "&league_id=152&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    past_fixtures_response = requests.get(past_fixtures_url)
    past_fixtures_data = past_fixtures_response.json()

    # Fetch upcoming fixtures
    upcoming_fixtures_url = "https://apiv3.apifootball.com/?action=get_events&from=" + today_formatted + "&to=" + (today + timedelta(days=50)).strftime("%Y-%m-%d") + "&league_id=152&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    upcoming_fixtures_response = requests.get(upcoming_fixtures_url)
    upcoming_fixtures_data = upcoming_fixtures_response.json()
    
    #Prepare data for predictions
    team_mapping = {
        "Bournemouth": 2,
        "Manchester Utd": 16,
        "Brentford": 3,
        "Sheffield Utd": 20,
        "Burnley": 5,
        "Brighton": 4,
        "Manchester City": 15,
        "Luton": 12,
        "Newcastle": 17,
        "Tottenham": 22,
        "Nottingham": 19,
        "Wolves": 26,
        "Arsenal": 0,
        "Aston Villa": 1,
        "Liverpool": 14,
        "Crystal Palace": 8,
        "West Ham": 25,
        "Fulham": 10,
        "Chelsea": 7,
        "Everton": 9,
    }
    
    predictor = FootballPredictor()
    
    # Iterate over upcoming fixtures and make predictions
    for fixture in upcoming_fixtures_data:
        team_name = fixture["match_hometeam_name"]
        opp_team_name = fixture["match_awayteam_name"]
        day_of_week = datetime.strptime(fixture["match_date"], "%Y-%m-%d").weekday()
        hour_of_match = int(fixture["match_time"].split(":")[0])
        venue_code = 1 if fixture["match_hometeam_name"] == team_name else 0

        # Map team names to numerical codes
        home_team_code = team_mapping.get(team_name)
        opp_team_code = team_mapping.get(opp_team_name)
        
        team_performance = [
            venue_code,
            opp_team_code,
            hour_of_match,
            day_of_week,
            home_team_code
        ]

        # Make prediction
        prediction = predictor.predict_outcome(team_performance)

        # Add prediction to fixture data
        fixture["prediction"] = prediction

    
    return render(request, 'Dashboard/fixtures.html', {'past_fixtures_data': past_fixtures_data, 'upcoming_fixtures_data': upcoming_fixtures_data})

def display_match_details(request, match_id):
    match_details_url = "https://apiv3.apifootball.com/?action=get_events&match_id="+match_id+"&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    match_details_response = requests.get(match_details_url)
    match_details_data = match_details_response.json()
    
    home_team_id = match_details_data[0]["match_hometeam_id"]
    away_team_id = match_details_data[0]["match_awayteam_id"]
    
    h2h_url = "https://apiv3.apifootball.com/?action=get_H2H&firstTeamId="+home_team_id+"&secondTeamId="+away_team_id+"&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    h2h_response = requests.get(h2h_url)
    h2h_data = h2h_response.json()
    
    return render(request, 'Dashboard/match_details.html', {'match_details_data': match_details_data, 'h2h_data': h2h_data})

def display_team_details(request, team_id):
    team_details_url = "https://apiv3.apifootball.com/?action=get_teams&team_id="+team_id+"&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    team_details_response = requests.get(team_details_url)
    team_details_data = team_details_response.json()
    return render(request, 'Dashboard/team_details.html', {'team_details_data': team_details_data})

def display_player_details(request, player_id):
    player_details_url = "https://apiv3.apifootball.com/?action=get_players&player_id="+player_id+"&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    player_details_response = requests.get(player_details_url)
    player_details_data = player_details_response.json()
    
    clubs_list = ['Arsenal',
                  'Liverpool',
                  'Manchester City',
                  'Aston Villa',
                  'Tottenham Hotspur',
                  'Manchester United',
                  'West Ham United',
                  'Newcastle United',
                  'Brighton & Hove Albion',
                  'Wolverhampton Wanderers',
                  'AFC Bournemouth',
                  'Chelsea',
                  'Fulham',
                  'Crystal Palace',
                  'Brentford',
                  'Everton',
                  'Nottingham Forest',
                  'Luton Town',
                  'Burnley',
                  'Sheffield United']
    
    return render(request, 'Dashboard/player_details.html', {'player_details_data': player_details_data, 'clubs': clubs_list})

def display_player_stats(request):
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=4f8b1de6e9bc7f5bdd5db3b94221a3c7628cfd7e1f457eac33ecacf6ca91730d"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()
    
    return render(request, 'Dashboard/player_stats.html', {'topScorer_data': topScorer_data})

def display_predictions(request):
    team_performance = [0, 64, 16, 5, 11]
    predictor = FootballPredictor()
    prediction = predictor.predict_outcome(team_performance)
    context = {'prediction': prediction}
    
    return render(request, 'Dashboard/predictions.html', context)

    
