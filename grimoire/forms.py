from django.forms import ModelForm
from .models import Grimoire


class GrimoireForm(ModelForm):
    class Meta:
        model = Grimoire
        fields = ['name']
