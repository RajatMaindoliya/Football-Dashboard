from django import forms

class PredictionForm(forms.Form):
    
    team_choices = [
        ('0', 'Arsenal'),
        ('1', 'Aston Villa FC'),
        ('2', 'Bournemouth AFC'),
        ('3', 'Brentford'),
        ('4', 'Brighton & Hove Albion'),
        ('5', 'Burnley'),
        ('7', 'Chelsea'),
        ('8', 'Crystal Palace'),
        ('9', 'Everton FC'),
        ('10', 'Fulham'),
        ('14', 'Liverpool FC'),
        ('12', 'Luton Town'),
        ('15', 'Manchester City FC'),
        ('16', 'Manchester United FC'),
        ('17', 'Newcastle United'),
        ('19', 'Nottingham Forest'),
        ('20', 'Sheffield United'),
        ('22', 'Tottenham Hotspur FC'),
        ('25', 'West Ham United'),
        ('26', 'Wolverhampton Wanderers'),     
    ]
    
    hour_choices = [
        ('12', '12:30'),
        ('14', '14:00'),
        ('14', '14:30'),
        ('15', '15:00'),
        ('15', '15:30'),
        ('16', '16:00'),
        ('16', '16:30'),
        ('17', '17:00'),
        ('17', '17:30'),
        ('18', '18:00'),
        ('18', '18:30'),
        ('19', '19:00'),
        ('19', '19:15'),
        ('19', '19:30'),
        ('19', '19:45'),
        ('20', '20:00'),
        ('20', '20:15'),
    ]
    
    day_choices = [
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ]
    
    venue_choices = [
        ('1', 'Home'),
        ('0', 'Away'),
    ]
    
    team_code = forms.ChoiceField(label='Your Team', choices=team_choices)
    opp_team_code = forms.ChoiceField(label='Opponent Team', choices=team_choices)
    hour_of_match = forms.ChoiceField(label='Hour of Match', choices=hour_choices)
    day_of_week = forms.ChoiceField(label='Day of Week', choices=day_choices)
    venue_code = forms.ChoiceField(label='Venue Code', choices=venue_choices)