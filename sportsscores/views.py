from django.shortcuts import render

from django.http import HttpResponse

import requests
import json

from django.utils import timezone

import datetime
import calendar

import pytz

from .models import League, Team, TeamLeague

timezone = pytz.timezone('America/New_York')

from itertools import zip_longest

from datetime import datetime
import pytz














def adjust_timezone(time_chunks, time_offset):
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

            time_chunks['Day'] = days_in_month[ time_chunks['Month'] ]

    return time_chunks

def get_day_of_week(given_date):
    import datetime
    import calendar

# Format the time for the game into a dictionary
def format_time_soccer(unformattedTime ):

    import datetime
    import calendar

    time_chunks = {}

    given_date = datetime.date(
        int(unformattedTime[0:4]),
        int(unformattedTime[5:7]),
        int(unformattedTime[8:10])
    )

    day_of_week_abbreviation = {
        "Sunday" : "Sun",
        "Monday" : "Mon",
        "Tuesday" : "Tue",
        "Wednesday" : "Wed",
        "Thursday" : "Thu",
        "Friday" : "Fri",
        "Saturday" : "Sat",
    }

    num_to_month = {
        1 : "Jan",
        2 : "Feb",
        3 : "Mar",
        4 : "Apr",
        5 : "May",
        6 : "Jun",
        7 : "Jul",
        8 : "Aug",
        9 : "Sep",
        10 : "Oct",
        11 : "Nov",
        12 : "Dec",
    }

    # Soccer Time Format:
    #   2023-08-11T19:00:00+00:00

    # The int() is to convert the json into int so it
    #   can be compared to the current time dict
    time_chunks['Year'] = int(unformattedTime[0:4])
    time_chunks['Month'] = int(unformattedTime[5:7])
    time_chunks['Month_Name'] = num_to_month[ int(unformattedTime[5:7]) ]
    time_chunks['Day'] = int(unformattedTime[8:10])
    time_chunks['Hour'] = int(unformattedTime[11:13])
    time_chunks['Minute_0'] = int(unformattedTime[14:15])
    time_chunks['Minute_1'] = int(unformattedTime[15:16])
    time_chunks['Day_of_Week'] = day_of_week_abbreviation[ given_date.strftime("%A") ]

    time_chunks = adjust_timezone( time_chunks, 4)

    return time_chunks


def format_time_football(unformattedTime):

    import datetime
    import calendar
    
    time_chunks = {}

    given_date = datetime.date(
        int(unformattedTime['date'][0:4]),
        int(unformattedTime['date'][5:7]),
        int(unformattedTime['date'][8:10])
    )

    # Soccer Time Format:
    #   2023-08-11T19:00:00+00:00

    # The int() is to convert the json into int so it
    #   can be compared to the current time dict
    time_chunks['Year'] = int(unformattedTime['date'][0:4])
    time_chunks['Month'] = int(unformattedTime['date'][5:7])
    time_chunks['Day'] = int(unformattedTime['date'][8:10])
    time_chunks['Hour'] = int(unformattedTime['time'][0:2])
    time_chunks['Minute_0'] = int(unformattedTime['time'][3:4])
    time_chunks['Minute_1'] = int(unformattedTime['time'][4:5])
    time_chunks['Day_of_Week'] = given_date.strftime("%A")

    time_chunks = adjust_timezone( time_chunks, 4)

    return time_chunks


# Send a game schedule to determine if the game is 
#   in the future 
def is_future_game(current_time, game_time):
    
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






def get_next_games_raw_json( raw_league_schedule, sport ):
    print("Finding next games...")

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
    for j in raw_league_schedule:
        if j['teams']['home']['id'] != 0 and j['teams']['away']['id'] != 0:
            if j['teams']['home']['id'] not in all_team_IDs:
                all_team_IDs.append( j['teams']['home']['id'] )
            if j['teams']['away']['id'] not in all_team_IDs:
                all_team_IDs.append( j['teams']['away']['id'] )

    print("ALL NEXT GAMES \n\n")
    print(all_team_IDs)

    # Get the next game for each team
    for team_ID in all_team_IDs:
        for game in raw_league_schedule:
            if( game['teams']['home']['id'] == team_ID or game['teams']['away']['id'] == team_ID ):
                
                if( sport == "SOCCER"):
                    game_time_chunks = format_time_soccer( game['fixture']['date'] )
                elif( sport == "FOOTBALL"):
                    game_time_chunks = format_time_football( game['game']['date'] )
                    
                if( is_future_game( current_time_chunks, game_time_chunks ) ):
                    all_next_games.append( game )
                    
                    break

    # Filter the duplicate games out of the list
    unique_game_list = [item for index, item in enumerate(all_next_games) if item not in all_next_games[:index]]

    # Return next games in raw json form
    return unique_game_list


def abbreviate_long_team_names(games):

    long_team_names = {
        "Manchester City" : "Man City",
        "Manchester United" : "Man United",
        "Nottingham Forest" : "Nottm Forest",
    }

    for g in games:
        if(g['Teams']['Home'] in long_team_names):
            g['Teams']['Home'] = long_team_names[g['Teams']['Home']]
        if(g['Teams']['Away'] in long_team_names):
            g['Teams']['Away'] = long_team_names[g['Teams']['Away']]

    return games



def get_next_games_display(league_obj):

    # Format the raw json for each individual game into a dict
    def format_game(raw_json):

        date_time = {}

        if( league_obj.sport == "SOCCER"):
            date_time = format_time_soccer( raw_json['fixture']['date'] )
        elif( league_obj.sport == "FOOTBALL"):
            date_time = format_time_football( raw_json['game']['date'] )

        formatted_json = {
            "Display_Name" : league_obj.name,
            "Teams" : {
                "Home" : raw_json['teams']['home']['name'],
                "Away" : raw_json['teams']['away']['name'],
            },

            "Date_Time" : date_time
        }

        

        return formatted_json





    # Get the raw JSON of all the next games (game list is unique)
    next_game_raw_json_list = get_next_games_raw_json(league_obj.json_data, league_obj.sport)
    formatted_games_list = []

    
    # Format the games into a dictionary to be displayed on the template
    for something in next_game_raw_json_list:
        formatted_games_list.append(
            format_game( something )
        )

    formatted_games_list = abbreviate_long_team_names(formatted_games_list)

    #return formatted_games_list
    league_obj.set_game_details( formatted_games_list )
















# Create your views here.
def index(request):


    print("##################### START INDEX #####################")
    context = {}


    print("********************** LOADING PREMIER LEAGUE INTO CONTEXT ***********")

    # Load context with leagues
    leagues = League.objects.all()

    stage_context = {}

    # Get the league objects and load them into context
    for league in leagues:

        # Update game_details dict

        # Get the raw league schedule
        raw_league_schedule = league.get_raw_league_schedule()

        # Format the raw json and find the next game
        get_next_games_display( league )

        # Get next games dict
        games = league.get_game_details()

        # Add dict to staging area
        stage_context[league.get_dict_key_name()] = games

      

        
        


        
    
    # This is hard coded but it needs to be changed once more leagues are added in
    #deuce = zip_longest( stage_context['Premier_League'], stage_context['NFL'], fillvalue=None )
    #context['deuce'] = deuce


    context['Premier_League'] = stage_context['Premier_League']
    context['NFL'] = stage_context['NFL']


    print("##################### END INDEX #######################")
    return render(request, "sportsscores/index.html", context)












