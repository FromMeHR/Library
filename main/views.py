from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
from books.models import Categories

def index(request):
    categories = Categories.objects.all()
    context = {
        'title':'Main',
        'categories':categories
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title':'About', 
    }
    return render(request, 'main/about.html', context)

def contacts(request):
    context = {
        'title':'Contacts', 
    }
    return render(request, 'main/contacts.html', context)

def ordering_system(request):
    context = {
        'title':'Ordering system', 
        'text_on_page':'Text on this page'
    }
    return render(request, 'main/ordering_system.html', context)