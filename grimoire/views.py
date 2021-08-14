from django.shortcuts import render, get_object_or_404, redirect
from spell.models import Spell
from .models import Grimoire
from .forms import GrimoireForm
from django.views.decorators.csrf import csrf_protect
import time

# Create your views here.

@csrf_protect
def grimoire_list(request):
    message = ''
    if request.method == "POST":
        if request.POST['name'] == '':
            message = 'Defina um nome para seu grimório de magias ;)'
        elif len(request.POST['name']) > 100:
            message = 'O nome informado é grande demais ;)'
        else:
            form = GrimoireForm(request.POST)
            new_grimoire = form.save(commit=False)
            new_grimoire.user = request.user
            new_grimoire.save()
            message = 'Grimório criado com sucesso!'
    if request.user.is_authenticated:
        user_grimoires = Grimoire.objects.filter(user=request.user).all().order_by('name')
        if user_grimoires is not None:
            return render(request, 'grimoire/grimoire_list.html', {
                'user_grimoires': user_grimoires, 'message': message})
    return render(request, 'homepage/login.html')


@csrf_protect
def delete_grimoire(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            grimoire = get_object_or_404(Grimoire, pk=request.POST['grimoire_id'])
            grimoire.delete()
            user_grimoires = Grimoire.objects.filter(user=request.user).all().order_by('name')
            return render(request, 'grimoire/grimoire_list.html', {
                'user_grimoires': user_grimoires, 'message': 'Grimório {} excluído com sucesso!'.format(grimoire.name)})
        return render(request, 'homepage/login.html')

@csrf_protect
def grimoire_page(request):
    if request.method == 'POST':
        if request.POST['action'] == 'Excluir':
            return delete_grimoire(request)

        grimoire = get_object_or_404(Grimoire, pk=request.POST['grimoire_id'])
        spell_list = [val for val in Spell.objects.all().order_by('name') if val in grimoire.spells.all()]
        return render(request, 'grimoire/grimoire_page.html', {
            'grimoire': grimoire, 'spell_list': spell_list,
            'circles': ['1', '2', '3', '4', '5'],
            'count': len(spell_list)})


@csrf_protect
def add_spells(request):
    if request.method == 'POST':
        grimoire = get_object_or_404(Grimoire, pk=request.POST['grimoire_id'])
        for value in request.POST:
            if 'spell' in value:
                spell_id = value.replace('spell', '')
                sp = Spell.objects.get(id=spell_id)
                grimoire.spells.add(sp.id)

        spell_list = [val for val in Spell.objects.all().order_by('name') if val in grimoire.spells.all()]
        return render(request, 'grimoire/grimoire_page.html', {
            'grimoire': grimoire, 'spell_list': spell_list, 'circles': ['1', '2', '3', '4', '5'],
            'count': len(spell_list)})

@csrf_protect
def remove_spell(request):
    if request.method == 'POST':
        grimoire = get_object_or_404(Grimoire, pk=request.POST['grimoire_id'])
        value = request.POST['spell']
        spell_id = value.replace('spell', '')
        sp = Spell.objects.get(id=spell_id)
        grimoire.spells.remove(sp.id)

        spell_list = [val for val in Spell.objects.all().order_by('name') if val in grimoire.spells.all()]
        print("Removing spell {} in grimoire {}".format(spell_id, grimoire.id))
        return render(request, 'grimoire/grimoire_page.html', {
            'grimoire': grimoire, 'spell_list': spell_list, 'circles': ['1', '2', '3', '4', '5']})
