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
from tkinter import messagebox


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

        # assign column numbers
        self.pt_n = 0
        self.tc_n = 2
        self.tw_n = 3
        self.result_n = 5
        self.score_n = 6
        self.button_n = 7

        self.s1_n = 1
        self.s2_n = 4

        # configure 8 columns
        self.pt_col = {}
        self.game_page.columnconfigure(self.pt_n, weight=1)
        self.conced_col = {}
        self.game_page.columnconfigure(self.tc_n, weight=2)
        self.win_col = {}
        self.game_page.columnconfigure(self.tw_n, weight=2)
        self.result_col = {}
        self.game_page.columnconfigure(self.result_n, weight=3)
        self.score_col = {}
        self.game_page.columnconfigure(self.score_n, weight=3)
        self.players_button_col = {}
        self.game_page.columnconfigure(self.button_n, weight=1)

        self.s1_col = {}
        self.game_page.columnconfigure(self.s1_n, weight=1)
        self.s2_col = {}
        self.game_page.columnconfigure(self.s2_n, weight=1)


        # add heading labels
        self.pt_num_head = tk.Label(self.game_page, text="Pt", font=('Arial', 18))
        self.pt_num_head.grid(row=0 , column = self.pt_n, sticky=tk.W + tk.E)

        self.concede_head = tk.Label(self.game_page, text="TC", font=('Arial', 18))
        self.concede_head.grid(row=0 , column = self.tc_n, sticky=tk.W + tk.E)

        self.win_head = tk.Label(self.game_page, text="TW", font=('Arial', 18))
        self.win_head.grid(row=0 , column = self.tw_n, sticky=tk.W + tk.E)

        self.result_head = tk.Label(self.game_page, text="Result", font=('Arial', 18))
        self.result_head.grid(row=0 , column = self.result_n, sticky=tk.W + tk.E)

        self.score_head = tk.Label(self.game_page, text="Score", font=('Arial', 18))
        self.score_head.grid(row=0 , column = self.score_n, sticky=tk.W + tk.E)

        # add column separators
        self.s1 = ttk.Separator(self.game_page, orient='vertical')
        self.s1.grid(row=0, column=self.s1_n, sticky="ns", padx=4)

        self.s2 = ttk.Separator(self.game_page, orient='vertical')
        self.s2.grid(row=0, column=self.s2_n, sticky="ns", padx=4)

        # horizontal Separator
        s0 = ttk.Separator(self.game_page, orient='horizontal')
        s0.grid(row=1, column = 0, sticky=tk.W + tk.E, columnspan=8 , pady=5)

    def crunch_data_from_import(self, list_of_turns, list_of_active_players):
        """When using imported data, this function calls other functions to calculate the results"""

        # run the loop for each point to fill each category
        for i in range(len(list_of_turns)):
            none = self.evaluate_point(list_of_turns[i], list_of_active_players[i])

    def _initiate_game_state(self):
        """Looks at the number of turns and calcualtes the points won/lost and turnovers won/lost per point"""
        
        # record who playes each point
        self.point_lineups = {}

        self.team_performance = {
            "Hold or Break" : [],
            "Who Scored" : [],
            "Team Score" : [],
            "Op Score" : [],
            "Disc Won" : [],
            "Disc Lost" : [],
            "Players on Pitch" : [],
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


    def evaluate_point(self, number_of_turns, list_of_active_players):
        """Takes the information from a completed point and updates necessary variables"""
        
        # increment point number
        self.point_number += 1

        # copy out needed info
        self.number_of_turns = number_of_turns
        self.point_lineups[self.point_number] = list_of_active_players

        # get the basic stats
        self._work_out_team_performance()

        # update the game page
        self._update_game_display_tab()
        
        # reset the modifier for who starts the next point on defense
        self.o_start_indicator = 1 - (self.team_point * 2)

        self._update_player_stats()

        # feed the score text value back to the live game tab
        return self.live_score_text


    def _work_out_team_performance(self):
        """Uses the number of turns to work out the team stats"""
        
        # work out whether the point was a hold or a break
        self.hold_or_break = 1 - 2 * (self.number_of_turns % 2) # hold = 1, break = -1

        # update our score accordingly
        self.team_point = (self.o_start_indicator * self.hold_or_break + 1 ) / 2
        self.team_performance["Team Score"].append(self.team_point)

        # work out how many turnovers we won
        self.turnovers_won = int((self.number_of_turns /2) + ((self.hold_or_break - 1) * self.o_start_indicator) / 4)
        self.team_performance["Disc Won"].append(self.turnovers_won)
        self.turnovers_conceded = int(self.number_of_turns - self.turnovers_won)
        self.team_performance["Disc Lost"].append(self.turnovers_conceded)

    def _update_game_display_tab(self):
        """adds a nw row to the table on the game tab"""

        # point number
        self.pt_col[self.point_number] = tk.Label(self.game_page, text=self.point_number, font=('Arial', 16))
        self.pt_col[self.point_number].grid(row=self.point_number+1, column=self.pt_n, sticky=tk.W + tk.E)

        # number of turnovers conceded
        self.conced_col[self.point_number] = tk.Label(self.game_page, text=self.turnovers_conceded, font=('Arial', 16))
        self.conced_col[self.point_number].grid(row=self.point_number+1, column=self.tc_n, sticky=tk.W + tk.E)

        # number of turnovers won
        self.win_col[self.point_number] = tk.Label(self.game_page, text=self.turnovers_won, font=('Arial', 16))
        self.win_col[self.point_number].grid(row=self.point_number+1, column=self.tw_n, sticky=tk.W + tk.E)

        # summary of who won the point
        if self.team_point == 1:
            result_text_1 = "Team "
            self.live_team_score+=1
        else:
            result_text_1 = "Opp "
            self.live_opp_score+=1
        if self.hold_or_break == 1:
            result_text_2 = "hold"
        else:
            result_text_2 = "break"
        self.result_col[self.point_number] = tk.Label(self.game_page, text=result_text_1+result_text_2, font=('Arial', 16))
        self.result_col[self.point_number].grid(row=self.point_number+1, column=self.result_n, sticky=tk.W + tk.E)

        # live score update
        score_text = str(self.live_team_score) + " - " + str(self.live_opp_score)
        self.score_col[self.point_number] = tk.Label(self.game_page, text=score_text, font=('Arial', 16))
        self.score_col[self.point_number].grid(row=self.point_number+1, column=self.score_n, sticky=tk.W + tk.E)

        # create a text representation of the live score for the live tab
        self.live_score_text = "Score: " + str(self.live_team_score) + " - " + str(self.live_opp_score)
        
        # button to show who played that point
        self.players_button_col[self.point_number] = tk.Button(self.game_page, text="+", font=('Arial', 12), command=lambda t=self.point_number: self.show_players_on_pitch(t))
        self.players_button_col[self.point_number].grid(row=self.point_number+1, column=self.button_n, sticky=tk.W + tk.E, pady=2)

        # redraw separators
        self.s1.grid(row=0, rowspan=self.point_number+2, column=self.s1_n, sticky="ns", padx=4)
        self.s2.grid(row=0, rowspan=self.point_number+2, column=self.s2_n, sticky="ns", padx=4)

    def show_players_on_pitch(self, reference_point_number):
        """Brings up a message box listing the players who played that point"""

        messagebox_title = "Point " + str(reference_point_number) + " line-up"
        player_string = ""
        for player in self.point_lineups[reference_point_number]:
            player_string = player_string + player + " // "
        messagebox.showinfo(title=messagebox_title, message=player_string)
        

    def _update_player_stats(self):
        """Feeds relevant stats back to each player"""

        for player in self.parent.team.roster:

            # if the player was on that point
            if player in self.point_lineups[self.point_number]:

                # increment points played by one
                self.parent.team.roster[player].games[self.parent.active_game]["Number of Points Played"] += 1
