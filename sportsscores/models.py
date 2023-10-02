from django.db import models

# Create your models here.
# Create your models here.
class League(models.Model):

    SOCCER = "SOCCER"
    FOOTBALL = "FOOTBALL"

    SPORT_TYPE = [
        (SOCCER, "Soccer"),
        (FOOTBALL, "Football"),
    ]

    """
    api_id = models.IntegerField(blank=False, validators=[MinValueValidator(0)]),
    name = models.CharField(blank=True, max_length=50),
    sport = models.CharField(max_length=15, choices=SPORT_TYPE),
    json_data = models.JSONField()
    """

    def default_json():
        return {}

    api_id = models.IntegerField(blank=False, default=0)
    name = models.CharField(max_length=50, default="Leagaaa")
    sport = models.CharField(max_length=15, choices=SPORT_TYPE, default=SOCCER, blank=True)
    json_data = models.JSONField(default=default_json)

    def adjust_timezone(self, time_chunks, time_offset):
        days_in_month = {
            1 : 31,
            2 : 28,
            3 : 31,
            4 : 30,
            5 : 31,
            6 : 30,
            7 : 31,
            8 : 31,
            9 : 30,
            10 : 31,
            11 : 30,
            12 : 31
        }

        time_chunks['Hour'] -= time_offset

        if time_chunks['Hour'] < 0:
            time_chunks['Hour'] %= 24
            time_chunks['Day'] -= 1

            if time_chunks['Day'] <= 0:
                time_chunks['Month'] -= 1

                if time_chunks['Month'] <= 0:
                    time_chunks['Month'] = 12
                    time_chunks['Year'] -= 1

                time_chunks['Day'] = days_in_month[ time_chunks['Day'] ]

        return time_chunks

    # Format the time for the game into a dictionary
    def format_time_soccer( self, unformattedTime ):

        time_chunks = {}

        # Soccer Time Format:
        #   2023-08-11T19:00:00+00:00

        # The int() is to convert the json into int so it
        #   can be compared to the current time dict
        time_chunks['Year'] = int(unformattedTime[0:4])
        time_chunks['Month'] = int(unformattedTime[5:7])
        time_chunks['Day'] = int(unformattedTime[8:10])
        time_chunks['Hour'] = int(unformattedTime[11:13])
        time_chunks['Minute'] = int(unformattedTime[14:16])

        time_chunks = self.adjust_timezone( time_chunks, 4)

        return time_chunks


    def format_time_football( self, unformattedTime):
        time_chunks = {}

        # Soccer Time Format:
        #   2023-08-11T19:00:00+00:00

        # The int() is to convert the json into int so it
        #   can be compared to the current time dict
        time_chunks['Year'] = int(unformattedTime['date'][0:4])
        time_chunks['Month'] = int(unformattedTime['date'][5:7])
        time_chunks['Day'] = int(unformattedTime['date'][8:10])
        time_chunks['Hour'] = int(unformattedTime['time'][0:2])
        time_chunks['Minute'] = int(unformattedTime['time'][3:5])

        time_chunks = self.adjust_timezone( time_chunks, 4)

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
        print("Finding next game...")

        # Get the current date and time
        current_time = datetime.now()

        # Breakdown the current date and time into dictionary keys
        current_time_chunks = {}
        current_time_chunks['Year'] = current_time.year
        current_time_chunks['Month'] = current_time.month
        current_time_chunks['Day'] = current_time.day
        current_time_chunks['Hour'] = current_time.hour
        current_time_chunks['Minute'] = current_time.minute
        

        all_team_IDs = []
        all_next_games = []

        # Get all team IDs
        for j in self.json_data:
            if j['teams']['home']['id'] != 0 and j['teams']['away']['id'] != 0:
                if j['teams']['home']['id'] not in all_team_IDs:
                    all_team_IDs.append( j['teams']['home']['id'] )
                if j['teams']['away']['id'] not in all_team_IDs:
                    all_team_IDs.append( j['teams']['away']['id'] )

        print("ALL NEXT GAMES \n\n")
        print(all_team_IDs)
        # Get the next game for each team
        for team_ID in all_team_IDs:
            print("TEAM ID: ", team_ID)
            for game in self.json_data:
                if( game['teams']['home']['id'] == team_ID or game['teams']['away']['id'] == team_ID ):
                    print("\n\n",self.sport)
                    if( self.sport == "SOCCER"):
                        game_time_chunks = self.format_time_soccer( game['fixture']['date'] )
                    elif( self.sport == "FOOTBALL"):
                        game_time_chunks = self.format_time_football( game['game']['date'] )
                        

                    if( self.is_future_game( current_time_chunks, game_time_chunks ) ):
                        all_next_games.append( game )

                        print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                        print(game)
                        print( game_time_chunks )
                        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
                        
                        break


        unique_game_list = [item for index, item in enumerate(all_next_games) if item not in all_next_games[:index]]
        
        print( unique_game_list )

        return unique_game_list

        

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
        #print("Finding next game...")

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
