import requests
import time
from datetime import datetime
import pytz

# Define Variables
base_url = 'http://data.nba.net'

# Get Today's date US TZ


def get_fmt_date():
    date_today = datetime.now()
    us_date = date_today.astimezone(pytz.timezone('America/Los_Angeles'))
    fmt_date = us_date.strftime('%Y%m%d')
    return fmt_date


# Test date
test_date = '20210617'

# Get Play by Play


def get_play_data(gameId):
    request = requests.get(
        f'{base_url}/data/10s/json/cms/noseason/game/{test_date}/{gameId}/pbp_all.json')
    return request.json()


def show_plays(gameId):
    active_game = 1
    while active_game == 1:
        play_data = get_play_data(gameId)
        plays = play_data['sports_content']['game']['play']
        current_play = '{}: {}'.format(
            plays[200]['clock'], plays[200]['description'])
        print(current_play, end="\r")
        time.sleep(3)

# Show games


def show_games_today(games_today):
    print('Todays games:')
    # Loop over games
    for game in games_today:
        print('{} @ {}'.format(game['hTeam']
              ['triCode'], game['vTeam']['triCode']))

    selected_game = input('What game? ')

    for game in games_today:
        if selected_game == game['hTeam']['triCode']:
            show_plays(game['gameId'])
            break

# Request today's scoreboard


def get_scoreboard():
    scoreboard_req = requests.get(
        '{}/10s/prod/v1/{}/scoreboard.json'.format(base_url, test_date))
    scoreboard = scoreboard_req.json()
    games_today = scoreboard['games']
    show_games_today(games_today)


get_scoreboard()
