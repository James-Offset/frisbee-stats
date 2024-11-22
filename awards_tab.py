"""This file holds the class that defines the functions for the team awards tab and functions"""

import tkinter as tk
from tkinter import ttk

class AwardsTab():
    def __init__(self, parent):
        """TBC"""

        self.parent = parent

        self.tour_name = self.parent.tournament_name

        self._establish_awards()

        self._create_notebook_tab()

    def _establish_awards(self):
        """Creates the data structure for the awards"""

        self.awards_definitions = {
            "MVP" :             ["Most Valuable Player", self.mvp_cal],
            "O-Line MVP" :      ["Most likely to win the point on offence", self.o_mvp_cal],
            "D-Line MVP" :      ["Most likely to win the point on defence", self.d_mvp_cal],
            "The Juggernaut" :  ["Highest offence score rate", self.jug_cal],
            "The Wall" :        ["Highest defence turnover rate", self.wall_cal],
            "Big Batteries" :   ["Most possessions played", self.bat_cal],
            "Captain Dependable" :  ["Most consistent contribution", 0],
            "Glass Cannon" :    ["Greatest offence to defence scores", self.glass_cal],
            "Pacifist" :        ["Greatest defence to offence scores", self.pac_cal],
            "The Infiltrator" : ["Highest score rate against tough opposition", 0],
            "The Fortress" :    ["Highest turnover win rate against tough opposition", 0],
            "Flat-Track Bully": ["Scores skew towards winning games", 0],
            "Die-Hard" :        ["Scores skew towards losing games", 0],
            "Clutch Player" :   ["Performs at their best in close games", 0],
            "Upwind Specialist" :   ["Performs at their best upwind", 0],
            "Downwind Specialist" : ["Performs at their best downwind", 0],
        }

        # establish a dictionary of winners
        self.winners = {}
        for award in self.awards_definitions:
            self.winners[award] = {
                "Highest Recorded Score" : 0,
                "Holder of Highest Score" : "-",
            }

    def _create_notebook_tab(self):
        """Creates a new tab in the notebook and adds gui elements"""

        # create the new tab
        self.gui_page = tk.Frame(self.parent.parent.notebook)
        self.gui_page.pack()
        tab_label = "Awards"
        self.parent.parent.notebook.add(self.gui_page, text=tab_label)

        # create a dictionary to hold the details of the GUI columns
        self.gui_columns = {
            "heading text" : ["Award", "Winner", "Description"],
            "column weighting" : [2, 2, 2,],
            "label elements" : {}
        }

        # create dictionaries to hold the gui labels
        self.gui_awards_titles = {}
        self.gui_awards_winners = {}
        self.gui_awards_descriptions = {}

        # create columns in turn according to above configuration
        column_number=0
        for column in self.gui_columns["heading text"]:
            # create a column
            self.gui_page.columnconfigure(column_number, weight=self.gui_columns["column weighting"][column_number])
        
            # add heading labels
            if "separator" in column:
                self.gui_columns["label elements"][column] = ttk.Separator(self.gui_page, orient="vertical")
                self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky='ns', padx=2)
            else:
                self.gui_columns["label elements"][column] = tk.Label(self.gui_page, text=self.gui_columns["heading text"][column_number], font=('Arial', 18))
                self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=10)

            column_number += 1
        
        # horizontal Separator
        s0 = ttk.Separator(self.gui_page, orient='horizontal')
        s0.grid(row=1, column = 0, sticky=tk.W + tk.E, columnspan=3 , pady=2)

        # add award columns
        self.row_number = 1

        for award in self.awards_definitions:
            # increment row number
            self.row_number += 1

            # add award label
            self.gui_awards_titles[award] = tk.Label(self.gui_page, text=award, font=('Arial', 16))
            self.gui_awards_titles[award].grid(row=self.row_number , column = 0, sticky=tk.W + tk.E, pady=4)

            # add award winner
            self.gui_awards_winners[award] = tk.Label(self.gui_page, text="-", font=('Arial', 16))
            self.gui_awards_winners[award].grid(row=self.row_number , column = 1, sticky=tk.W + tk.E, pady=4)

            # add award description
            self.gui_awards_descriptions[award] = ttk.Label(self.gui_page, text=self.awards_definitions[award][0], font=('Arial', 12), wraplength = 200, justify= tk.CENTER)
            self.gui_awards_descriptions[award].grid(row=self.row_number , column = 2, pady=4)

    def calcualte_awards(self):
        """Calculates the scores for each player, and thus who wins the award"""
        
        # run through each player
        for player in self.parent.roster:

            # run through each award category and compare if the player beats the previous score
            for award in self.awards_definitions:

                #!! until we get a method for each award, this check needs to be in
                if self.awards_definitions[award][1] == 0:
                    pass
                else:
                    self.process_player_score(award, player)
        
        # update the gui output
        for award in self.awards_definitions:
            self.gui_awards_winners[award].config(text=self.winners[award]["Holder of Highest Score"])
        
        # wipe all the scores so that the next time awards are awarded it is done with a clean slate
        for award in self.awards_definitions:
            self.winners[award]["Highest Recorded Score"] = 0
                    
    
    def process_player_score(self, award, player):
        """Calls the method to work out the score for a player in a given category, then compares to see if it is the highest"""

        try: # we want to skip over instances where there was not enough data to produce a number
            # call the method to calcualte the score for that award
            score = self.awards_definitions[award][1](player)

            # compare this with the current high score
            if score > self.winners[award]["Highest Recorded Score"]:
                self.winners[award]["Highest Recorded Score"] = score
                self.winners[award]["Holder of Highest Score"] = player
            elif score == self.winners[award]["Highest Recorded Score"]:
                if score == 0: # no-one has scored yet
                    self.winners[award]["Holder of Highest Score"] = "-"
                else: # multiple have the highest score
                    self.winners[award]["Holder of Highest Score"] = "Tie"
        except TypeError:
            pass
    
    def mvp_cal(self,player):
        return self.parent.roster[player].marginal_stats[self.tour_name]["marginal total score"]
    
    def o_mvp_cal(self, player):
        return self.parent.roster[player].marginal_stats[self.tour_name]["marginal o-line score"]
    
    def d_mvp_cal(self, player):
        return self.parent.roster[player].marginal_stats[self.tour_name]["marginal d-line score"]
    
    def jug_cal(self, player):
        return self.parent.roster[player].marginal_stats[self.tour_name]["marginal offence conversion"]
    
    def wall_cal(self, player):
        return self.parent.roster[player].marginal_stats[self.tour_name]["marginal defence conversion"]
    
    def bat_cal(self, player):
        score = self.parent.roster[player].data_dict[self.tour_name]["pitch"]["number of possessions played"]
        return score
    
    def glass_cal(self, player):
        m_o_c = self.parent.roster[player].marginal_stats[self.tour_name]["marginal offence conversion"]
        m_d_c = self.parent.roster[player].marginal_stats[self.tour_name]["marginal defence conversion"]

        if m_o_c > 0 and m_d_c < 0:
            score = m_o_c - m_d_c
        else:
            score = 0
        return score
    
    def pac_cal(self, player):
        m_o_c = self.parent.roster[player].marginal_stats[self.tour_name]["marginal offence conversion"]
        m_d_c = self.parent.roster[player].marginal_stats[self.tour_name]["marginal defence conversion"]

        if m_o_c < 0 and m_d_c > 0:
            score = m_d_c - m_o_c
        else:
            score = 0
        return score