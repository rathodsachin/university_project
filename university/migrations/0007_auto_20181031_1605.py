# Generated by Django 2.1 on 2018-10-31 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0006_auto_20181031_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='password1',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='students',
            name='user_name',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
