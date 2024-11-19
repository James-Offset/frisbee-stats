"""This file holds the class information for building and storing the team roster

I will need a team entry function, and maybe a team edit function
We want to capture the team name, but this might go elsewhere
Then a dictionary containing the player names and their numbers. 
We might also need to leave a load of space for all their stats as well

"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk


"""My Code"""
from player import Player



class Team():
    """A class to manage all the functions relating to the team roster"""

    def __init__(self, parent):
        """Initial set up"""

        # copy out key parent parts
        self.parent = parent

        # create a dictionary to hold the player classes
        self.display_row_number = 0
        self.roster={}

        # create a dictionary to hold the display tabs for player stats
        self.player_stats_pages = {}

        # Get tournament name !!"MIR 2017"
        self.tournament_name = parent.tournament_name
        self.team_name = parent.team_name

        # create a player class that actually represents the whole team
        self.team_record = Player(self, self.team_name, 0, -1)

        # put a roster page on the main GUI for the full tournaments stats
        self.build_player_stats_page(self.tournament_name)

    def build_player_stats_page(self, tab_name):
        """Creates the basic grid for the roster page, not filled in"""

        # doesn't fit with the rest of the function, but we need the team stats dictionary to make a new subfolder
        self.team_record.prepare_to_receive_data(tab_name)

        # create the new tab
        self.player_stats_pages[tab_name] = tk.Frame(self.parent.notebook)
        self.player_stats_pages[tab_name].pack()
        tab_label = tab_name[:6] + " Stats"
        self.parent.notebook.add(self.player_stats_pages[tab_name], text=tab_label)

        # create a dictionary to hold the details of the GUI columns
        self.gui_columns = {
            "heading text" : [
                "Player Name", 
                "#", 
                "separator1", 
                "PP", 
                "OP",
                "OC",
                "DP",
                "DC",
                ],
            "column weighting" : [3, 1, 1, 1, 1, 1, 1, 1,],
            "label elements" : {}
        }

        # neaten this later !!
        self.separator_column_number = 2

        column_number=0
        for column in self.gui_columns["heading text"]:
            # create a column
            self.player_stats_pages[tab_name].columnconfigure(column_number, weight=self.gui_columns["column weighting"][column_number])
        
            # add heading labels
            if "separator" in column:
                self.gui_columns["label elements"][column] = ttk.Separator(self.player_stats_pages[tab_name], orient="vertical")
                self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky='ns', padx=2)
            else:
                self.gui_columns["label elements"][column] = tk.Label(self.player_stats_pages[tab_name], text=self.gui_columns["heading text"][column_number], font=('Arial', 18))
                self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=10)

            column_number += 1

    def new_player_entry(self, player_name, player_number):
        """Creates a class to for a new player"""

        #!! add data validation
        
        self.display_row_number += 1

        # create a new class
        self.roster[player_name] = Player(self, player_name, player_number, self.display_row_number)

        # add the player to the existing stats pages on the GUI
        for tab_name in self.player_stats_pages:
            self.roster[player_name].prepare_to_receive_data(tab_name)
            
            # redraw separator
            self.gui_columns["label elements"]["separator1"].grid(row=0, rowspan=self.display_row_number+1, column=self.separator_column_number, sticky="ns", padx=3)


    def add_players_to_stats_page(self, tab_name):
        """For a new stats page, we need to add a row for each player already on the roster"""

        # add the player information to the new data tab
        for player in self.roster:
            self.roster[player].prepare_to_receive_data(tab_name)
        
        # redraw separator
        self.gui_columns["label elements"]["separator1"].grid(row=0, rowspan=self.display_row_number+1, column=self.separator_column_number, sticky="ns", padx=3)


        
