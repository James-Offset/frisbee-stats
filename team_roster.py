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
from awards_tab import AwardsTab



class Team():
    """A class to manage all the functions relating to the team roster"""

    def __init__(self, parent):
        """Initial set up"""

        # copy out key parent parts
        self.parent = parent

        # create a dictionary to hold the player classes
        self.display_row_number = 0
        self.roster={}

        # create a dictionary to hold the display frames for the tabs
        self.player_stats_pages = {} # holds the other two frames
        self.team_frame = {} # holds the team info table
        self.player_frame = {} # holds the player info table

        # Get tournament name !!"MIR 2017"
        self.tournament_name = parent.tournament_name
        self.team_name = parent.team_name

        # create a player class that actually represents the whole team
        self.team_record = Player(self, self.team_name, 0, -1)

        # put a roster page on the main GUI for the full tournaments stats
        self.build_team_stats_page(self.tournament_name)

        # create the awards tab
        self.awards_class = AwardsTab(self)


    def build_team_stats_page(self, tab_name):
        """Prepares the team records and builds the two sections of the gui tabs"""

        # doesn't fit with the rest of the function, but we need the team stats dictionary to make a new subfolder
        self.team_record.prepare_to_receive_data(tab_name)

        # create the new tab
        self.player_stats_pages[tab_name] = tk.Frame(self.parent.notebook)
        self.player_stats_pages[tab_name].pack()
        tab_label = tab_name[:7] + " Stats"
        self.parent.notebook.add(self.player_stats_pages[tab_name], text=tab_label)

        # set up the two sections of the tab
        self._create_team_section(tab_name)
        self._create_player_section(tab_name)

    def _create_team_section(self, tab_name):
        """Creates the grid for the team information"""
        pass

    def _create_player_section(self, tab_name):    
        """Creates the basic grid for the roster page, not filled in"""

        # create frame to hold section
        self.player_frame[tab_name] = tk.Frame(self.player_stats_pages[tab_name])
        self.player_frame[tab_name].pack(fill=tk.X, expand=True)

        # create a dictionary to hold the details of the GUI columns
        self.gui_headings = [
            "Player", 
            "#", 
            "PP", 
            "OP",
            "OC",
            "DP",
            "DC",
            "MO",
            "MD",
            "OS",
            "DS", 
            "TS",
            ]
        # <<< These correspond to the output stats in the player class
        
        self.gui_elements = {}
        
        # decide where to put separators
        self.separator_columns = [2, 8]

        # create a dictionary to keep the separators in
        self.separator_elements = {}

        column_number=0
        for heading in self.gui_headings:
            
            if column_number in self.separator_columns:
                # create a column for the separator
                self.player_frame[tab_name].columnconfigure(column_number, weight=1)
                self.separator_elements[str(column_number)] = ttk.Separator(self.player_frame[tab_name], orient="vertical")
                self.separator_elements[str(column_number)].grid(row=0 , rowspan=1, column = column_number, sticky='ns', padx=2)

                column_number += 1
            
            # create a column for the heading
            self.player_frame[tab_name].columnconfigure(column_number, weight=1)
        
            # add heading labels
            self.gui_elements[heading] = tk.Label(self.player_frame[tab_name], text=heading, font=('Arial', 18))
            self.gui_elements[heading].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=10)

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
            
            # redraw separators
            for separator in self.separator_elements:
                self.separator_elements[separator].grid(row=0 , rowspan=self.display_row_number+1, column = int(separator), sticky='ns', padx=2)


    def add_players_to_stats_page(self, tab_name):
        """For a new stats page, we need to add a row for each player already on the roster"""

        # add the player information to the new data tab
        for player in self.roster:
            self.roster[player].prepare_to_receive_data(tab_name)
        
        # redraw separators
        for separator in self.separator_elements:
            self.separator_elements[separator].grid(row=0 , rowspan=self.display_row_number+1, column = int(separator), sticky='ns', padx=2)


    def end_of_game_calcs(self):
        """Calls each player class to run their comparison calcs"""

        for player in self.roster:
            self.roster[player].calculate_comparison_stats()
        
        # update awards
        self.awards_class.calcualte_awards()
