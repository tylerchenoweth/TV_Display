# Generated by Django 4.2.3 on 2023-09-26 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsscores', '0002_team_teamleague'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='api_id',
            field=models.IntegerField(default=0),
        ),
    ]
