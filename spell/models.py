from django.db import models


class Enhancement(models.Model):
    cost = models.SmallIntegerField()
    effect = models.TextField()
    pass


class Spell(models.Model):

    # id = models.CharField()
    spell_name = models.CharField()
    image = models.ImageField(upload_to='spell/images')

    SPELL_TYPE_CHOICES = [
        ('AR', 'Arcana'),
        ('DI', 'Divina'),
        ('UN', 'Universal'),
    ]
    spell_type = models.CharField(
        choices=SPELL_TYPE_CHOICES,
    )

    SCHOOL_CHOICES = [
        ('AB', 'Abjuração'),
        ('AD', 'Advinhação'),
        ('CO', 'Convocação'),
        ('EN', 'Encantamento'),
        ('EV', 'Evocação'),
        ('IL', 'Ilusão'),
        ('NE', 'Necromancia'),
        ('TR', 'Transmutação'),
    ]
    school = models.CharField(
        choices=SCHOOL_CHOICES,
    )

    circle = models.SmallIntegerField()
    execution = models.CharField()
    range = models.CharField()
    target_area_effect = models.TextField()
    duration = models.CharField()
    resistance = models.CharField(blank=True)
    pass
