from django.shortcuts import render, get_object_or_404, redirect
from spell.models import Spell, Enhancement, SpellForm
from django.db.models import Q
from grimoire.models import Grimoire
# import unidecode


def spell_page(request):
    user_grimoires = False
    rip = False
    if request.user.is_authenticated:
        user_grimoires = Grimoire.objects.filter(user=request.user).all().order_by('name')

        Lagrimas = ['Kasu','eduardo_marques1','EichelbaumElvis','silquelado', 'gionin@terra.com.br']
        if request.user.get_username() in Lagrimas:
            rip = True

    if request.method == 'GET':

        query = Q(user='1')
        if request.user.is_authenticated:
            query |= Q(user=request.user)
            query |= Q(shared_users__icontains=';' + request.user.get_username() + ';')
        spells = Spell.objects.filter(query).order_by('sorting_name')

        query = Q()
        query &= Q()
        type_filters = ['AR', 'DI', 'UN']
        school_filters = ['AB', 'AD', 'CO', 'EN', 'EV', 'IL', 'NE', 'TR']
        for key, value in request.GET.items():
            if value != '':
                if 'type' in key and value != '':
                    if any(value in s for s in type_filters):
                        query |= Q(spell_type__icontains=value)
        spells = spells.filter(query).order_by('sorting_name')
        query = Q()

        for key, value in request.GET.items():
            if value != '':
                if key == 'keyword' and value != '':
                    kw_list = value.split(';')
                    for kw in kw_list:
                        query |= Q(name__icontains=kw)
                        query |= Q(enhancement__cost__icontains=kw)
                        query |= Q(description__icontains=kw)
                        query |= Q(enhancement__effect__icontains=kw)
                    spells = spells.filter(query).distinct()
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
                if key == 'range' and value != '':
                    query &= Q(range__icontains=value)
                if key == 'target_area_effect' and value != '':
                    query &= Q(target_area_effect__icontains=value)
                if key == 'resistance' and value != '':
                    query &= Q(resistance__icontains=value)
                if key == 'book_magazine' and value != '':
                    query &= Q(book_magazine__icontains=value)

        spells = spells.filter(query).order_by('sorting_name').distinct()
        origins = []
        for spell in spells:
            spell_origin = spell.book_magazine
            if spell_origin not in origins:
                origins.append(spell_origin)
        return render(request, 'spell/spells_page.html', {'spells': spells,
                                                          'circles': ['1', '2', '3', '4', '5'],
                                                          'user_grimoires': user_grimoires,
                                                          'origins': origins,
                                                          'rip': rip,
                                                          })


def spell_details(request, spell_id):
    spell = get_object_or_404(Spell, pk=spell_id)
    enhancements = Enhancement.objects.filter(related_spell=spell_id)
    return render(request, 'spell/spell_details.html', {'spell': spell, 'enhancements': enhancements})


def create_spell(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
#    if request.method == 'GET':
    return render(request, 'spell/create_spell.html', {'form': SpellForm()})


def add_shared_spell(request, spell_id):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    spell = get_object_or_404(Spell, pk=spell_id)
    user = (';' + request.user.get_username() + ';')
    message = ''
    if spell.book_magazine == 'Homebrew':
        if spell.user != request.user:
            if user not in spell.shared_users:
                spell.shared_users += user
                spell.save()
                message = "Magia '" + spell.name + "' adicionada."
            else:
                message = 'Você já adicionou está magia.'
        else:
            message = 'Para adicionar uma magia, você não pode ser o criador dela.'
    else:
        message = 'Para adicionar uma magia, ela deve ser Homebrew.'
    return render(request, 'spell/add_shared_spell.html', {'spell': spell, 'creator': spell.user.username, 'message': message})

def remove_shared_spell(request, spell_id):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    spell = get_object_or_404(Spell, pk=spell_id)
    user = (';' + request.user.get_username() + ';')
    if spell.book_magazine == 'Homebrew':
        if spell.user != request.user:
            if user in spell.shared_users:
                spell.shared_users = spell.shared_users.replace(user, '')
                spell.save()
    return redirect('/')



# def copy_sorting_name(request):
#     spells = Spell.objects.order_by('name').all()
#     for spell in spells:
#         spell.sorting_name = unidecode.unidecode(spell.name)
#         spell.save()
#     return render(request, 'homepage/home.html', {'response': 'sorting names copied'})
