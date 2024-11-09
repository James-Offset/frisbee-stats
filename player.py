"""Any data that needs to be stored or processed at the player level is stored here

Not sure if this is necessary at this point, but we can set up a class if needed. 
"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk

class Player():
    """A class for all the data and functions that relate to a single player"""

    def __init__(self, parent, number):
        """Sets up the data fields for the player"""

        self.parent = parent
        self.number = number

        # set up all the bits for the GUI
        self._create_gui_elements()

        # create a dictionary to store performance data for the whole tournament
        self.aggregate_dictionary = {
            "number of points played" : 0,
            "Points Scored" : 0,
            "Points Won" : 0,
            "Turns Won" : 0,
            "Turns Lost" : 0
        }

        self.stats_count = {
            "number of points played" : 0,
            "possessions played" : 0,
            "offence possessions" : 0,
            "defence possessions" : 0,
            "turnovers conceded" : 0,
            "turnovers won" : 0,
        }

        self.display_dictionary={
            "number of points played" : 0,
            "offence conversion rate" : 0,
            "defence conversion rate" : 0,
        }

        # create a dictionary to store data for each game played
        self.game_stats_count = {}

    def _create_gui_elements(self):
        """Sorts out all the labels that will display a data point for a certain player"""
        
        # create a dictionary to hold all of the elements that will go into the roster display tab
        self.gui_elements = {
            "name" : 0,
            "number" : 0,
            "separator placeholder" : 0,
            "number of points played" : 0,
            "offence conversion rate" : 0,
            "defence conversion rate" : 0,
        }

        for element in self.gui_elements:
            self.gui_elements[element] = tk.Label(self.parent.roster_page, text="-", font=('Arial', 16))

        


    def create_game_dictionary(self, name_of_game):
        """When we start a new game, create a new dictionary to keep the stats for that game in"""

        self.game_stats_count[name_of_game] = {
            "number of points played" : 0,
            "possessions played" : 0,
            "offence possessions" : 0,
            "defence possessions" : 0,
            "turnovers conceded" : 0,
            "turnovers won" : 0,
        }

    def calculate_new_scores(self):
        """takes the new count data from the most recent point and works out the players performance"""

        # run calcualtions for each stat
        try:
            o_conv = round(100 * (1 - (self.stats_count["turnovers conceded"] / self.stats_count["offence possessions"])))
        except ZeroDivisionError:
            o_conv = "-"
        
        try:
            d_conv = round(100 * (self.stats_count["turnovers won"] / self.stats_count["defence possessions"]))
        except ZeroDivisionError:
            d_conv = "-"

        # update display dictionary
        self.display_dictionary["number of points played"] = self.stats_count["number of points played"]
        self.display_dictionary["offence conversion rate"] = o_conv
        self.display_dictionary["defence conversion rate"] = d_conv

        # update the text on the label for each stat on the roster tab
        for element in self.display_dictionary:
            self.gui_elements[element].config(text=self.display_dictionary[element])