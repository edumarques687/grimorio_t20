"""Grimorio_T20 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = 'spell'

urlpatterns = [
    path('', views.spell_page, name='spells_page'),
    # path('copysortingname/', views.copy_sorting_name, name='copy_sorting_name'),
    path('<int:spell_id>/', views.spell_details, name='spell_details'),
    path('add_spell/<int:spell_id>/', views.add_shared_spell, name='add_shared_spell'),
    path('remove_spell/<int:spell_id>/', views.remove_shared_spell, name='remove_shared_spell'),
    # path('create_spell/', views.create_spell, name='create_spell'),
]
