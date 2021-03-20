from django.db import models
from spell.models import Spell
from django.contrib.auth.models import User


class Grimoire(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spells = models.ManyToManyField(to=Spell, related_name='grimoire', blank=True)

    def id(self):
        return self.id

    def __str__(self):
        return str(self.name) + ' (' + self.user.username + ')'
