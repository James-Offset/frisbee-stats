"""This file holds the class for a single frisbee game. It contains methods to record what happens for each point and to calculate performance"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class FrisbeeGame():
    def __init__(self, parent, game_number, opp_name, defence_start, wind_name=None):
        """This stores the core infomation"""

        # copy out useful variables
        self.parent = parent
        self.name = "G" + str(game_number) + " vs " + opp_name[:7]
        self.opp_name = opp_name
        self.defence_start = defence_start
        self.wind_name = wind_name

        # create a new tab in the GUI
        self.game_page = tk.Frame(self.parent.notebook)
        self.game_page.pack()
        self.parent.notebook.add(self.game_page, text=self.name)

        # set up the GUI
        self._create_game_stats_canvas()

        # set up additional dicitionaries and variables needed to track the match
        self._initiate_game_state()

    def _create_game_stats_canvas(self):
        """Creates the scollable canvas where the player names go"""

        # create the canvas and scrollbar
        self.canvas = tk.Canvas(self.game_page)
        self.v_scrollbar = ttk.Scrollbar(self.game_page, orient='vertical', command=self.canvas.yview)
        self.canvas['yscrollcommand'] = self.v_scrollbar.set
        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        # add a new frame to the canvas
        self.game_record_frame = tk.Frame(self.canvas)
        self.scrollable_window = self.canvas.create_window((0,0), anchor='nw', window=self.game_record_frame)

        # extra scrolling functionality
        self.game_record_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.resize_scrollable_frame)

        # populate the GUI
        self._configure_table()

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
            self.game_record_frame.columnconfigure(column_number, weight=self.gui_grid_dict["column weighting"][column_number])
        
            # add heading labels
            if "separator" in column:
                self.gui_grid_dict["label elements"][column] = ttk.Separator(self.game_record_frame, orient="vertical")
                self.gui_grid_dict["label elements"][column].grid(row=0 , column = column_number, sticky='ns', padx=1)
            else:
                self.gui_grid_dict["label elements"][column] = tk.Label(self.game_record_frame, text=self.gui_grid_dict["heading text"][column_number], font=('Arial', 18))
                self.gui_grid_dict["label elements"][column].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=5)

            column_number += 1

        # remove the button heading text which we had to add in to make the previous bit work
        self.gui_grid_dict["label elements"]["button"].config(text="")

        # horizontal Separator
        s0 = ttk.Separator(self.game_record_frame, orient='horizontal')
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
        """Looks at the number of turns and calculates the points won/lost and turnovers won/lost per point"""
        
        # set up some dictionaries to store game events
        self.point_lineups = {}
        self.list_of_numbers_of_turns = []
        self.wind_direction_list = []

        # create a dictionary to record what happened in each point
        self.team_performance = {
            "Hold or Break" : [],
            "Who Scored" : [],
            "Team Score" : [],
            "Op Score" : [],
            "Disc Won" : [],
            "Disc Lost" : [],
            "Players on Pitch" : [],
        }

        # set up the flag for who starts the first half on defence
        self.establish_start_indicator(False)

        # set up some useful counters
        self.point_number = 0
        self.live_team_score = 0
        self.live_opp_score = 0
        self.wind_direction = 1

        # find out which row position in the dataframe refers to the wind direction
        if self.wind_name == None:
            # playing indoors, no wind
            pass
        else:
            # start a count at 1 because of how the data frame works
            self.wind_row_index = 1 
            for i in self.parent.data_frame_headings:
                # if the heading is the same as the wind name, we found the position
                if i == self.wind_name:
                    break
                else:
                    # increment the count
                    self.wind_row_index += 1

    def establish_start_indicator(self, half_time):
        """At the beginning of the game, or after half time, set the indicator for who starts on offence"""

        # record a modifier for who starts the point on defence
        if self.defence_start == 'Us' or self.defence_start == "My Team":
            self.o_start_indicator = -1
        else:
            self.o_start_indicator = 1

        if half_time == True:
            # switch the starting team
            self.o_start_indicator = self.o_start_indicator * -1

    def half_time_poss_switch(self):
        """Changes the indicator of who started on offence following half time. Method is called from the live game page via button"""

        # log switch of possession
        self.establish_start_indicator(True)

        # change the wind direction
        self.wind_direction *= -1

    def evaluate_point(self, number_of_turns, list_of_active_players):
        """Takes the information from a completed point and updates necessary variables"""
        
        # increment point number
        self.point_number += 1

        # copy out needed info
        self.number_of_turns = number_of_turns
        self.point_lineups[self.point_number] = list_of_active_players

        # store the number of turns if we need to save the info later !! check if this is used at all
        self.list_of_numbers_of_turns.append(self.number_of_turns)
        self.wind_direction_list.append(self.wind_direction)

        # calculate how many possessions each team had and who won the point
        self._work_out_the_number_of_possessions()

        # update the game page
        self._update_game_display_tab()
        
        # reset the modifier for who starts the next point on defence
        self.o_start_indicator = 1 - (self.team_point * 2)

        # update the stats for each individual player
        self._feed_game_information_to_player_classes()
        
        # update the main DataFrame which is used for machine learning
        self.update_main_data_frame()

        # change the wind direction
        self.wind_direction *= -1

        # feed the score text value back to the live game tab
        return self.live_score_text


    def _work_out_the_number_of_possessions(self):
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
        
        # create a dictionary of stats from that point that will be copied for each player who participated
        self.point_stats_list = {
            "number of points played" : 1,
            "number of possessions played" : self.number_of_turns + 1,
            "no. offence possessions" : int(self.turnovers_conceded + self.team_point),
            "no. defence possessions" : int(self.turnovers_won + (1-self.team_point)),
            "turnovers conceded" : self.turnovers_conceded,
            "turnovers won" : self.turnovers_won,
        }
        # >>> copied in each player class, at least for the teammate section

    def _update_game_display_tab(self):
        """adds a new row to the table on the game tab"""

        # increment the display row number
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
        self.live_score_text = "Score: " + score_text

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
                # add a button that can be clicked to see who was on that point
                self.point_gui_rows[self.row_number_ref][element] = tk.Button(self.game_record_frame, text="+", font=('Arial', 12), command=lambda t=self.point_number: self.show_players_on_pitch(t))
                self.point_gui_rows[self.row_number_ref][element].grid(row=self.row_number_ref, column=column_number, sticky=tk.W + tk.E, pady=2)
            elif "separator" in element:
                # redraw the separator from the top
                self.gui_grid_dict["label elements"][element].grid(row=0, rowspan=self.row_number+1, column=column_number, sticky="ns", padx=3)
            else:
                # add a new label displaying the relevant info
                self.point_gui_rows[self.row_number_ref][element] = tk.Label(self.game_record_frame, text=text_entries[element], font=('Arial', 16))
                self.point_gui_rows[self.row_number_ref][element].grid(row=self.row_number_ref, column=column_number, sticky='ew')

            # increment column number
            column_number += 1

    def show_players_on_pitch(self, reference_point_number):
        """Brings up a message box listing the players who played that point"""

        messagebox_title = "Point " + str(reference_point_number) + " line-up"
        message_string = ""
        for player in self.point_lineups[reference_point_number]:
            message_string = message_string + player + " // "
        wind_direction_indicator = int((self.wind_direction + 3) / 2)
        message_string = message_string + "Wind direction " + str(wind_direction_indicator)
        messagebox.showinfo(title=messagebox_title, message=message_string)
        

    def _feed_game_information_to_player_classes(self):
        """Feeds relevant stats back to each player"""

        # update the stats record for the full team
        self.parent.team.team_record.update_point_data(self.point_stats_list, self.parent.team_name)

        # update the stats for each player on the pitch
        for player in self.parent.team.roster:

            # call the function for that player
            self.parent.team.roster[player].update_point_data(self.point_stats_list, self.point_lineups[self.point_number])

    def update_main_data_frame(self):
        """Looks at what happened during the point and updates the main data frame"""
        
        # create an empty list for the new row of data, this will be copied out multiple times
        new_row = []

        # the first entry is the success measure. We will copy the row for each possession concede first (success = 0)
        new_row.append(0)

        # player records
        # log a 1 or a zero depending on whether the player is on the field
        for factor in self.parent.data_frame_headings:
            if factor in self.point_lineups[self.point_number] + [self.opp_name]:
                new_row.append(1)
            else:
                new_row.append(0)

        # fix the indicator for the wind direction
        if self.wind_name == None:
            # playing indoors, no wind
            pass
        else:
            new_row[self.wind_row_index] = self.wind_direction

        # each time we concede a turnover, copy out the row
        for i in range(self.turnovers_conceded):
            self.parent.mldf["offence"].loc[len(self.parent.mldf["offence"])] = new_row

        # if we lose the point, copy out the row
        if self.team_point == 0:
            self.parent.mldf["defence"].loc[len(self.parent.mldf["defence"])] = new_row

        # switch to logging team successes
        new_row[0] = 1

        # for each possesion won, copy out the row
        for i in range(self.turnovers_won):
            self.parent.mldf["defence"].loc[len(self.parent.mldf["defence"])] = new_row

        # if we scored the point, copy out the row
        if self.team_point == 1:
            self.parent.mldf["offence"].loc[len(self.parent.mldf["offence"])] = new_row

