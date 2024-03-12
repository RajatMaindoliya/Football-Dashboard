from django.shortcuts import render,redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Dashboard.views import display_dashboard

def homepage(request):
    
    return render(request, 'Authentication/index.html')

def register(request):
    
    form = CreateUserForm
    if request.method == "POST":
        
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    
    context = {'registerform':form}
    return render(request, 'Authentication/register.html', context=context)



def login(request):
     
    form = LoginForm() 
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                
                return display_dashboard(request)
            
    context = {'loginform': form}
        
    return render(request, 'Authentication/login.html', context=context)



def logout(request):
    
    auth.logout(request)
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    
    return render(request, 'Authentication/index.html')
