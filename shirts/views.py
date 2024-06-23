from django.shortcuts import render
from .models import Shirt

def shirts_list(request):
    shirts = Shirt.objects.all()
    return render(request, 'shirts/shirt_list.html', {'shirts': shirts})
