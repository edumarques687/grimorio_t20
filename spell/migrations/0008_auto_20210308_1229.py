# Generated by Django 3.1.5 on 2021-03-08 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spell', '0007_auto_20210306_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spell',
            name='circle',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, max_length=1),
        ),
        migrations.AlterField(
            model_name='spell',
            name='enhancements',
            field=models.ManyToManyField(blank=True, related_name='spell', to='spell.Enhancement'),
        ),
        migrations.AlterField(
            model_name='spell',
            name='school',
            field=models.CharField(choices=[('AB', 'Abjuração'), ('AD', 'Advinhação'), ('CO', 'Convocação'), ('EN', 'Encantamento'), ('EV', 'Evocação'), ('IL', 'Ilusão'), ('NE', 'Necromancia'), ('TR', 'Transmutação')], default='AB', max_length=2),
        ),
        migrations.AlterField(
            model_name='spell',
            name='spell_type',
            field=models.CharField(choices=[('AR', 'Arcana'), ('DI', 'Divina'), ('UN', 'Universal')], default='AR', max_length=2),
        ),
        migrations.CreateModel(
            name='Grimoire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('spells', models.ManyToManyField(blank=True, related_name='grimoire', to='spell.Spell')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]