from django.shortcuts import render, get_object_or_404, redirect
from spell.models import Spell, Enhancement, SpellForm
from django.db.models import Q
from grimoire.models import Grimoire
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import escape
import json
import re
import markdown
from bleach import clean


def sanitize_input(text, allow_markdown=False):
    """
    Sanitize user input to prevent XSS and SQL injection attacks.
    
    Args:
        text: The text to sanitize
        allow_markdown: If True, allows safe markdown/HTML tags
    
    Returns:
        Sanitized text string
    """
    if not text:
        return text
    
    # Remove any SQL injection attempts
    sql_patterns = [
        r'(\bUNION\b.*\bSELECT\b)',
        r'(\bDROP\b.*\bTABLE\b)',
        r'(\bINSERT\b.*\bINTO\b)',
        r'(\bDELETE\b.*\bFROM\b)',
        r'(\bUPDATE\b.*\bSET\b)',
        r'(;.*--)',
        r'(\'.*OR.*\'.*=.*\')',
    ]
    
    for pattern in sql_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove script tags and dangerous attributes
    if allow_markdown:
        # Allow safe HTML tags for markdown rendering
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img', 'table',
            'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'i', 'b'
        ]
        allowed_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title'],
            '*': ['class']
        }
        # Clean HTML but allow safe tags
        text = clean(text, tags=allowed_tags, attributes=allowed_attributes, strip=True)
    else:
        # For non-markdown fields, escape all HTML
        text = escape(text)
    
    return text


def render_markdown(text):
    """
    Convert markdown text to HTML with sanitization.
    
    Args:
        text: Markdown text to convert
    
    Returns:
        Safe HTML string
    """
    if not text:
        return text
    
    # Convert markdown to HTML
    html = markdown.markdown(text, extensions=['extra', 'nl2br'])
    
    # Sanitize the output
    html = sanitize_input(html, allow_markdown=True)
    
    return html


def spell_page(request):
    user_grimoires = False
    rip = False
    if request.user.is_authenticated:
        user_grimoires = Grimoire.objects.filter(user=request.user).all().order_by('name')

        Lagrimas = ['Kasu','eduardo_marques1','EichelbaumElvis','silquelado', 'gionin@terra.com.br']
        if request.user.get_username() in Lagrimas:
            rip = True

    if request.method == 'GET':

        query = Q(user='248')
        if request.user.is_authenticated:
            query |= Q(user=request.user)
            query |= Q(shared_users__icontains=';' + request.user.get_username() + ';')
        
        # Check if filtering for public homebrew spells only
        if request.GET.get('public_only') == 'true':
            # Show all homebrew spells (public and non-public) if user is eduardo_marques1
            if request.user.is_authenticated and request.user.get_username() == 'eduardo_marques1':
                query |= Q(book_magazine='Homebrew')
            else:
                query |= Q(public=True, book_magazine='Homebrew')
        
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
    try:
        spell = Spell.objects.get(pk=spell_id)
    except Spell.DoesNotExist:
        return render(request, 'spell/spell_not_found.html')
    
    enhancements = Enhancement.objects.filter(related_spell=spell_id)
    is_homebrew = bool(True if spell.user.username != "GrimorioT20" else False)
    if is_homebrew:
        # Allow access if spell is public
        if spell.public:
            return render(request, 'spell/spell_details.html', {'spell': spell,
                                                                'enhancements': enhancements, 'is_homebrew': is_homebrew})
        # Allow access for eduardo_marques1 even if spell is not public
        if request.user.is_authenticated and request.user.get_username() == 'eduardo_marques1':
            return render(request, 'spell/spell_details.html', {'spell': spell,
                                                                'enhancements': enhancements, 'is_homebrew': is_homebrew})
        # Otherwise require authentication and shared access
        if not request.user.is_authenticated:
            return redirect('loginuser')
        if request.user.is_authenticated and request.user.get_username() not in spell.shared_users:
            return render(request, 'spell/access_denied.html')
    return render(request, 'spell/spell_details.html', {'spell': spell,
                                                        'enhancements': enhancements, 'is_homebrew': is_homebrew})


