"""
Extracting information about players.
"""
__author__ = "Zener085"
__version__ = "1.0.0"
__license__ = "MIT"

from pyrebase import initialize_app
from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

DATA: dict = {
    "apiKey": getenv("apiKey"),
    "authDomain": getenv("authDomain"),
    "databaseURL": getenv("databaseURL"),
    "projectId": getenv("projectId"),
    "storageBucket": getenv("storageBucket"),
    "messagingSenderId": getenv("messagingSenderId"),
    "appId": getenv("appId"),
    "measurementId": getenv("measurementId")
}


class Player:
    def __init__(self, *args: str):
        self.alias: str = str(args[0])
        self.id: int = int(args[1])
        self.name: str = str(args[2])
        self.points: int = int(args[3])
        self.loses: int = int(args[4])
        self.attendance: int = self.loses + self.points

    def __str__(self) -> str:
        return "Name - " + self.name + \
               "\nId - " + str(self.id) + \
               "\nPoints - " + str(self.points) + \
               "\nLoses - " + str(self.loses)

    def __repr__(self) -> str:
        return "Name - " + self.name + \
               "; Id - " + str(self.id) + \
               "; Points - " + str(self.points) + \
               "; Loses - " + str(self.loses)


def import_string() -> str:
    """import STRING from data"""
    return initialize_app(DATA).database().child("save").get().val()


def parse_data(string: str = None) -> dict:
    """parsing STRING to normal list"""
    if string is None:
        return {}

    players: dict[str, Player] = {}

    for substring in string.split(";")[:-1]:
        player = Player(*substring.split(":"))
        players[player.alias] = player

    return players


def generate_top(top_: list) -> list:
    """generate list with all players, had the same points in top 3 or higher"""
    top_players: list = [[top_[0]]]
    index: int = 0

    for i in range(1, len(top_)):
        if top_[i].points == top_[i - 1].points:
            top_players[index].append(top_[i])
        else:
            players = 0
            for top_player in top_players:
                players += len(top_player)
            if players >= 3:
                break
            top_players.append([top_[i]])
            index += 1

    return top_players


def top_rating() -> str:
    """return list of top 3 or higher players (if they have the same points)"""
    answer = "Top mafia players:\n"
    top: list = sorted(parse_data(import_string()).values(), key=lambda p: p.points, reverse=True)

    if top[0].points == '0':
        return "Everybody has the same number of points - 0."

    top = generate_top(top)

    if len(top) == 1:  # All top 3 players have the same number of points
        answer += f"1-{len(top[0])}: "
        for player in top[0]:
            answer += f"{player.name}, "
        answer += f"all have {top[0][0].points} points."
    elif len(top) == 2:  # There are 2 groups of players, having 1-2 and 3-... places in rating
        if len(top[0]) != 1:
            answer += f"1-{len(top[0])}: "
            for player in top[0]:
                answer += f"{player.name}, "
            answer += f"all have {top[0][0].points} points;\n"
        else:
            answer += f"1: {top[0][0].name}, {top[0][0].points} points;\n"

        answer += f"{len(top[0]) + 1}-{len(top[1]) + len(top[0])}: "
        for player in top[1]:
            answer += f"{player.name}, "
        answer += f"all have {top[1][0].points} points."
    else:  # 1 and 2 places have different rating and 3-... have another
        answer += f"1: {top[0][0].name}, {top[0][0].points} points;\n"
        answer += f"2: {top[1][0].name}, {top[1][0].points} points;\n"

        if len(top[2]) != 1:
            answer += f"3-{len(top[2]) + 2}: "
            for player in top[2]:
                answer += f"{player.name}, "
            answer += f"all have {top[2][0].points} points."
        else:
            answer += f"3: {top[2][0].name}, {top[2][0].points} points."

    return answer


if __name__ == "__main__":
    pass
