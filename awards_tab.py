"""This file holds the class that defines the functions for the team awards tab and functions"""

import tkinter as tk
from tkinter import ttk

class AwardsTab():
    def __init__(self, parent):
        """Copy out variables and set up the GUI"""

        # copy out needed variables
        self.parent = parent
        self.tour_name = self.parent.tournament_name

        # create the list of awards
        self._establish_awards()

        # build the GUI
        self._create_notebook_tab()

    def _establish_awards(self):
        """Creates the data structure for the awards and link them to the calcualtion method"""

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

        #!! since we haven't got a function for each award yet, we add another step
        self.list_of_valid_awards = []
        for award in self.awards_definitions:
            if self.awards_definitions[award][1] == 0:
                pass # way to determine winner does not exist yet
            else:
                self.list_of_valid_awards.append(award)

                self.winners[award] = {
                    "Highest Recorded Score" : 0,
                    "Holder of Highest Score" : "-",
                }

    def _create_notebook_tab(self):
        """Creates a new tab in the notebook and sets up scroll capability"""

        # create the new tab
        self.tab_page = tk.Frame(self.parent.parent.notebook)
        self.tab_page.pack()
        self.parent.parent.notebook.add(self.tab_page, text="Awards")

        # create the canvas and scrollbar
        self.canvas = tk.Canvas(self.tab_page)
        self.v_scrollbar = ttk.Scrollbar(self.tab_page, orient='vertical', command=self.canvas.yview)
        self.canvas['yscrollcommand'] = self.v_scrollbar.set
        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        # add a new frame to the canvas
        self.awards_frame = tk.Frame(self.canvas)
        self.scrollable_window = self.canvas.create_window((0,0), anchor='nw', window=self.awards_frame)

        # extra scrolling functionality
        #!! self.awards_frame.bind("<Configure>", self.update_scroll_region)
        #self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.resize_scrollable_frame)

        # fill out the inner frame
        self._create_awards_grid_content()

    def resize_scrollable_frame(self, event):
        # Ensure the frame width matches the canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_window, width=canvas_width)

    def update_scroll_region(self, event):
        # Update the scroll region when the frame changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        # Enable mousewheel scrolling
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def _create_awards_grid_content(self):
        """"Adds the GUI label elements into a grid inside the scrollable frame"""

        # create a dictionary to hold the details of the GUI columns
        self.gui_columns = {
            "heading text" : ["Award", "Winner", "Description"],
            "column weighting" : [2, 2, 4],
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
            self.awards_frame.columnconfigure(column_number, weight=self.gui_columns["column weighting"][column_number])
        
            # add heading labels
            if "separator" in column:
                self.gui_columns["label elements"][column] = ttk.Separator(self.awards_frame, orient="vertical")
                self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky='ns', padx=2)
            else:
                self.gui_columns["label elements"][column] = tk.Label(self.awards_frame, text=self.gui_columns["heading text"][column_number], font=('Arial', 18))
                self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=10)

            column_number += 1
        
        # horizontal Separator
        s0 = ttk.Separator(self.awards_frame, orient='horizontal')
        s0.grid(row=1, column = 0, sticky=tk.W + tk.E, columnspan=3 , pady=2)

        # add award columns
        self.row_number = 1

        # create a new row for each award
        for award in self.list_of_valid_awards:

            # increment row number
            self.row_number += 1

            # add award label
            self.gui_awards_titles[award] = tk.Label(self.awards_frame, text=award, font=('Arial', 16))
            self.gui_awards_titles[award].grid(row=self.row_number , column = 0, sticky=tk.W + tk.E, pady=4)

            # add award winner
            self.gui_awards_winners[award] = tk.Label(self.awards_frame, text="-", font=('Arial', 16))
            self.gui_awards_winners[award].grid(row=self.row_number , column = 1, sticky=tk.W + tk.E, pady=4)

            # add award description
            self.gui_awards_descriptions[award] = ttk.Label(self.awards_frame, text=self.awards_definitions[award][0], font=('Arial', 12), wraplength = 200, justify= tk.CENTER)
            self.gui_awards_descriptions[award].grid(row=self.row_number , column = 2, pady=4)


    def calculate_awards(self):
        """Calculates the scores for each player, and thus who wins the award"""

        # run through each award category 
        for award in self.list_of_valid_awards:
        
            # run through each player and compare if the player beats the previous score
            for player in self.parent.roster:
                self.process_player_score(award, player)
        
            # update the gui output
            self.gui_awards_winners[award].config(text=self.winners[award]["Holder of Highest Score"])
        
            # wipe all the scores so that the next time awards are awarded it is done with a clean slate
            self.winners[award]["Highest Recorded Score"] = 0
                    
    
    def process_player_score(self, award, player):
        """Calls the method to work out the score for a player in a given category, then compares to see if it is the highest"""

        try: # we want to skip over instances where there was not enough data to produce a number
            # call the method to calcualte the score for that award
            score = self.awards_definitions[award][1](player)

            # compare this with the current high score
            if score > self.winners[award]["Highest Recorded Score"]:
                # update the new high score and add the player name
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
        return self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal total score"]
    
    def o_mvp_cal(self, player):
        return self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal o-line score"]
    
    def d_mvp_cal(self, player):
        return self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal d-line score"]
    
    def jug_cal(self, player):
        return self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal offence conversion rate"]
    
    def wall_cal(self, player):
        return self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal defence conversion rate"]
    
    def bat_cal(self, player):
        score = self.parent.roster[player].data_dict[self.tour_name]["pitch"]["number of possessions played"]
        return score
    
    def glass_cal(self, player):
        m_o_c = self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal offence conversion rate"]
        m_d_c = self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal defence conversion rate"]

        if m_o_c > 0 and m_d_c < 0:
            score = m_o_c - m_d_c
        else:
            score = 0
        return score
    
    def pac_cal(self, player):
        m_o_c = self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal offence conversion rate"]
        m_d_c = self.parent.roster[player].data_dict[self.tour_name]["pitch"]["marginal defence conversion rate"]

        if m_o_c < 0 and m_d_c > 0:
            score = m_d_c - m_o_c
        else:
            score = 0
        return score