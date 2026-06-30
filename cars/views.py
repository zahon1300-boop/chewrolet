from django.shortcuts import render, get_object_or_404
from .models import Car, CarCategory

def home(request):
    featured_cars = Car.objects.filter(is_featured=True)[:6]
    categories = CarCategory.objects.all()
    return render(request, 'home.html', {
        'featured_cars': featured_cars,
        'categories': categories,
    })

def cars_list(request):
    cars = Car.objects.all()
    categories = CarCategory.objects.all()
    return render(request, 'cars/cars_list.html', {
        'cars': cars,
        'categories': categories,
    })

def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    specifications = car.specifications.all()
    colors = car.colors.all()
    gallery = car.gallery.all()
    return render(request, 'cars/car_detail.html', {
        'car': car,
        'specifications': specifications,
        'colors': colors,
        'gallery': gallery,
    })
