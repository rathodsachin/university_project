# Generated by Django 2.1.2 on 2018-10-30 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]
