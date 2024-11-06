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
        self.roster={}

        # put a roster page on the main GUI
        self.build_roster_page()

    def build_roster_page(self):
        """Creates the basic grid for the roster page"""

        # create the new tab
        self.roster_page = tk.Frame(self.parent.notebook)
        self.roster_page.pack()
        self.parent.notebook.add(self.roster_page, text="Team Roster")

        # configure 2 columns
        self.roster_page.columnconfigure(0, weight=3)
        self.roster_page.columnconfigure(1, weight=1)

        # add heading labels
        self.r_head_1 = tk.Label(self.roster_page, text="Player Name", font=('Arial', 18))
        self.r_head_1.grid(row=0 , column = 0, sticky=tk.W + tk.E, pady=10)

        self.r_head_2 = tk.Label(self.roster_page, text="Player No.", font=('Arial', 18))
        self.r_head_2.grid(row=0 , column = 1, sticky=tk.W + tk.E)

        # create a roster table
        self.name_col = {}
        self.number_col = {}
        self.number_of_players = 0

    def new_player_entry(self, player_name, player_number):
        """Creates a class to for a new player"""

        #!! add data validation
        
        self.number_of_players += 1

        # create a new class
        self.roster[player_name] = Player(player_number)

        #!! consider re-drawing entire grid in alphabetical order

        # add the new player to the grid
        self.name_col[player_name] = tk.Label(self.roster_page, text=player_name, font=('Arial', 18))
        self.name_col[player_name].grid(row=self.number_of_players, column=0, sticky=tk.W + tk.E)

        self.number_col[player_name] = tk.Label(self.roster_page, text=player_number, font=('Arial', 18))
        self.number_col[player_name].grid(row=self.number_of_players, column=1, sticky=tk.W + tk.E)

