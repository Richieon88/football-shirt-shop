from django.shortcuts import render, get_object_or_404
from .models import Shirt, ShirtSize

def shirts_list(request):
    shirts = Shirt.objects.all()
    return render(request, 'shirts/shirt_list.html', {'shirts': shirts})

def shirt_detail(request, pk):
    shirt = get_object_or_404(Shirt, pk=pk)
    shirt_sizes = ShirtSize.objects.filter(shirt=shirt)
    return render(request, 'shirts/shirt_detail.html', {'shirt': shirt, 'shirt_sizes': shirt_sizes})
