"""Any data that needs to be stored or processed at the player level is stored here

Not sure if this is necessary at this point, but we can set up a class if needed. 
"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk
import copy

class Player():
    """A class for all the data and functions that relate to a single player"""

    def __init__(self, parent, name, number, row_number):
        """Sets up the data fields for the player"""

        self.parent = parent
        self.name = name
        self.number = number
        self.display_row_number = row_number

        # !!
        self.tournament_name = self.parent.parent.tournament_name

        # set up the data structures for the class
        self._create_data_structures()


    def _create_data_structures(self):
        """ Creates all the dictionaries that player data and gui information will be stored"""

        # create a dictionary to store the input data provided by the game class. Sub-dictionary for each game
        self.page_stats_count = {}

        # create a mirror dictionary to capture team performance when the player is not on the pitch
        self.negative_stats_count = {}

        # create templates for the game data sub dictionary
        self.template_stats_count_dict = {
            "number of points played" : 0,
            "number of possessions played" : 0,
            "no. offence possessions" : 0,
            "no. defence possessions" : 0,
            "turnovers conceded" : 0,
            "turnovers won" : 0,
        }

        # create a dictionary that will store all the gui labels that will display data
        self.gui_labels_dicts = {}

        # dictionary for gui info that does not change
        self.fixed_gui_display_data = {
            "name" : self.name,
            "number" : self.number,
        }

        # dictionary for output display data. This will hold a sub-dictionary per game
        self.output_display_data = {}
        self.negative_stats_output = {}
        self.comparison_stats_output = {}

        
        # create a template for this sub dictionary
        self.template_variable_display_dict ={
            "number of points played" : 0,
            "no. offence possessions" : 0,
            "offence conversion rate" : 0,
            "no. defence possessions" : 0,
            "defence conversion rate" : 0,
        }


    def prepare_to_receive_data(self, data_tab):
        """when a new stats roster tab is created this function creates sub-dictionaries to recieve data and adds the player details to the table"""

        #!! consider re-drawing entire grid in alphabetical order

        # find out what the reference for the new data tab is (tournament name or game ref)
        self.live_game_ref = data_tab

        # create a new sub-dictionary to store input data for that game from the game class
        self.page_stats_count[self.live_game_ref] = copy.deepcopy(self.template_stats_count_dict)
        self.negative_stats_count[self.live_game_ref] = copy.deepcopy(self.template_stats_count_dict)

        # copy out a sub dictionaries for the variable display data that will be shown on this stats tab, as well as for the negative and comparisons
        self.output_display_data[self.live_game_ref] = copy.deepcopy(self.template_variable_display_dict)
        self.negative_stats_output[self.live_game_ref] = copy.deepcopy(self.template_variable_display_dict)
        self.comparison_stats_output[self.live_game_ref] = copy.deepcopy(self.template_variable_display_dict)

        if self.display_row_number < 0:
            # must be the full team stats class
            pass
        else:
            # add the player to the relevant stats tab
            self.add_player_to_gui_tab()
        
    def add_player_to_gui_tab(self):
        """Sets up the GUI elements that track for that player on the active stats tab"""
        
        # create a sub-dictionary to hold all of the gui elements that will go into the stats tab
        self.gui_labels_dicts[self.live_game_ref] = {}

        # for each data point that will need to be shown, create a label to hold it and add it to the grid. (both fixed and variable data)
        column_number = 0
        for element in self.fixed_gui_display_data:
            self.gui_labels_dicts[self.live_game_ref][element] = tk.Label(self.parent.player_stats_pages[self.live_game_ref], text=self.fixed_gui_display_data[element], font=('Arial', 16))
            self.gui_labels_dicts[self.live_game_ref][element].grid(row=self.display_row_number, column=column_number, sticky='ew')
            column_number += 1

        column_number+=1 # for a separator
        
        for element in self.output_display_data[self.live_game_ref]:
            self.gui_labels_dicts[self.live_game_ref][element] = tk.Label(self.parent.player_stats_pages[self.live_game_ref], text="-", font=('Arial', 16))
            self.gui_labels_dicts[self.live_game_ref][element].grid(row=self.display_row_number, column=column_number, sticky='ew')
            column_number += 1
        

    def update_point_data(self, stats_input, name_check):
        """If a player was on the pitch for a point, this function will be called at the end to update the records for the player"""

        # check whether the player was on the pitch (or it's the team class)
        if name_check == self.name:
        
            # store each statistic in both the game dictionaries and the tournament dictionaries
            for data_set in (self.live_game_ref, self.tournament_name):
                for game_event in stats_input:
                    # update each input stat in turn
                    self.page_stats_count[data_set][game_event] += stats_input[game_event]

                #!! will want to calc display stats for the full team at some point
                if self.display_row_number < 0:
                    pass
                else:
                    # calculate new output stats for that data set
                    self.calculate_display_stats(data_set)

        else: # player was not on the pitch, so add the info to the negative stats dictionary
            for data_set in (self.live_game_ref, self.tournament_name):
                for game_event in stats_input:
                    # update each input stat in turn
                    self.negative_stats_count[data_set][game_event] += stats_input[game_event]

    def calculate_display_stats(self, sub_dict):
        """takes the new count data from the most recent point and works out the players performance"""

        # run calcualtions for each stat
        try:
            o_conv = round(100 * (1 - (self.page_stats_count[sub_dict]["turnovers conceded"] / self.page_stats_count[sub_dict]["no. offence possessions"])))
        except ZeroDivisionError:
            o_conv = "-"
        
        try:
            d_conv = round(100 * (self.page_stats_count[sub_dict]["turnovers won"] / self.page_stats_count[sub_dict]["no. defence possessions"]))
        except ZeroDivisionError:
            d_conv = "-"

        # update display dictionary
        self.output_display_data[sub_dict]["number of points played"] = self.page_stats_count[sub_dict]["number of points played"]
        self.output_display_data[sub_dict]["no. offence possessions"] = self.page_stats_count[sub_dict]["no. offence possessions"]
        self.output_display_data[sub_dict]["offence conversion rate"] = o_conv 
        self.output_display_data[sub_dict]["no. defence possessions"] = self.page_stats_count[sub_dict]["no. defence possessions"]
        self.output_display_data[sub_dict]["defence conversion rate"] = d_conv

        # update the text on the label for each stat on the roster tab
        for element in self.output_display_data[sub_dict]:
            self.gui_labels_dicts[sub_dict][element].config(text=self.output_display_data[sub_dict][element])

    def calculate_comparison_stats(self, data_set):
        """Compares the on- and off- pitch performance for the player"""

        if self.negative_stats_count[data_set]["no. offence possessions"] > 3:
            # work out the negative offence and defence conversion rates
            pass

