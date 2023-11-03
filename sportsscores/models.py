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


    def default_json():
        return {}

    def default_game_details():
        details = [
            {
                "Display_Name" : None,
                "teams" : { 
                    "home" : None,
                    "away" : None,
                },
                "datetime" : {
                    "year" : None,
                    "month" : None,
                    "day" : None,
                    "hour" : None,
                    "minute" : None
                }
            }
        ]

        return details


    api_id = models.IntegerField(blank=False, default=0)
    name = models.CharField(max_length=50, default="Leagaaa")
    sport = models.CharField(max_length=15, choices=SPORT_TYPE, default=SOCCER, blank=True)
    json_data = models.JSONField(default=default_json)
    game_details = models.JSONField( default=default_json, blank=True )
    logo = models.ImageField(upload_to='logos_folder/', default='default_image.png')


    def get_raw_league_schedule(self):
        return self.json_data

    def get_game_details(self):
        return self.game_details

    def set_game_details(self, updated_game_details):
        self.game_details = updated_game_details


    def get_dict_key_name(self):
        return self.name.replace(' ','_')

    def __str__(self):
        return self.name






class Team(models.Model):

    SOCCER = "SOCCER"
    FOOTBALL = "FOOTBALL"

    SPORT_TYPE = [
        (SOCCER, "Soccer"),
        (FOOTBALL, "Football"),
    ]

    name = models.CharField(max_length=50)
    sport = models.CharField(max_length=15, choices=SPORT_TYPE, default=SOCCER, blank=True)
    api_id = ArrayField( models.IntegerField(blank=False, default=0) )
    # New additions
    logo = models.ImageField(upload_to='logos_folder/', default='default_image.png')
    



    

    def __str__(self):
        return self.name


from datetime import datetime
import pytz


