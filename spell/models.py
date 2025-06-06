from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Enhancement(models.Model):
    cost = models.CharField(max_length=100)
    effect = models.TextField()
    related_spell = models.ForeignKey('Spell', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return 'Related to: ' + self.related_spell.name


class Spell(models.Model):

    name = models.TextField()
    sorting_name = models.TextField(blank=True)
    image = models.ImageField(upload_to='spell/images', blank=True)

    SPELL_TYPE_CHOICES = [
        ('AR', 'Arcana'),
        ('DI', 'Divina'),
        ('UN', 'Universal'),
    ]
    spell_type = models.CharField(
        max_length=2,
        choices=SPELL_TYPE_CHOICES,
        default='AR',
    )

    SCHOOL_CHOICES = [
        ('AB', 'Abjuração'),
        ('AD', 'Adivinhação'),
        ('CO', 'Convocação'),
        ('EN', 'Encantamento'),
        ('EV', 'Evocação'),
        ('IL', 'Ilusão'),
        ('NE', 'Necromancia'),
        ('TR', 'Transmutação'),
    ]
    school = models.CharField(
        max_length=2,
        choices=SCHOOL_CHOICES,
        default='AB',
    )

    CIRCLE_CHOICES = [
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    ]

    circle = models.CharField(
        max_length=1,
        choices=CIRCLE_CHOICES,
        default=1,
    )

    execution = models.TextField()
    range = models.TextField()
    target_area_effect = models.TextField()
    duration = models.TextField()
    resistance = models.TextField(blank=True)
    description = models.TextField(default='')
    enhancements = models.ManyToManyField(to=Enhancement, related_name='spell', blank=True)
    short_description = models.CharField(max_length=100, blank=True)
    book_magazine = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shared_users = models.TextField(blank=True)

    def id(self):
        return self.id

    def __str__(self):
        return self.name


class SpellForm(ModelForm):
    class Meta:
        model = Spell
        fields = ['name', 'spell_type', 'school', 'circle', 'execution', 'range', 'target_area_effect', 'duration', 'resistance', 'description']

