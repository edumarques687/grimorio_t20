# Generated by Django 3.0.5 on 2021-05-29 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grimoire', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grimoire',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
