from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

import requests

def index(request):
    today = datetime.today().strftime('%y-%m-%d')
    url = "https://apiv3.apifootball.com/?action=get_events&from=2024-01-22&to=2024-01-22&league_id=152&APIkey=9c9749f2a2029cae173b134f0587a2761af39a48300c0627414b0181e7a32251"
    response = requests.get(url)
    jsonResponse = response.json() #turning the text result into json (array)
    return render(request, 'Dashboard/index.html',{'jsonResponse':jsonResponse})
