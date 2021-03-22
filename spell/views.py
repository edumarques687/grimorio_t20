from django.shortcuts import render, get_object_or_404
from spell.models import Spell, Enhancement
from django.db.models import Q
from grimoire.models import Grimoire


def spell_page(request):
    user_grimoires = False
    if request.user.is_authenticated:
        user_grimoires = Grimoire.objects.filter(user=request.user).all().order_by('name')
    spells = Spell.objects.order_by('name').all()
    if request.method == 'GET':
        query = Q()
        query &= Q()
        type_filters = ['AR', 'DI', 'UN']
        school_filters = ['AB', 'AD', 'CO', 'EN', 'EV', 'IL', 'NE', 'TR']
        query_type = ['']
        for key, value in request.GET.items():
            if value != '':
                if 'type' in key and value != '':
                    if any(value in s for s in type_filters):
                        query |= Q(spell_type__icontains=value)
        spells = Spell.objects.filter(query).all()
        query = Q()
        for key, value in request.GET.items():
            if value != '':
                if 'school' in key and value != '':
                    if any(value in s for s in school_filters):
                        query |= Q(school__icontains=value)
                if key == 'execution' and value != '':
                    query &= Q(execution__icontains=value)
                if key == 'duration' and value != '':
                    query &= Q(duration__icontains=value)
                if key == 'target_area_effect' and value != '':
                    query &= Q(target_area_effect__icontains=value)
                if key == 'resistance' and value != '':
                    query &= Q(resistance__icontains=value)
                if key == 'book_magazine' and value != '':
                    query &= Q(book_magazine__icontains=value)
                print(query)

        spells = spells.filter(query).all()
        origins = []
        for spell in spells:
            spell_origin = spell.book_magazine
            if spell_origin not in origins:
                origins.append(spell_origin)
        return render(request, 'spell/spells_page.html', {'spells': spells,
                                                      'circles': ['1', '2', '3', '4', '5'],
                                                      'user_grimoires': user_grimoires,
                                                      'origins': origins})


def spell_details(request, spell_id):
    spell = get_object_or_404(Spell, pk=spell_id)
    enhancements = Enhancement.objects.filter(related_spell=spell_id)
    return render(request, 'spell/spell_details.html', {'spell': spell, 'enhancements': enhancements})
