from django.shortcuts import render
from .models import Dealer

def dealers_list(request):
    dealers = Dealer.objects.filter(is_active=True)
    return render(request, 'dealers/dealers_list.html', {
        'dealers': dealers,
    })
