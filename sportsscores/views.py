from django.shortcuts import render

from django.http import HttpResponse

import requests
import json

from django.utils import timezone
from datetime import datetime
import pytz


timezone = pytz.timezone('America/New_York')


def format_time_soccer(unformattedTime):
    print("FORMATTED TIME\n\n\n\n\n\n\n")

    print("Current Time: ", datetime.now() )

    print("Unformatted Time: ", unformattedTime)

    time_chunks = {}

    time_chunks['Year'] = unformattedTime[0:4]
    time_chunks['Month'] = unformattedTime[5:7]
    time_chunks['Day'] = unformattedTime[8:10]
    time_chunks['Hour'] = unformattedTime[11:13]
    time_chunks['Minute'] = unformattedTime[14:16]


    return time_chunks

def get_game_status(timestamp):
    print("Getting status... ")

    current_time = datetime.now()

    print( current_time )
    print( current_time.day )

    print( type( int(timestamp['Year']) ) )
    print( type(current_time.year) )

    print( timestamp['Year'] )
    print( current_time.year )

    print( current_time.hour)
    print( int(timestamp['Hour'])-4)

    if( current_time.year == int( timestamp['Year'] ) and current_time.month == int( timestamp['Month'] ) ):
        # If it is the day before
        if( current_time.day < int( timestamp['Day'] )  ):
            return "Tomorrow"
        # If the game is today
        elif( current_time.day == int( timestamp['Day'] ) ):
            
            if( current_time.hour == int(timestamp['Hour'])-4  and current_time.minute >= int(timestamp['Minute']) ):
                return "Now"
            elif( current_time.hour == (int(timestamp['Hour'])-4 + 1) ):
                return "Now"
            elif( current_time.hour == (int(timestamp['Hour'])-4 + 2)  and current_time.minute < int(timestamp['Minute']) ):
                return "Now"
            else:
                return "TodayAndOver"

    else:
        return "Meh"


def download_schedule():
    # The code below will fetch the data from the API
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"league":39,"season":"2023"}

    headers = {
        "X-RapidAPI-Key": "1e3ccc2439msh0e41508573472b1p12951ejsnbb3a79fa2ed1",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    

# Create your views here.
def index(request):

    

    # Get the schedule for offline mode
    f = open( 'NFL_Schedule.json')
    data = json.load( f )
    print("Loading NFL...")



    context_array = []

    #formattedTime = formatTime( data[0]['fixture']['date'] )

    

    #print( formattedTime )

    #get_game_status(formattedTime)

    count = 0

    """ # Load Chelsea games into the dict
    for d in data:
        if( d['teams']['home']['id'] == 45 or d['teams']['away']['id'] == 45 ):

            

            

            formattedTime = format_time_soccer( d['fixture']['date'] )
            status = get_game_status( formattedTime )

            print("GAME STATUS: ", status)

            tmp_dict = {
    
                'home_team': d['teams']['home']['name'],
                'away_team': d['teams']['away']['name'],
                'home_score': d['goals']['home'],
                'away_score': d['goals']['away'],
                'date': d['fixture']['date'],
                'status': status

            }
            context_array.append(tmp_dict)
            count += 1

            if( count >= 5 ):
                break
    """


    # Load Chelsea games into the dict
    
        
    team_IDs = []

    # Get list of all team id's
    for d in data:
        if( d['teams']['home']['id'] not in team_IDs and d['teams']['home']['id'] != 0):
            team_IDs.append( int( d['teams']['home']['id'] ) )

            if( len( team_IDs ) >= 32 ):
                break
    
    NFL_next_games = []

    Short_Finish_Codes = ['FT', 'AOT']
    Long_Finish_Codes = ['Final/OT', 'Finished', 'After Over Time']


    # Get every teams next game
    for ID in team_IDs:
        for d in data:
            
            if( d['game']['status']['long'] not in Long_Finish_Codes ):
                if( d['teams']['home']['id'] == ID ):
                    if( d not in NFL_next_games ):
                        NFL_next_games.append( d )
                    break
                elif( d['teams']['away']['id'] == ID ):
                    if( d not in NFL_next_games ):
                        NFL_next_games.append( d )
                    break


    print( "NFL_next_games: ", len( NFL_next_games ) )
    print( "LENGHT: ", len(team_IDs))
    print( team_IDs )

    # Load next NFL games into the dict
    for d in NFL_next_games:

        #formattedTime = format_time_soccer( d['fixture']['date'] )
        #status = get_game_status( formattedTime )

        tmp_dict = {

            'home_team': d['teams']['home']['name'],
            'away_team': d['teams']['away']['name'],
            'home_score': d['scores']['home']['total'],
            'away_score': d['scores']['away']['total'],
            'date': d['game']['date']['date'],
            'time': d['game']['date']['time'],
            'week': d['game']['week']

        }
        context_array.append(tmp_dict)
        count += 1

        #if( count >= 5 ):
        #    break
    


    #print(context_array)

    sorted_context_array = sorted( context_array, key=lambda x: x['date'])
           

    context = {
        "Premier_League_Chelsea_Games" : sorted_context_array
    }


    return render(request, "sportsscores/index.html", context)












