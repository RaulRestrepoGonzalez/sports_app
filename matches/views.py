from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import requests
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render
from user_agents import parse
from django.contrib import messages
from .forms import RegisterForm, LoginForm

API_KEY = '126c43ebeb56579485963bf9a3bf232f'
BASE_URL = 'https://v3.football.api-sports.io/fixtures'
STANDINGS_URL = 'https://v3.football.api-sports.io/standings'
LEAGUES_URL = 'https://v3.football.api-sports.io/leagues'

def home(request):
    current_date = datetime.now().strftime('%Y-%m-%d')  # Formato: YYYY-MM-DD
    current_year = datetime.now().year
    user_agent = parse(request.META.get('HTTP_USER_AGENT'))
    is_mobile = user_agent.is_mobile
    
    # Obtener las ligas disponibles
    leagues = get_leagues()
    # Obtener la fecha y temporada del formulario o usar los valores actuales por defecto
    selected_date = request.GET.get('date', current_date)
    selected_season = request.GET.get('season', str(current_year))
    selected_league = request.GET.get('league', '39')
    
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    params = {
        'date': selected_date,  # Fecha seleccionada o actual
        'league': selected_league,  # Liga seleccionada
        'season': selected_season # Temporada seleccionada
    }
    #response = requests.get(BASE_URL, headers=headers, params=params)
    #fixtures = response.json().get('response', [])
    #return render(request, 'home.html', {'fixtures': fixtures})
    response = requests.get(BASE_URL, headers=headers, params=params)
    fixtures = response.json().get('response', [])

    return render(request, 'home.html', {
        'fixtures': fixtures,
        'current_date': selected_date,
        'current_season': selected_season,
        'leagues': leagues,  # Pasar las ligas al frontend
        'selected_league': selected_league,  # Liga seleccionada
        'is_mobile': is_mobile
    })

def get_leagues():
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    try:
        response = requests.get(LEAGUES_URL, headers=headers)
        response.raise_for_status()  # Lanza un error si la solicitud falla (códigos HTTP 4xx o 5xx)
        leagues_data = response.json().get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching leagues: {e}")
        leagues_data = []  # Devuelve una lista vacía en caso de error
    return leagues_data

# Vista para el registro
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después del registro
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect('home')
        else:
            messages.error(request, "Error en el registro. Por favor, corrige los errores.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Vista para el inicio de sesión
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Error en el formulario. Por favor, corrige los errores.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Vista para cerrar sesión
def user_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('home')


def match_detail(request, match_id):
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(f"{BASE_URL}/{match_id}", headers=headers)
    match_data = response.json().get('response', {})
    return render(request, 'match_detail.html', {'match_data': match_data})

def league_standings(request):
    # Obtener los filtros del formulario o usar valores predeterminados
    selected_date = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_season = request.GET.get('season', str(datetime.now().year))
    selected_league = request.GET.get('league', '39')  # Default: Premier League

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    params = {
        'date': selected_date,
        'league': selected_league,
        'season': selected_season
    }

    try:
        response = requests.get(STANDINGS_URL, headers=headers, params=params)
        response.raise_for_status()
        standings_data = response.json().get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching standings: {e}")
        standings_data = []

    return render(request, 'league_standings.html', {
        'standings_data': standings_data,
        'selected_date': selected_date,
        'selected_season': selected_season,
        'selected_league': selected_league
    })
    
def results(request):
    # Obtener los filtros del formulario o usar valores predeterminados
    selected_date = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_league = request.GET.get('league', '39')  # Default: Premier League
    selected_season = request.GET.get('season', str(datetime.now().year))

    params = {
        'date': selected_date,
        'league': selected_league,
        'season': selected_season,
    }

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        matches = response.json().get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching matches: {e}")
        matches = []

    # Obtener las ligas disponibles para el combobox
    leagues = get_leagues()

    return render(request, 'match_detail.html', {
        'matches': matches,
        'current_date': selected_date,
        'current_season': selected_season,
        'selected_league': selected_league,
        'leagues': leagues
    })