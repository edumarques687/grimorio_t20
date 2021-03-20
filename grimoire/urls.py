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

app_name = 'grimoire'

urlpatterns = [
    path('', views.grimoire_page, name='grimoire_page'),
    path('g/', views.grimoire_list, name='grimoire_list'),
    path('addspells/', views.add_spells, name='add_spells'),
    path('removespell/', views.remove_spell, name='remove_spell')
]
