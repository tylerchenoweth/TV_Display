from django.db import models
from django.contrib.postgres.fields import ArrayField



# Create your models here.

class League(models.Model):

    SOCCER = "SOCCER"
    FOOTBALL = "FOOTBALL"

    SPORT_TYPE = [
        (SOCCER, "Soccer"),
        (FOOTBALL, "Football"),
    ]


    api_id = models.IntegerField()
    api_source = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    sport = models.CharField(max_length=255, choices=SPORT_TYPE)
    raw_json = models.JSONField()
    #teams = models.ManyToManyField('Team', related_name='league')
    logo = models.ImageField(upload_to='logos_folder/')
    # , default='default_image.png'


    def __str__(self):
        return self.name

class Team(models.Model):


    api_id = models.IntegerField()
    api_source = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    league = models.ManyToManyField(League, related_name='teams')
    logo = models.ImageField(upload_to='logos_folder/')
    # , default='default_image.png'
    

    def __str__(self):
        return self.name


from datetime import datetime
import pytz

class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    date = models.DateTimeField()