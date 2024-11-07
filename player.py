"""Any data that needs to be stored or processed at the player level is stored here

Not sure if this is necessary at this point, but we can set up a class if needed. 
"""


class Player():
    """A class for all the data and functions that relate to a single player"""

    def __init__(self, number):
        """Sets up the data fields for the player"""

        self.number = number


        # create a dictionary to store performance data for the whole tournament
        self.aggregate_dictionary = {
            "Points Played" : 0,
            "Points Scored" : 0,
            "Points Won" : 0,
            "Turns Won" : 0,
            "Turns Lost" : 0
        }

        # create a dictionary to store data for each game played
        self.games = {}

    def create_game_dictionary(self, name_of_game):
        """When we start a new game, create a new dictionary to keep the stats for that game in"""

        self.games[name_of_game] = {
            "Number of Points Played" : 0
        }