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
        self.number_of_players = 0
        self.roster={}

        # put a roster page on the main GUI
        self.build_roster_page()

    def build_roster_page(self):
        """Creates the basic grid for the roster page"""

        # create the new tab
        self.roster_page = tk.Frame(self.parent.notebook)
        self.roster_page.pack()
        self.parent.notebook.add(self.roster_page, text="Team Roster")

        # configure 7 columns
        self.roster_page.columnconfigure(0, weight=3)
        self.roster_page.columnconfigure(1, weight=1)
        self.roster_page.columnconfigure(2, weight=1)
        self.roster_page.columnconfigure(3, weight=1)
        self.roster_page.columnconfigure(4, weight=1)
        self.roster_page.columnconfigure(5, weight=1)
        self.roster_page.columnconfigure(6, weight=1)

        # add heading labels
        self.name_h = tk.Label(self.roster_page, text="Player Name", font=('Arial', 18))
        self.name_h.grid(row=0 , column = 0, sticky=tk.W + tk.E, pady=10)

        self.number_h = tk.Label(self.roster_page, text="Player No.", font=('Arial', 18))
        self.number_h.grid(row=0 , column = 1, sticky=tk.W + tk.E)

        self.s1 = ttk.Separator(self.roster_page, orient="vertical")
        self.s1.grid(row=0 , column = 2, sticky='ns', padx=3)

        self.pp_h = tk.Label(self.roster_page, text="PP", font=('Arial', 18))
        self.pp_h.grid(row=0 , column = 3, sticky=tk.W + tk.E, pady=10)

        self.pc_h = tk.Label(self.roster_page, text="OC", font=('Arial', 18))
        self.pc_h.grid(row=0 , column = 4, sticky=tk.W + tk.E, pady=10)

        self.tc_h = tk.Label(self.roster_page, text="DC", font=('Arial', 18))
        self.tc_h.grid(row=0 , column = 5, sticky=tk.W + tk.E, pady=10)
        

    def new_player_entry(self, player_name, player_number):
        """Creates a class to for a new player"""

        #!! add data validation
        
        self.number_of_players += 1

        # create a new class
        self.roster[player_name] = Player(self, player_number)

        #!! consider re-drawing entire grid in alphabetical order

        # add the new player to the grid
        column_number = 0
        for element in self.roster[player_name].gui_elements:
            self.roster[player_name].gui_elements[element].grid(row=self.number_of_players, column=column_number, sticky='ew')
            column_number += 1

        self.roster[player_name].gui_elements["name"].config(text=player_name)
        self.roster[player_name].gui_elements["number"].config(text=player_number)
        self.roster[player_name].gui_elements["separator placeholder"].config(text="") #!! just remove this element, or stop it being made

        # redraw separator
        self.s1.grid(row=0, rowspan=self.number_of_players, column=2, sticky="ns", padx=3)

