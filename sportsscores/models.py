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
    game_details = models.JSONField( default=default_json )


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

    

    def __str__(self):
        return self.name


from datetime import datetime
import pytz

class TeamLeague(models.Model):

    def default_json():
        return {}

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team_api_id = models.IntegerField(blank=False, default=0)
    json_data = models.JSONField(default=default_json)

    
    # Format the time for the game into a dictionary
    def format_time_soccer( self, unformattedTime ):

        time_chunks = {}

        # The int() is to convert the json into int so it
        #   can be compared to the current time dict
        time_chunks['Year'] = int(unformattedTime[0:4])
        time_chunks['Month'] = int(unformattedTime[5:7])
        time_chunks['Day'] = int(unformattedTime[8:10])
        time_chunks['Hour'] = int(unformattedTime[11:13])
        time_chunks['Minute'] = int(unformattedTime[14:16])

        return time_chunks

    # Send a game schedule to determine if the game is 
    #   in the future 
    def is_future_game(self, current_time, game_time):
        
        is_future_game = False

        if( current_time['Year'] < game_time['Year'] ):
            return True
        elif( current_time['Year'] == game_time['Year'] ):  
            if( current_time['Month'] < game_time['Month'] ):
                return True
            elif( current_time['Month'] == game_time['Month'] ):
                if( current_time['Day'] < game_time['Day'] ):
                    return True
                elif( current_time['Day'] == game_time['Day'] ):
                    if( current_time['Hour'] < game_time['Hour'] ):
                        return True
                    elif( current_time['Hour'] == game_time['Hour'] ):
                        if( current_time['Minute'] <= game_time['Minute'] ):
                            return True
        return False


    def get_next_game(self):

        # Get the current date and time
        current_time = datetime.now()

        # Breakdown the current date and time into dictionary keys
        current_time_chunks = {}
        current_time_chunks['Year'] = current_time.year
        current_time_chunks['Month'] = current_time.month
        current_time_chunks['Day'] = current_time.day
        current_time_chunks['Hour'] = current_time.hour
        current_time_chunks['Minute'] = current_time.minute
        

        for game in self.json_data:
            #print("###########################################################")
            #print(game['fixture']['date'])

            game_time_chunks = self.format_time_soccer( game['fixture']['date'] )

            #print( self.is_future_game( current_time_chunks, game_time_chunks ) )

            #print("###########################################################")

            if( self.is_future_game( current_time_chunks, game_time_chunks ) ):
                print(current_time)
                return game

        









    # We use the league/team name as the key in the context
    #   dict and it doesnt like it when key names have spaces.
    #   so this
    def get_dict_key_name(self):
        self.get_next_game()
        return self.team.name.replace(' ','_')

    class Meta:
        unique_together = ['team', 'league']

    def __str__(self):
        return self.team.name
