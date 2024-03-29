# Generated by Django 3.1.5 on 2021-03-06 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spell', '0006_auto_20210306_0245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enhancement',
            old_name='spell',
            new_name='related_spell',
        ),
        migrations.AddField(
            model_name='spell',
            name='enhancements',
            field=models.ManyToManyField(related_name='spell', to='spell.Enhancement'),
        ),
        migrations.AlterField(
            model_name='enhancement',
            name='cost',
            field=models.CharField(max_length=20),
        ),
    ]
