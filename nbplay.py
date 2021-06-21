import requests
import time
from datetime import datetime
import pytz

# Styles class


class style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


# Define Variables
base_url = 'http://data.nba.net'

# Get Today's date US TZ


def get_fmt_date():
    date_today = datetime.now()
    us_date = date_today.astimezone(pytz.timezone('America/Los_Angeles'))
    fmt_date = us_date.strftime('%Y%m%d')
    return fmt_date


# Test date
test_date = '20210620'

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
        current_play = '{}{}:{} {}'.format(
            style.RED, plays[200]['clock'], style.RESET, plays[200]['description'])
        print(current_play, end="\r")
        time.sleep(3)

# Show games


def show_games_today(games_today):
    print(style.MAGENTA + 'Todays games:' + style.RESET)
    # Loop over games
    for game in games_today:
        print('{} @ {}'.format(game['hTeam']
              ['triCode'], game['vTeam']['triCode']))

    selected_game = input(style.GREEN + 'What game? ' + style.RESET)

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
