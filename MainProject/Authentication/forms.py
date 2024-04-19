from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    
    #team choices for the user to pick from with the IDs that correspond to the API
    TEAM_CHOICES = [
        ('141', 'Arsenal'),
        ('3088', 'Aston Villa FC'),
        ('3071', 'Bournemouth AFC'),
        ('3086', 'Brentford'),
        ('3079', 'Brighton & Hove Albion'),
        ('3075', 'Burnley'),
        ('88', 'Chelsea'),
        ('3429', 'Crystal Palace'),
        ('3073', 'Everton FC'),
        ('3085', 'Fulham'),
        ('84', 'Liverpool FC'),
        ('3091', 'Luton Town'),
        ('80', 'Manchester City FC'),
        ('102', 'Manchester United FC'),
        ('3100', 'Newcastle United'),
        ('3089', 'Nottingham Forest'),
        ('3074', 'Sheffield United'),
        ('164', 'Tottenham Hotspur FC'),
        ('3081', 'West Ham United'),
        ('3077', 'Wolverhampton Wanderers'),
    ]
    
    team_name = forms.ChoiceField(choices=TEAM_CHOICES)
    
    class Meta:
        model = CustomUser 
        fields = ['username', 'email', 'password1', 'password2', 'team_name'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    
    


    