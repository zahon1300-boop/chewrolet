from django.shortcuts import render
from .models import News

def news_list(request):
    news_list = News.objects.filter(is_published=True)
    return render(request, 'news/news_list.html', {
        'news_list': news_list,
    })
