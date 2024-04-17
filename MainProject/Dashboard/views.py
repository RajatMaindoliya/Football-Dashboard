from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
import requests
from django.contrib.auth.decorators import login_required
import joblib
from Predictions.models import FootballPredictor
import pandas as pd
from . forms import PredictionForm

today = datetime.today()
week_ago = today - timedelta(days=7)
week_ago_formatted = week_ago.strftime('%y-%m-%d')
today_formatted = today.strftime('%y-%m-%d')

@login_required(login_url="login")
def display_dashboard(request):
    user = request.user

    favourite_team = user.team_name
    
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    standings_response = requests.get(standings_url)
    standings_data = standings_response.json()
    
    events_url = "https://apiv3.apifootball.com/?action=get_events&from=2024-01-05&to="+today_formatted+"&team_id="+favourite_team+"&league_id=152&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    events_response = requests.get(events_url)
    events_data = events_response.json()
    
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()
    
    top_scorer_player_key = topScorer_data[0]['player_key']
    topScorerImage_url = "https://apiv3.apifootball.com/?action=get_players&player_id=" + str(top_scorer_player_key) + "&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    topScorerImage_response = requests.get(topScorerImage_url)
    topScorerImage_data = topScorerImage_response.json()
    
    favouriteTeam_url = "https://apiv3.apifootball.com/?action=get_teams&team_id="+favourite_team+"&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    favouriteTeam_response = requests.get(favouriteTeam_url)
    favouriteTeam_data = favouriteTeam_response.json()
    
    team_mapping = {
        "3071": 2,
        "102": 16,
        "3086": 3,
        "3074": 20,
        "3075": 5,
        "3079": 4,
        "80": 15,
        "3091": 12,
        "3100": 17,
        "164": 22,
        "3089": 19,
        "3077": 26,
        "141": 0,
        "3088": 1,
        "84": 14,
        "3429": 8,
        "3081": 25,
        "3085": 10,
        "88": 7,
        "3073": 9,
    }
    
    predictor = FootballPredictor()
    
    latest_match = events_data[-1]
    team_id = latest_match["match_hometeam_id"]
    opp_team_id = latest_match["match_awayteam_id"]
    day_of_week = datetime.strptime(latest_match["match_date"], "%Y-%m-%d").weekday()
    hour_of_match = int(latest_match["match_time"].split(":")[0])
    venue_code = 1

    team_code = team_mapping.get(team_id)
    opp_team_code = team_mapping.get(opp_team_id)
        
    team_performance = [
        venue_code,
        opp_team_code,
        hour_of_match,
        day_of_week,
        team_code
    ]
    
    print(team_performance)

    prediction = predictor.predict_outcome(team_performance)

    latest_match["prediction"] = prediction
     
    return render(request, 'Dashboard/dashboard.html', {
                           'standings_data': standings_data, 
                           'events_data': events_data,
                           'topScorer_data': topScorer_data, 
                           'favouriteTeam_data': favouriteTeam_data,
                           'latest_match': latest_match,
                           'topScorerImage_data': topScorerImage_data})


def display_stats(request):
    # Make API call to fetch league standings data
    standings_url = "https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
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
    past_fixtures_url = "https://apiv3.apifootball.com/?action=get_events&from=" + week_ago_formatted + "&to=" + today_formatted + "&league_id=152&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    past_fixtures_response = requests.get(past_fixtures_url)
    past_fixtures_data = past_fixtures_response.json()

    # Fetch upcoming fixtures
    upcoming_fixtures_url = "https://apiv3.apifootball.com/?action=get_events&from=" + today_formatted + "&to=" + (today + timedelta(days=50)).strftime("%Y-%m-%d") + "&league_id=152&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    upcoming_fixtures_response = requests.get(upcoming_fixtures_url)
    upcoming_fixtures_data = upcoming_fixtures_response.json()
    
    #Prepare data for predictions
    team_mapping = {
        "3071": 2,
        "102": 16,
        "3086": 3,
        "3074": 20,
        "3075": 5,
        "3079": 4,
        "80": 15,
        "3091": 12,
        "3100": 17,
        "164": 22,
        "3089": 19,
        "3077": 26,
        "141": 0,
        "3088": 1,
        "84": 14,
        "3429": 8,
        "3081": 25,
        "3085": 10,
        "88": 7,
        "3073": 9,
    }
    
    predictor = FootballPredictor()
    
    for fixture in upcoming_fixtures_data:
        team_id = fixture["match_hometeam_id"]
        opp_team_id = fixture["match_awayteam_id"]
        day_of_week = datetime.strptime(fixture["match_date"], "%Y-%m-%d").weekday()
        hour_of_match = int(fixture["match_time"].split(":")[0])
        venue_code = 1

        team_code = team_mapping.get(team_id)
        opp_team_code = team_mapping.get(opp_team_id)
        
        team_performance = [
            venue_code,
            opp_team_code,
            hour_of_match,
            day_of_week,
            team_code
        ]

        prediction = predictor.predict_outcome(team_performance)

        fixture["prediction"] = prediction

    
    return render(request, 'Dashboard/fixtures.html', {'past_fixtures_data': past_fixtures_data, 'upcoming_fixtures_data': upcoming_fixtures_data})

