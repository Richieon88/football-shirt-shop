from django.shortcuts import render, get_object_or_404
from .models import Shirt, ShirtSize

def shirts_list(request):
    # Fetch unique teams and seasons for filter options
    teams = Shirt.objects.values_list('team', flat=True).distinct()
    seasons = Shirt.objects.values_list('season', flat=True).distinct()

    # Apply filters based on query parameters
    team = request.GET.get('team')
    season = request.GET.get('season')
    home_or_away = request.GET.get('home_or_away')

    shirts = Shirt.objects.all()

    if team:
        shirts = shirts.filter(team=team)
    if season:
        shirts = shirts.filter(season=season)
    if home_or_away:
        shirts = shirts.filter(home_or_away=home_or_away)

    return render(request, 'shirts/shirt_list.html', {
        'shirts': shirts,
        'teams': teams,
        'seasons': seasons,
        'selected_team': team,
        'selected_season': season,
        'selected_home_or_away': home_or_away
    })

def shirt_detail(request, pk):
    shirt = get_object_or_404(Shirt, pk=pk)
    shirt_sizes = ShirtSize.objects.filter(shirt=shirt)
    return render(request, 'shirts/shirt_detail.html', {'shirt': shirt, 'shirt_sizes': shirt_sizes})