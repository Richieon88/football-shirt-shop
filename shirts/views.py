from django.shortcuts import render, get_object_or_404
from .models import Shirt

def shirts_list(request):
    shirts = Shirt.objects.all()
    return render(request, 'shirts/shirt_list.html', {'shirts': shirts})

def shirt_detail(request, pk):
    shirt = get_object_or_404(Shirt, pk=pk)
    return render(request, 'shirts/shirt_detail.html', {'shirt': shirt})