# Generated by Django 2.0.13 on 2019-03-30 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='branch',
        ),
        migrations.AddField(
            model_name='volunteer',
            name='field',
            field=models.CharField(default='', max_length=20),
        ),
    ]
