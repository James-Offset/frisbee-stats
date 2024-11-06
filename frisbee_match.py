"""This file holds the class for a single frisbee game

The main purpose of this class will be to capture the line-ups for each point and the number of turn-overs per point.
Ideally we would have some kind of readout displaying the live score

Meta data would be the game number, opposition name, maybe date and time, who starts on offence

Functions:
Capture the line-up for a point (maybe by calling a function within the point class)
Work out what the live score is + print whether last point was a hold or a break
Initiate half time
calculate stats for just this game > maybe call another class



Calculate overall game stats: num_points, num_turns, num_o_starts, num_possessions, avg_poss_per_point
Turns Won
Turns Lost
No. O Posessions
No. D Posessions

Score rate
Pos Loss Rate
Concede rate
Pos Win Rate

Predicted Goals for
Predicted Goals Against
Net

O start goal
O start concede
D start goal
D start concede

O goal rate
O concede rate
D goal rate
D concede rate

Pos / OG
Pos / OC
Pos / DG
Pos / DC

No. O / OG
No. D / OG
No. D / DG
No. O / DG

"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk


class FrisbeeGame():
    def __init__(self, parent, name):
        """This stores the core infomation"""

        # copy out useful variables
        self.parent = parent
        self.name = name

        # create a new tab in the GUI
        self.game_page = tk.Frame(self.parent.notebook)
        self.game_page.pack()
        self.parent.notebook.add(self.game_page, text=self.name)

        self._configure_table()

        self._initiate_game_state()

    def _configure_table(self):
        """Sets up the table that presents the game summary on the game tab"""

        # configure 6 columns
        self.pt_col = {}
        self.game_page.columnconfigure(0, weight=1)
        self.start_col = {}
        self.game_page.columnconfigure(1, weight=2)
        self.conced_col = {}
        self.game_page.columnconfigure(2, weight=2)
        self.win_col = {}
        self.game_page.columnconfigure(3, weight=2)
        self.result_col = {}
        self.game_page.columnconfigure(4, weight=3)
        self.score_col = {}
        self.game_page.columnconfigure(5, weight=3)

        # add heading labels
        self.pt_num_head = tk.Label(self.game_page, text="Pt", font=('Arial', 18))
        self.pt_num_head.grid(row=0 , column = 0, sticky=tk.W + tk.E)

        self.start_head = tk.Label(self.game_page, text="Start", font=('Arial', 18))
        self.start_head.grid(row=0 , column = 1, sticky=tk.W + tk.E)

        self.concede_head = tk.Label(self.game_page, text="Turn Con", font=('Arial', 18))
        self.concede_head.grid(row=0 , column = 2, sticky=tk.W + tk.E)

        self.win_head = tk.Label(self.game_page, text="Turn Won", font=('Arial', 18))
        self.win_head.grid(row=0 , column = 3, sticky=tk.W + tk.E)

        self.result_head = tk.Label(self.game_page, text="Result", font=('Arial', 18))
        self.result_head.grid(row=0 , column = 4, sticky=tk.W + tk.E)

        self.score_head = tk.Label(self.game_page, text="Live Score", font=('Arial', 18))
        self.score_head.grid(row=0 , column = 5, sticky=tk.W + tk.E)


    def crunch_data_from_import(self, list_of_turns):
        """When using imported data, this function calls other functions to calculate the results"""

        self.list_of_turns = list_of_turns

        # run the loop for each point to fill each category
        for number_of_turns in self.list_of_turns:
            none = self.evaluate_point(number_of_turns)

    def _initiate_game_state(self):
        """Looks at the number of turns and calcualtes the points won/lost and turnovers won/lost per point"""
        self.team_performance = {
            "Hold or Break" : [],
            "Who Scored" : [],
            "Team Score" : [],
            "Op Score" : [],
            "Disc Won" : [],
            "Disc Lost" : []
        }

        #!! Fix this
        self.defence_start = 'Us'

        # record a modifier for who starts on defence
        if self.defence_start == 'Us':
            self.o_start_indicator = -1
        else:
            self.o_start_indicator = 1

        self.point_number = 0
        self.live_team_score = 0
        self.live_opp_score = 0

            

    def evaluate_point(self, number_of_turns):
        """Takes the information from a completed point and updates necessary variables"""

        # increment point number
        self.point_number += 1
        
        # work out whether the point was a hold or a break
        hold_or_break = 1 - 2 * (number_of_turns % 2) # hold = 1, break = -1

        # update our score accordingly
        our_score = (self.o_start_indicator * hold_or_break + 1 ) / 2
        self.team_performance["Team Score"].append(our_score)

        # work out how many turnovers we won
        turnovers_won = int((number_of_turns /2) + ((hold_or_break - 1) * self.o_start_indicator) / 4)
        self.team_performance["Disc Won"].append(turnovers_won)
        turnovers_conceded = int(number_of_turns - turnovers_won)
        self.team_performance["Disc Lost"].append(turnovers_conceded)

        # update the display table
        self.pt_col[self.point_number] = tk.Label(self.game_page, text=self.point_number, font=('Arial', 16))
        self.pt_col[self.point_number].grid(row=self.point_number, column=0, sticky=tk.W + tk.E)

        if self.o_start_indicator == 1:
            start_text = "Team"
        else:
            start_text = "Opp"
        self.start_col[self.point_number] = tk.Label(self.game_page, text=start_text, font=('Arial', 16))
        self.start_col[self.point_number].grid(row=self.point_number, column=1, sticky=tk.W + tk.E)

        self.conced_col[self.point_number] = tk.Label(self.game_page, text=turnovers_conceded, font=('Arial', 16))
        self.conced_col[self.point_number].grid(row=self.point_number, column=2, sticky=tk.W + tk.E)

        self.win_col[self.point_number] = tk.Label(self.game_page, text=turnovers_won, font=('Arial', 16))
        self.win_col[self.point_number].grid(row=self.point_number, column=3, sticky=tk.W + tk.E)

        if our_score == 1:
            result_text_1 = "Team "
            self.live_team_score+=1
        else:
            result_text_1 = "Opp "
            self.live_opp_score+=1
        if hold_or_break == 1:
            result_text_2 = "hold"
        else:
            result_text_2 = "break"
        self.result_col[self.point_number] = tk.Label(self.game_page, text=result_text_1+result_text_2, font=('Arial', 16))
        self.result_col[self.point_number].grid(row=self.point_number, column=4, sticky=tk.W + tk.E)

        score_text = str(self.live_team_score) + " - " + str(self.live_opp_score)
        self.score_col[self.point_number] = tk.Label(self.game_page, text=score_text, font=('Arial', 16))
        self.score_col[self.point_number].grid(row=self.point_number, column=5, sticky=tk.W + tk.E)

        # reset the modifier for who starts the next point on defense
        self.o_start_indicator = 1 - (our_score * 2)

        # create a text representation of the live score for the live tab
        live_score_text = "Score: " + str(self.live_team_score) + " - " + str(self.live_opp_score)

        return live_score_text
            