def display_match_details(request, match_id):
    match_details_url = "https://apiv3.apifootball.com/?action=get_events&match_id="+match_id+"&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    match_details_response = requests.get(match_details_url)
    match_details_data = match_details_response.json()
    
    statistics = match_details_data[0]["statistics"]
    total_shots = {"home": None, "away": None}
    total_passes = {"home": None, "away": None}
    accurate_passes = {"home": None, "away": None}
    shots_on_target = {"home": None, "away": None}
    shots_inside_box = {"home": None, "away": None}
    shots_outside_box = {"home": None, "away": None}
    fouls = {"home": None, "away": None}
    offsides = {"home": None, "away": None}
    corners = {"home": None, "away": None}
    saves = {"home": None, "away": None}
    
    
    #I used different for loops and the data provided by the API is not consistent
    for stat in statistics:
        if stat["type"] == "Shots Total":
            total_shots["home"] = stat["home"]
            total_shots["away"] = stat["away"]
            break
    
    for stat in statistics:
        if stat["type"] == "Passes Total":
            total_passes["home"] = stat["home"]
            total_passes["away"] = stat["away"]
            break
        
    for stat in statistics:
        if stat["type"] == "Passes Accurate":
            accurate_passes["home"] = stat["home"]
            accurate_passes["away"] = stat["away"]
            break
        
    for stat in statistics:
        if stat["type"] == "On Target":
            shots_on_target["home"] = stat["home"]
            shots_on_target["away"] = stat["away"]
            break
        
    for stat in statistics:
        if stat["type"] == "Shots Inside Box":
            shots_inside_box["home"] = stat["home"]
            shots_inside_box["away"] = stat["away"]
            break
        
    for stat in statistics:
        if stat["type"] == "Shots Outside Box":
            shots_outside_box["home"] = stat["home"]
            shots_outside_box["away"] = stat["away"]
            break
        
    for stat in statistics:
        if stat["type"] == "Fouls":
            fouls["home"] = stat["home"]
            fouls["away"] = stat["away"]
            break
    
    for stat in statistics:
        if stat["type"] == "Offsides":
            offsides["home"] = stat["home"]
            offsides["away"] = stat["away"]
            break
        
    for stat in statistics:
        if stat["type"] == "Corners":
            corners["home"] = stat["home"]
            corners["away"] = stat["away"]
            break
    
    for stat in statistics:
        if stat["type"] == "Saves":
            saves["home"] = stat["home"]
            saves["away"] = stat["away"]
            break
    
        
    #Gather the head to head data
    home_team_id = match_details_data[0]["match_hometeam_id"]
    away_team_id = match_details_data[0]["match_awayteam_id"]
    
    h2h_url = "https://apiv3.apifootball.com/?action=get_H2H&firstTeamId="+home_team_id+"&secondTeamId="+away_team_id+"&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    h2h_response = requests.get(h2h_url)
    h2h_data = h2h_response.json()
    
    return render(request, 'Dashboard/match_details.html', 
                          {'match_details_data': match_details_data,
                           'h2h_data': h2h_data,
                           'total_shots': total_shots,
                           'total_passes': total_passes,
                           'accurate_passes': accurate_passes,
                           'shots_on_target': shots_on_target,
                           'shots_inside_box': shots_inside_box,
                           'shots_outside_box': shots_outside_box,
                           'fouls': fouls,
                           'offsides': offsides,
                           'corners': corners,
                           'saves': saves})

def display_team_details(request, team_id):
    team_details_url = "https://apiv3.apifootball.com/?action=get_teams&team_id="+team_id+"&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    team_details_response = requests.get(team_details_url)
    team_details_data = team_details_response.json()
    return render(request, 'Dashboard/team_details.html', {'team_details_data': team_details_data})

def display_player_details(request, player_id):
    player_details_url = "https://apiv3.apifootball.com/?action=get_players&player_id="+player_id+"&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    player_details_response = requests.get(player_details_url)
    player_details_data = player_details_response.json()
    
    player_details_data = player_details_data[-1]
    
    return render(request, 'Dashboard/player_details.html', {'player_details_data': player_details_data})

def display_player_stats(request):
    topScorer_url = "https://apiv3.apifootball.com/?action=get_topscorers&league_id=152&APIkey=914cc74bf4d2df76a18517ee040621b1158ccd9d5f10f15679512c190a06472d"
    topScorer_response = requests.get(topScorer_url)
    topScorer_data = topScorer_response.json()
    
    return render(request, 'Dashboard/player_stats.html', {'topScorer_data': topScorer_data})

def display_predictions(request):
    prediction = None
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            venue_code = form.cleaned_data['venue_code']
            opp_team_code = form.cleaned_data['opp_team_code']
            hour_of_match = form.cleaned_data['hour_of_match']
            day_of_week = form.cleaned_data['day_of_week']
            team_code = form.cleaned_data['team_code']
            
            predictor = FootballPredictor()
            team_performance = [venue_code, opp_team_code, hour_of_match, day_of_week, team_code]
            prediction = predictor.predict_outcome(team_performance)
            
            team_names = {
                '0': 'Arsenal',
                '1': 'Aston Villa FC',
                '2': 'Bournemouth AFC',
                '3': 'Brentford',
                '4': 'Brighton & Hove Albion',
                '5': 'Burnley',
                '7': 'Chelsea',
                '8': 'Crystal Palace',
                '9': 'Everton FC',
                '10': 'Fulham',
                '14': 'Liverpool FC',
                '12': 'Luton Town',
                '15': 'Manchester City FC',
                '16': 'Manchester United FC',
                '17': 'Newcastle United',
                '19': 'Nottingham Forest',
                '20': 'Sheffield United',
                '22': 'Tottenham Hotspur FC',
                '25': 'West Ham United',
                '26': 'Wolverhampton Wanderers',
            }
            
            if prediction == 0: #if a loss for your team
                predicted_winner = team_names[opp_team_code]
            elif prediction == 1: 
                predicted_winner = team_names[team_code]
            else:
                predicted_winner = 'Draw'
            
            context = {
                'form': form,
                'prediction': predicted_winner,
            }
            return render(request, 'Dashboard/predictions.html', context)
    else:
        form = PredictionForm()
    
    return render(request, 'Dashboard/predictions.html', {'form': form})

    
