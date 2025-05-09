import random

team_selected = "lakers"
player_selected = "lebron"

offense = True
deffense = False 

teammate0 = ""
teammate1 = ""
teammate2 = ""
teammate3 = ""
teammate4 = ""
 
oppmate0 = ""
oppmate1 = ""
oppmate2 = ""
oppmate3 = ""
oppmate4 = ""

lakers_players = ["lebron", "kobe", "reeves", "luka", "hachi"]
knicks_players = ["brunson", "melo", "og", "hart", "kat"]

offenseive_plays = ["4:1", "3:2", "5out"]


def offensive_game_play():

    if team_selected == "knicks":


        teammate0 = player_selected
        knicks_players.remove(teammate0)
        teammate1 = random.choice(knicks_players)
        knicks_players.remove(teammate1)
        teammate2 = random.choice(knicks_players)
        knicks_players.remove(teammate2)
        teammate3 = random.choice(knicks_players)
        knicks_players.remove(teammate3)
        teammate4 = random.choice(knicks_players)

        oppmate0 = random.choice(lakers_players)
        lakers_players.remove(oppmate0)
        oppmate1 = random.choice(lakers_players)
        lakers_players.remove(oppmate1)
        oppmate2 = random.choice(lakers_players)
        lakers_players.remove(oppmate2)
        oppmate3 = random.choice(lakers_players)
        lakers_players.remove(oppmate3)
        oppmate4 = random.choice(lakers_players)

    else:
        
        teammate0 = player_selected
        lakers_players.remove(teammate0)
        teammate1 = random.choice(lakers_players)
        lakers_players.remove(teammate1)
        teammate2 = random.choice(lakers_players)
        lakers_players.remove(teammate2)
        teammate3 = random.choice(lakers_players)
        lakers_players.remove(teammate3)
        teammate4 = random.choice(lakers_players)

        oppmate0 = random.choice(knicks_players)
        knicks_players.remove(oppmate0)
        oppmate1 = random.choice(knicks_players)
        knicks_players.remove(oppmate1)
        oppmate2 = random.choice(knicks_players)
        knicks_players.remove(oppmate2)
        oppmate3 = random.choice(knicks_players)
        knicks_players.remove(oppmate3)
        oppmate4 = random.choice(knicks_players)

    offense_play = random.choice(offenseive_plays)

    matchup0 = [teammate0, oppmate0, '1']
    matchup1 = [teammate1, oppmate1, '2']
    matchup2 = [teammate2, oppmate2, '3']
    matchup3 = [teammate3, oppmate3, '4']
    matchup4 = [teammate4, oppmate4, '5']

    print("offensive_game_play")
    print(matchup0, matchup1, matchup2, matchup3, matchup4)
    print(offense_play)

def defensive_game_play():
    print("defensive_game_play")

if offense == True:
    offensive_game_play() 
else:
    defensive_game_play()

