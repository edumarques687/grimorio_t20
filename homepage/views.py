from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.
def home(request):
    return render(request, 'homepage/home.html')

def spell(request):
    return render(request, 'homepage/spell.html')

def password(request):

    characters = list('qwertyuiopasdfghjklzxcvbnm')
    if request.GET.get('uppercase'):
        characters.extend('QWERTYUIOPASDFGHJKLZXCVBNM')
    if request.GET.get('numbers'):
        characters.extend('1234567890')
    if request.GET.get('special_characters'):
        characters.extend('!@#$%&*')

    length = int(request.GET.get('length', 7))

    generated_password = ''
    for x in range(length):
        generated_password += random.choice(characters)
    return render(request, 'homepage/password.html', {'password': generated_password})
