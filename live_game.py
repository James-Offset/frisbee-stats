"""This file is to handle the tab for the live game and allow for new data input"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk

class LiveGame():
    def __init__(self, parent):
        # copy out key parent parts
        self.parent = parent

        # create a dictionary?!!
        self.roster={}

        # put a roster page on the main GUI
        self.build_live_page()

    def build_live_page(self):
        """Creates the strucutre for the live game page"""

        # create the new tab
        self.live_page = tk.Frame(self.parent.notebook)
        self.live_page.pack()
        self.parent.notebook.add(self.live_page, text="Live Game")

        # configure 5 columns
        self.live_page.columnconfigure(0, weight=1)
        self.live_page.columnconfigure(1, weight=2)
        self.live_page.columnconfigure(2, weight=1)
        self.live_page.columnconfigure(3, weight=1)
        self.live_page.columnconfigure(4, weight=2)

        # add the top row: Opp, Score, scorebox
        opp_name_text = "Opponent"
        self.opp_name = tk.Label(self.live_page, text=opp_name_text, font=('Arial', 18))
        self.opp_name.grid(row=0 , column = 0, sticky=tk.W + tk.E, columnspan=2)

        self.score_label = tk.Label(self.live_page, text="Score: ", font=('Arial', 18))
        self.score_label.grid(row=0 , column = 2, sticky=tk.E, columnspan=2)

        self.score_readout = tk.StringVar()
        self.live_score = tk.Label(self.live_page, textvariable=self.score_readout, font=('Arial', 18))
        self.live_score.grid(row=0 , column = 4, sticky=tk.W + tk.E)
        self.score_readout.set("0 - 0")

        # First row (after zero): Turnover Heading
        self.turnover_label = tk.Label(self.live_page, text="Turnovers:", font=('Arial', 18))
        self.turnover_label.grid(row=1 , column =0 , sticky=tk.W + tk.E, columnspan=3)

        self.posession_text = tk.StringVar()
        self.posession_label = tk.Label(self.live_page, textvariable=self.posession_text, font=('Arial', 18))
        self.posession_label.grid(row=1 , column =4 , sticky=tk.W + tk.E)
        self.posession_text.set("Opp possesion")

        # Second Row: minus, turns count, plus, space, end button
        self.minus_button = tk.Button(self.live_page, text="-", font=('Arial', 18), command=self.minus_function)
        self.minus_button.grid(row=2 , column =0 , sticky=tk.W + tk.E)

        self.turnover_count = 0
        self.turnover_count_value = tk.IntVar()
        self.count_label = tk.Label(self.live_page, textvariable=self.turnover_count_value, font=('Arial', 18))
        self.count_label.grid(row=2 , column =1 , sticky=tk.W + tk.E)
        self.turnover_count_value.set(self.turnover_count)

        self.plus_button = tk.Button(self.live_page, text="+", font=('Arial', 18), command=self.plus_function)
        self.plus_button.grid(row=2 , column =2 , sticky=tk.W + tk.E)

        self.end_button = tk.Button(self.live_page, text="End point", font=('Arial', 18), command=self.end_point)
        self.end_button.grid(row=2 , column =4 , sticky=tk.W + tk.E)

        # third row: player name, player number, on pitch, blanks
        self.r_head_1 = tk.Label(self.live_page, text="Player Name", font=('Arial', 18))
        self.r_head_1.grid(row=3 , column = 0, sticky=tk.W + tk.E, columnspan=2)

        self.r_head_2 = tk.Label(self.live_page, text="#", font=('Arial', 18))
        self.r_head_2.grid(row=3 , column = 2, sticky=tk.W + tk.E)

        self.on_label = tk.Label(self.live_page, text="On", font=('Arial', 18))
        self.on_label.grid(row=3 , column = 3, sticky=tk.W + tk.E)
        
        # create a roster table
        self.name_col = {}
        self.number_col = {}
        self.check_col = {}
        self.check_values = {}
        row_count = 3

        for player in self.parent.team.roster:
            row_count+=1
            self.name_col[player] = tk.Label(self.live_page, text=player, font=('Arial', 16))
            self.name_col[player].grid(row=row_count , column =0 , sticky=tk.W + tk.E, columnspan=2)

            number_text = self.parent.team.roster[player]["Number"]
            self.number_col[player] = tk.Label(self.live_page, text=number_text, font=('Arial', 16))
            self.number_col[player].grid(row=row_count , column =2 , sticky=tk.W + tk.E)

            # add checkboxes here
            self.check_values[player] = tk.IntVar()
            self.check_col[player] = tk.Checkbutton(self.live_page, variable=self.check_values[player], command=self.update_player_total)
            self.check_col[player].grid(row=row_count , column=3 , sticky=tk.W + tk.E)

        # Add a label showing the total number of players
        self.player_count = tk.IntVar()
        self.player_count_label = tk.Label(self.live_page, textvariable=self.player_count, font=('Arial', 18))
        self.player_count_label.grid(row=5 , column = 4, sticky=tk.W + tk.E)
        self.player_count.set(0)

    def plus_function(self):
        """Increments the turnover count when the plus button is pressed"""
        self.turnover_count += 1
        self.turnover_count_value.set(self.turnover_count)

    def minus_function(self):
        """decreases the turnover count when the minus button is pressed"""
        if self.turnover_count > 0:
            self.turnover_count -= 1
            self.turnover_count_value.set(self.turnover_count)   

    def update_player_total(self):
        """When a checkbox is checked or unchecked, we update the count of checked boxes"""
        players_checked = 0
        for player_box in self.check_values:
            checkbox_value = self.check_values[player_box].get()
            players_checked += checkbox_value
        
        self.player_count.set(players_checked)
        

    def end_point(self):
        """At the end of the point, log all the data and clear the roster for the next point"""

        # clear the checkboxes
        for player_box in self.check_values:
            self.check_values[player_box].set(0)
        # reset the count
        self.update_player_total()


