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

        # create a dictionary to hold the details of the GUI columns
        self.gui_grid_dict = {
            "heading text" : [
                "P", 
                "separator1", 
                "TC", 
                "TW", 
                "separator2",
                "Result",
                "Score",
                "button",
                ],
            "column weighting" : [1, 2, 1, 2, 3, 1, 3, 1],
            "label elements" : {}
        } #>>>> Repeat this in the point update method

        # neaten this later !!
        self.separator_column_number = 1

        column_number=0
        for column in self.gui_grid_dict["heading text"]:
            # create a column
            self.game_page.columnconfigure(column_number, weight=self.gui_grid_dict["column weighting"][column_number])
        
            # add heading labels
            if "separator" in column:
                self.gui_grid_dict["label elements"][column] = ttk.Separator(self.game_page, orient="vertical")
                self.gui_grid_dict["label elements"][column].grid(row=0 , column = column_number, sticky='ns', padx=1)
            else:
                self.gui_grid_dict["label elements"][column] = tk.Label(self.game_page, text=self.gui_grid_dict["heading text"][column_number], font=('Arial', 18))
                self.gui_grid_dict["label elements"][column].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=5)

            column_number += 1

        # remove the button heading text
        self.gui_grid_dict["label elements"]["button"].config(text="")

        # horizontal Separator
        s0 = ttk.Separator(self.game_page, orient='horizontal')
        s0.grid(row=1, column = 0, sticky=tk.W + tk.E, columnspan=8 , pady=5)

        # create a dictionary to hold the gui elements for each point, which will have its own row of the table
        self.point_gui_rows = {}

        # set the starting row number
        self.row_number = 1

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
        
        # reset the modifier for who starts the next point on defence
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
        
        # player stats list
        self.point_stats_list = {
            "number of points played" : 1,
            "number of possessions played" : self.number_of_turns + 1,
            "no. offence possessions" : int(self.turnovers_conceded + self.team_point),
            "no. defence possessions" : int(self.turnovers_won + (1-self.team_point)),
            "turnovers conceded" : self.turnovers_conceded,
            "turnovers won" : self.turnovers_won,
        }

        # save these in case we need them later
        self.extra_stats = {
        }

    def _update_game_display_tab(self):
        """adds a new row to the table on the game tab"""

        # increment row number
        self.row_number += 1
        self.row_number_ref = str(self.row_number)

        # create a new sub-dictionary to hold the gui elements for that row
        self.point_gui_rows[self.row_number_ref] = {}

        # work out non-trivial text elements:
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

        # live score update
        score_text = str(self.live_team_score) + " - " + str(self.live_opp_score)

        # create a text representation of the live score for the live tab
        self.live_score_text = "Score: " + str(self.live_team_score) + " - " + str(self.live_opp_score)

        # update text entries
        text_entries = {
            "P" : self.point_number,
            "separator1" : None,
            "TC" : self.turnovers_conceded,
            "TW" : self.turnovers_won,
            "separator2": None,
            "Result" : result_text_1+result_text_2,
            "Score" : score_text,
            "button" : None,
        } # <<<< copied from the table set up function

        # for each data point that will need to be shown, create a label to hold it and add it to the grid. (both fixed and variable data)
        column_number = 0        
        for element in self.gui_grid_dict["heading text"]:
            if element == "button":
                # add a button
                self.point_gui_rows[self.row_number_ref][element] = tk.Button(self.game_page, text="+", font=('Arial', 12), command=lambda t=self.point_number: self.show_players_on_pitch(t))
                self.point_gui_rows[self.row_number_ref][element].grid(row=self.row_number_ref, column=column_number, sticky=tk.W + tk.E, pady=2)
            elif "separator" in element:
                # redraw the separator from the top
                self.gui_grid_dict["label elements"][element].grid(row=0, rowspan=self.row_number+1, column=column_number, sticky="ns", padx=3)
            else:
                # add a new label
                self.point_gui_rows[self.row_number_ref][element] = tk.Label(self.game_page, text=text_entries[element], font=('Arial', 16))
                self.point_gui_rows[self.row_number_ref][element].grid(row=self.row_number_ref, column=column_number, sticky='ew')

            # increment column number
            column_number += 1

    def show_players_on_pitch(self, reference_point_number):
        """Brings up a message box listing the players who played that point"""

        messagebox_title = "Point " + str(reference_point_number) + " line-up"
        player_string = ""
        for player in self.point_lineups[reference_point_number]:
            player_string = player_string + player + " // "
        messagebox.showinfo(title=messagebox_title, message=player_string)
        

    def _update_player_stats(self):
        """Feeds relevant stats back to each player"""

        # update the stats record for the full team
        self.parent.team.team_record.update_point_data(self.point_stats_list, self.parent.team_name)

        # update the stats for each player on the pitch
        for player in self.parent.team.roster:

            # if the player was on that point
            if player in self.point_lineups[self.point_number]:
                pass_name = player
            else:
                pass_name = self.parent.team_name

            # call the function for that player
            self.parent.team.roster[player].update_point_data(self.point_stats_list, pass_name)


