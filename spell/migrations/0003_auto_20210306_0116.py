# Generated by Django 3.1.5 on 2021-03-06 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spell', '0002_auto_20210304_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enhancement',
            name='cost',
            field=models.TextField(),
        ),
    ]