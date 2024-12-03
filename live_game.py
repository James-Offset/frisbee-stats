"""This file is to handle the tab for the live game and allow for new data input"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk

class LiveGame():
    def __init__(self, parent):
        # copy out key parent parts
        self.parent = parent

        # collect key game meta info: !!
        self.opp_name_text = "Opponent"
        self.team_starting_on_O = "Opp Possession"
        self.number_of_players_at_once = self.parent.number_of_players_at_once
        self.default_count_message = "Please select " + str(self.number_of_players_at_once) + " players"
        
        # set the second half flag
        self.second_half = False

        # put a roster page on the main GUI
        self._build_live_page()

    def _build_live_page(self):
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

        # set a row count so it is easier to add new rows
        row_count = -1

        # Separator
        row_count+=1
        s0 = ttk.Separator(self.live_page, orient='horizontal')
        s0.grid(row=row_count, column = 0, sticky=tk.W + tk.E, columnspan=5 , pady=10)

        # add the top row: Opp, Score, scorebox
        row_count+=1

        self.opp_name = tk.Label(self.live_page, text=self.opp_name_text, font=('Arial', 18))
        self.opp_name.grid(row=row_count , column = 0, sticky=tk.W + tk.E, columnspan=2, pady=5)

        self.score_readout = tk.StringVar()
        self.live_score = tk.Label(self.live_page, textvariable=self.score_readout, font=('Arial', 18))
        self.live_score.grid(row=row_count , column = 4, sticky=tk.W + tk.E)
        self.score_readout.set("Score: 0 - 0")

        # Separator
        row_count+=1
        s1 = ttk.Separator(self.live_page, orient='horizontal')
        s1.grid(row=row_count, column = 0, sticky=tk.W + tk.E, columnspan=5 , pady=10)

        # First row (after zero): Turnover Heading
        row_count += 1

        self.turnover_label = tk.Label(self.live_page, text="Turnovers:", font=('Arial', 18))
        self.turnover_label.grid(row=row_count , column =0 , sticky=tk.W + tk.E, columnspan=3)

        self.posession_text = tk.StringVar()
        self.posession_label = tk.Label(self.live_page, textvariable=self.posession_text, width=18, font=('Arial', 18))
        self.posession_label.grid(row=row_count , column =4 , sticky=tk.W + tk.E)
        self.posession_text.set(self.team_starting_on_O)

        # Second Row: minus, turns count, plus, space, end button
        row_count+=1

        self.minus_button = tk.Button(self.live_page, text="-", font=('Arial', 20), width=3, command=self.minus_function)
        self.minus_button.grid(row=row_count , column =0 , sticky= tk.E)

        self.turnover_count = 0
        self.turnover_count_value = tk.IntVar()
        self.count_label = tk.Label(self.live_page, textvariable=self.turnover_count_value, font=('Arial', 18))
        self.count_label.grid(row=row_count , column =1 , sticky=tk.W + tk.E)
        self.turnover_count_value.set(self.turnover_count)

        self.plus_button = tk.Button(self.live_page, text="+", font=('Arial', 20), width=3, command=self.plus_function)
        self.plus_button.grid(row=row_count , column =2 , sticky=tk.W , pady=10)

        self.end_button = tk.Button(self.live_page, text="End point", font=('Arial', 18), command=self.end_point)
        self.end_button.grid(row=row_count , column =4 , sticky=tk.W + tk.E)

        # Separator
        row_count+=1
        s2 = ttk.Separator(self.live_page, orient='horizontal')
        s2.grid(row=row_count, column = 0, sticky=tk.W + tk.E, columnspan=5 , pady=10)

        # third row: player name, player number, on pitch, blanks
        row_count+=1

        self.r_head_1 = tk.Label(self.live_page, text="Player Name", font=('Arial', 18))
        self.r_head_1.grid(row=row_count , column = 0, sticky=tk.W + tk.E, columnspan=2, pady=10)

        self.r_head_2 = tk.Label(self.live_page, text="#", font=('Arial', 18))
        self.r_head_2.grid(row=row_count , column = 2, sticky=tk.W + tk.E)
        
        # create a roster table
        self.roster_widgets = {}
        row_count_memory = row_count-1

        for player in self.parent.team.roster:
            # create a plater profile to manage their widgets
            self.roster_widgets[player] = {}

            row_count+=1
            self.roster_widgets[player]["name_col"] = tk.Label(self.live_page, text=player, font=('Arial', 16))
            self.roster_widgets[player]["name_col"].grid(row=row_count , column =0 , sticky=tk.W + tk.E, columnspan=2)

            number_text = self.parent.team.roster[player].number
            self.roster_widgets[player]["number_col"] = tk.Label(self.live_page, text=number_text, font=('Arial', 16))
            self.roster_widgets[player]["number_col"].grid(row=row_count , column =2 , sticky=tk.W + tk.E)

            # add checkboxes here
            self.roster_widgets[player]["checkbox_value"] = tk.IntVar()
            self.roster_widgets[player]["check_col"] = tk.Checkbutton(self.live_page, variable=self.roster_widgets[player]["checkbox_value"], command=self.update_player_total)
            self.roster_widgets[player]["check_col"].grid(row=row_count , column=3 , sticky=tk.W + tk.E)

        # Add a label showing the total number of players
        row_count_memory += 1

        self.player_count_label = tk.Label(self.live_page, text="Players on:", font=('Arial', 16))
        self.player_count_label.grid(row=row_count_memory , column = 4, sticky=tk.W + tk.E + tk.N, columnspan=2)

        row_count_memory+=1
        self.player_count = tk.IntVar()
        self.player_count_display = tk.Label(self.live_page, textvariable=self.player_count, width = 6, font=('Arial', 18), bg='gray90')
        self.player_count_display.grid(row=row_count_memory , column = 4)
        self.player_count.set(0)

        row_count_memory+=1
        self.entry_message = tk.StringVar()
        self.entry_message_label = tk.Label(self.live_page, textvariable=self.entry_message, wraplength=80, font=('Arial', 12))
        self.entry_message_label.grid(row=row_count_memory , rowspan=3, column = 4, sticky=tk.W + tk.E)
        self.entry_message.set(self.default_count_message)

        row_count_memory+=4
        self.half_time_button = ttk.Button(self.live_page, text="Half Time", command=self.half_time)
        self.half_time_button.grid(row=row_count_memory, column=4)

        row_count_memory+=2
        self.end_game_button = tk.Button(self.live_page, text="End Game", font=('Arial', 18), command=self.end_game)
        self.end_game_button.grid(row=row_count_memory, column=4)

    def plus_function(self):
        """Increments the turnover count when the plus button is pressed"""
        self.turnover_count += 1
        self.turnover_count_value.set(self.turnover_count)
        self.switch_possession_text()

    def minus_function(self):
        """decreases the turnover count when the minus button is pressed"""
        if self.turnover_count > 0:
            self.turnover_count -= 1
            self.turnover_count_value.set(self.turnover_count)   
            self.switch_possession_text()

    def switch_possession_text(self):
        """Updates the text in the textbox of who has possession whenever there is a turnover"""
        if self.posession_text.get() == "Opp Possession":
            new_posession_text = "Team Possession"
        else:
            new_posession_text = "Opp Possession"
        self.posession_text.set(new_posession_text)

        # activate or deactivate the half time button as necessary
        if self.second_half == True or self.turnover_count > 0:
            self.half_time_button.state(["disabled"])
        else:
            self.half_time_button.state(["!disabled"])

    def update_player_total(self):
        """When a checkbox is checked or unchecked, we update the count of checked boxes"""
        players_checked = 0
        for player in self.roster_widgets:
            checkbox_value = self.roster_widgets[player]["checkbox_value"].get()
            players_checked += checkbox_value
        
        self.player_count.set(players_checked)

        # update the message if we have exactly the right number of players
        if players_checked == self.number_of_players_at_once:
            self.entry_message.set("Correct number of players")
            self.player_count_display.config(bg='PaleGreen')
        else:
            self.entry_message.set(self.default_count_message)
            self.player_count_display.config(bg='gray90')
        

    def end_point(self):
        """At the end of the point, log all the data and clear the roster for the next point"""

        # record who was playing
        active_players = []

        # clear the checkboxes
        for player in self.roster_widgets:
            if self.roster_widgets[player]["checkbox_value"].get() == 1:
                active_players.append(player)
                self.roster_widgets[player]["checkbox_value"].set(0)
        
        # reset the checkbox count
        self.player_count.set(0)
        self.entry_message.set(self.default_count_message)
        self.player_count_display.config(bg='gray90')

        # call the end point function in the active game
        new_score_text = self.parent.games[self.parent.active_game].evaluate_point(self.turnover_count, active_players)

        # update the live score label
        self.score_readout.set(new_score_text)

        # reset the turnover count
        self.turnover_count = 0 
        self.turnover_count_value.set(self.turnover_count)

        # switch the possession indicator
        self.switch_possession_text()

    def half_time(self):
        """Indicates that it is half time and switches possession"""

        # change the record for the team that started on o
        self.parent.games[self.parent.active_game].half_time_poss_switch()

        # deactivate button
        self.second_half = True

        # change the text indication
        self.switch_possession_text()

    def end_game(self):
        """Ends the live game"""

        # call the function to do comparison stats calculations
        self.parent.team.end_of_game_calcs()
        
        # close the live game tab
        self.parent.live_game_active=False
        self.live_page.destroy()


