# Generated by Django 4.2.3 on 2023-09-26 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsscores', '0003_team_api_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='api_id',
        ),
        migrations.AddField(
            model_name='teamleague',
            name='team_api_id',
            field=models.IntegerField(default=0),
        ),
    ]