def create_spell(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    
    if request.method == 'POST':
        try:
            # Process shared users
            shared_users_input = request.POST.get('shared_users', '').strip()
            shared_users_list = []
            
            # Always include the creator
            shared_users_list.append(request.user.get_username())
            
            # Parse comma-separated usernames
            if shared_users_input:
                # Split by comma, strip whitespace, remove empty strings
                usernames = [username.strip() for username in shared_users_input.split(',')]
                usernames = [username for username in usernames if username]
                
                # Validate usernames exist and add them
                for username in usernames:
                    if User.objects.filter(username=username).exists():
                        if username not in shared_users_list:
                            shared_users_list.append(username)
            
            # Format as ;username1;;username2;
            shared_users_formatted = ';' + ';'.join(shared_users_list) + ';'
            
            # Get public field value (checkbox returns 'on' if checked, None if not)
            is_public = request.POST.get('public') == 'on'
            
            # Sanitize inputs
            name = sanitize_input(request.POST.get('name', ''))
            execution = sanitize_input(request.POST.get('execution', ''))
            range_val = sanitize_input(request.POST.get('range', ''))
            target_area_effect = sanitize_input(request.POST.get('target_area_effect', ''))
            duration = sanitize_input(request.POST.get('duration', ''))
            resistance = sanitize_input(request.POST.get('resistance', ''))
            # Description allows HTML tags
            description = sanitize_input(request.POST.get('description', ''), allow_markdown=True)
            
            # Create the spell
            spell = Spell(
                name=name,
                sorting_name=name.replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('é', 'e').replace('á', 'a').replace('í', 'i').replace('ó', 'o').replace('ú', 'u'),
                spell_type=request.POST.get('spell_type:', 'AR'),
                circle=request.POST.get('circle:', '1'),
                school=request.POST.get('school:', 'AB'),
                execution=execution,
                range=range_val,
                target_area_effect=target_area_effect,
                duration=duration,
                resistance=resistance,
                description=description,
                book_magazine='Homebrew',
                user=request.user,
                shared_users=shared_users_formatted,
                public=is_public
            )
            spell.save()
            
            # Create enhancements
            enhancement_index = 0
            while True:
                cost_key = f'enhancement_cost_{enhancement_index}'
                effect_key = f'enhancement_effect_{enhancement_index}'
                
                if cost_key not in request.POST:
                    break
                
                cost = sanitize_input(request.POST.get(cost_key, '').strip())
                effect = sanitize_input(request.POST.get(effect_key, '').strip(), allow_markdown=True)
                
                # Only create enhancement if both cost and effect are provided
                if cost and effect:
                    enhancement = Enhancement(
                        cost=cost,
                        effect=effect,
                        related_spell=spell
                    )
                    enhancement.save()
                
                enhancement_index += 1
            
            return redirect('spell:spell_details', spell_id=spell.id)
        
        except Exception as e:
            return render(request, 'spell/create_spell.html', {'form': SpellForm(), 'error': f'Erro ao criar magia: {str(e)}'})
    
    return render(request, 'spell/create_spell.html', {'form': SpellForm()})


def edit_spell(request, spell_id):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    
    spell = get_object_or_404(Spell, pk=spell_id)
    
    # Check if user is the owner
    if spell.user != request.user:
        return render(request, 'spell/access_denied.html')
    
    # Check if it's a homebrew spell
    if spell.book_magazine != 'Homebrew':
        return render(request, 'spell/access_denied.html')
    
    if request.method == 'POST':
        try:
            # Process shared users
            shared_users_input = request.POST.get('shared_users', '').strip()
            shared_users_list = []
            
            # Always include the creator
            shared_users_list.append(request.user.get_username())
            
            # Parse comma-separated usernames
            if shared_users_input:
                usernames = [username.strip() for username in shared_users_input.split(',')]
                usernames = [username for username in usernames if username]
                
                for username in usernames:
                    if User.objects.filter(username=username).exists():
                        if username not in shared_users_list:
                            shared_users_list.append(username)
            
            # Format as ;username1;;username2;
            shared_users_formatted = ';' + ';'.join(shared_users_list) + ';'
            
            # Get public field value (checkbox returns 'on' if checked, None if not)
            is_public = request.POST.get('public') == 'on'
            
            # Sanitize inputs
            name = sanitize_input(request.POST.get('name', ''))
            execution = sanitize_input(request.POST.get('execution', ''))
            range_val = sanitize_input(request.POST.get('range', ''))
            target_area_effect = sanitize_input(request.POST.get('target_area_effect', ''))
            duration = sanitize_input(request.POST.get('duration', ''))
            resistance = sanitize_input(request.POST.get('resistance', ''))
            # Description allows HTML tags
            description = sanitize_input(request.POST.get('description', ''), allow_markdown=True)
            
            # Update the spell
            spell.name = name
            spell.sorting_name = name.replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('é', 'e').replace('á', 'a').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            spell.spell_type = request.POST.get('spell_type:', 'AR')
            spell.circle = request.POST.get('circle:', '1')
            spell.school = request.POST.get('school:', 'AB')
            spell.execution = execution
            spell.range = range_val
            spell.target_area_effect = target_area_effect
            spell.duration = duration
            spell.resistance = resistance
            spell.description = description
            spell.shared_users = shared_users_formatted
            spell.public = is_public
            spell.save()
            
            # Delete all existing enhancements
            Enhancement.objects.filter(related_spell=spell).delete()
            
            # Create new enhancements
            enhancement_index = 0
            while True:
                cost_key = f'enhancement_cost_{enhancement_index}'
                effect_key = f'enhancement_effect_{enhancement_index}'
                
                if cost_key not in request.POST:
                    break
                
                cost = sanitize_input(request.POST.get(cost_key, '').strip())
                effect = sanitize_input(request.POST.get(effect_key, '').strip(), allow_markdown=True)
                
                if cost and effect:
                    enhancement = Enhancement(
                        cost=cost,
                        effect=effect,
                        related_spell=spell
                    )
                    enhancement.save()
                
                enhancement_index += 1
            
            return redirect('spell:spell_details', spell_id=spell.id)
        
        except Exception as e:
            enhancements = Enhancement.objects.filter(related_spell=spell)
            return render(request, 'spell/edit_spell.html', {
                'spell': spell,
                'enhancements': enhancements,
                'error': f'Erro ao editar magia: {str(e)}'
            })
    
    # GET request - display the edit form
    enhancements = Enhancement.objects.filter(related_spell=spell)
    
    # Format shared_users for display (remove creator and format as comma-separated)
    shared_users_list = [u for u in spell.shared_users.split(';') if u and u != request.user.get_username()]
    shared_users_display = ', '.join(shared_users_list)
    
    return render(request, 'spell/edit_spell.html', {
        'spell': spell,
        'enhancements': enhancements,
        'shared_users_display': shared_users_display
    })


def delete_spell(request, spell_id):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    
    spell = get_object_or_404(Spell, pk=spell_id)
    
    # Check if user is the owner
    if spell.user != request.user:
        return render(request, 'spell/access_denied.html')
    
    # Check if it's a homebrew spell
    if spell.book_magazine != 'Homebrew':
        return render(request, 'spell/access_denied.html')
    
    # Delete the spell (this will also delete related enhancements due to CASCADE)
    spell.delete()
    
    # Redirect to spell list page
    return redirect('spell:spells_page')


def add_shared_spell(request, spell_id):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    spell = get_object_or_404(Spell, pk=spell_id)
    user = (';' + request.user.get_username() + ';')
    if spell.book_magazine == 'Homebrew':
        if spell.user != request.user:
            if user not in spell.shared_users:
                spell.shared_users += user
                spell.save()
    return redirect('spell:spell_details', spell_id=spell_id)

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
    return redirect('spell:spell_details', spell_id=spell_id)

def create_json(request):
    query = Q(user='248')
    if request.user.is_authenticated:
        query |= Q(user=request.user)
        query |= Q(shared_users__icontains=';' + request.user.get_username() + ';')
    spells = Spell.objects.filter(query).order_by('sorting_name')

    result = '[<br>'
    spell_pos = -1
    for sp in spells:
        spell_pos += 1
        result += '{<br>'
        result += '"grupo":"' + sp.get_spell_type_display() + '",<br>'
        result += '"nome":"' + sp.name + '",<br>'
        result += '"circulo":' + str(sp.get_circle_display()) + ',<br>'
        result += '"escola":"' + sp.get_school_display() + '",<br>'
        result += '"execucao":"' + sp.execution + '",<br>'
        result += '"alcance":"' + sp.range + '",<br>'
        result += '"alvo":"' + sp.target_area_effect + '",<br>'
        result += '"duracao":"' + sp.duration + '",<br>'
        result += '"resistencia":"' + sp.resistance + '",<br>'
        result += '"publicacao":"' + sp.book_magazine + '",<br>'
        result += '"descricao":"' + sp.description.replace('<br>', '').replace('</p>', '').replace('</i>', '').replace('<i>', '').replace('<p>', '').replace('\n', '').replace('', '') + '",<br>'
        result += '"Aprimoramentos": ['

        enhancements = Enhancement.objects.filter(related_spell=sp.id)
        en_pos = -1
        for ap in enhancements:
            en_pos += 1
            result += '<br>{<br>"Custo":"' + ap.cost + '",<br>"descricao":"' + ap.effect.replace('<br>', '').replace('</p>', '').replace('</i>', '').replace('<i>', '').replace('<p>', '').replace('\n', '').replace('', '') + '"<br>}'
            if en_pos != len(enhancements) -1:
                result += ','

        if spell_pos == len(spells) -1:
            result += ']<br>}<br>'
        else:
            result += ']<br>},<br>'
    result += ']'
    return HttpResponse(result)

def upload_spells(request):
    file_path = settings.STATIC_ROOT + '/spells.json'
    user = get_object_or_404(User, pk=248)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        spells = []
        for item in data:
            nome = item['nome']

            if 'Resistência' not in item:
                resist = 'nenhuma'
            else:
                resist = item['Resistência']

            spell = Spell(
                name=item['nome'],
                sorting_name=item['nome'].replace('ç', 'c').replace('ã','a').replace('õ','o'),
                circle=item['Circulo'],
                execution=item['Execução'].lower(),
                range=item['Alcance'].lower(),
                target_area_effect=item['Alvo/Área/Efeito'].lower(),
                duration=item['Duração'].lower(),
                book_magazine=item['Publicação'],
                description=item['Efeito'],
                resistance=resist,
                user=user
            )

            if item['tipo'] == 'Divina':
                spell.spell_type = 'DI'
            if item['tipo'] == 'Arcana':
                spell.spell_type = 'AR'
            if item['tipo'] == 'Universal':
                spell.spell_type = 'UN'
            if item['Escola'] == 'Abjuração':
                spell.school = 'AB'
            if item['Escola'] == 'Adivinhação':
                spell.school = 'AD'
            if item['Escola'] == 'Convocação':
                spell.school = 'CO'
            if item['Escola'] == 'Encantamento':
                spell.school = 'EN'
            if item['Escola'] == 'Evocação':
                spell.school = 'EV'
            if item['Escola'] == 'Ilusão':
                spell.school = 'IL'
            if item['Escola'] == 'Necromancia':
                spell.school = 'NE'
            if item['Escola'] == 'Transmutação':
                spell.school = 'TR'

            spells.append(spell)
        Spell.objects.bulk_create(spells)
        return JsonResponse({'message': f'{len(spells)} books added successfully!'})

# def copy_sorting_name(request):
#     spells = Spell.objects.order_by('name').all()
#     for spell in spells:
#         spell.sorting_name = unidecode.unidecode(spell.name)
#         spell.save()
#     return render(request, 'homepage/home.html', {'response': 'sorting names copied'})
