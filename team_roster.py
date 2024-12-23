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
from awards_tab import AwardsTab



class Team():
    """A class to manage all the functions relating to the team roster"""

    def __init__(self, parent):
        """Initial set up"""

        # copy out key parent parts
        self.parent = parent

        # set the threshold of what counts a significant ratio of data
        self.player_v_team_ratio = 0.2
        self.player_v_player_ratio = 0.25

        # create a dictionary to hold the player classes
        self.number_of_players = 0 
        self.display_row_number = 0
        self.roster={}

        # create a dictionary to hold the display frames for the tabs
        self.game_stats_pages = {} # holds the other two frames
        self.team_frame = {} # holds the team info table
        self.player_frame = {} # holds the player info table

        # create dictionaries to hold gui display elements within those frames
        self.tf_heading_elements = {}
        self.tf_separator_elements = {}
        self.pf_heading_elements = {}
        self.pf_separator_elements = {}

        # Get tournament name !!"MIR 2017"
        self.tournament_name = parent.tournament_name
        self.team_name = parent.team_name

        # create a player class that actually represents the whole team
        self.team_record = Player(self, self.team_name, 0, -1)

        # put a roster page on the main GUI for the full tournaments stats
        self.build_game_stats_page(self.tournament_name)

        # create the awards tab
        self.awards_class = AwardsTab(self)

    def build_game_stats_page(self, tab_name):
        """Prepares the team records and builds the two sections of the gui tabs"""

        # create the new tab
        self.game_stats_pages[tab_name] = tk.Frame(self.parent.notebook)
        self.game_stats_pages[tab_name].pack(fill=tk.BOTH, expand=True)
        tab_label = tab_name[:7] + " Stats"
        self.parent.notebook.add(self.game_stats_pages[tab_name], text=tab_label)

        # set up the two sections of the tab
        self._create_team_section(tab_name)
        self._create_player_section(tab_name)

        # doesn't fit with the rest of the function, but we need the team stats dictionary to make a new subfolder
        self.team_record.prepare_to_receive_data(tab_name)

    def _create_team_section(self, tab_name):
        """Creates the grid for the team information"""
        
        # create frame to hold section
        self.team_frame[tab_name] = tk.Frame(self.game_stats_pages[tab_name])
        self.team_frame[tab_name].grid(row=0, column=0, sticky="nsew")

        # configure the tab frame
        self.game_stats_pages[tab_name].grid_rowconfigure(0, weight=1)
        self.game_stats_pages[tab_name].grid_columnconfigure(0, weight=1)

        # create a dictionary to hold the details of the GUI columns
        self.team_gui_headings = [
            "Team Performance",
            ".",
            ]
        # <<< These correspond to ???
        
        self.tf_heading_elements[tab_name] = {}
        
        # decide where to put separators
        self.tf_separator_columns = []

        # create a dictionary to keep the separators in
        self.tf_separator_elements[tab_name] = {}

        column_number=0
        for heading in self.team_gui_headings:
            
            if column_number in self.tf_separator_columns:
                # create a column for the separator
                self.team_frame[tab_name].columnconfigure(column_number, weight=1)
                self.tf_separator_elements[tab_name][str(column_number)] = ttk.Separator(self.team_frame[tab_name], orient="vertical")
                self.tf_separator_elements[tab_name][str(column_number)].grid(row=0 , rowspan=1, column = column_number, sticky='ns', padx=2)

                column_number += 1
            
            # create a column for the heading
            self.team_frame[tab_name].columnconfigure(column_number, weight=1)
        
            # add heading labels
            self.tf_heading_elements[tab_name][heading] = tk.Label(self.team_frame[tab_name], text=heading, font=('Arial', 18))
            self.tf_heading_elements[tab_name][heading].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=10)

            column_number += 1

    def _create_player_section(self, tab_name):    
        """Creates the basic grid for the roster page, not filled in"""

        # create frame to hold section
        self.player_frame[tab_name] = tk.Frame(self.game_stats_pages[tab_name])
        self.player_frame[tab_name].grid(row=1, column=0, sticky="nsew")

        # configure the tab frame
        self.game_stats_pages[tab_name].grid_rowconfigure(1, weight=1)

        # create a dictionary to hold the details of the GUI columns
        self.player_gui_headings = [
            "Player", 
            "#", 
            "PP", 
            "OP",
            "DP",
            "OC",
            "DC",
            "MO",
            "MD",
            "OS",
            "DS", 
            "TS",
            ]
        # <<< These correspond to the output stats in the player class
        
        self.pf_heading_elements[tab_name] = {}
        
        # decide where to put separators
        self.pf_separator_columns = [2, 8]

        # create a dictionary to keep the separators in
        self.pf_separator_elements[tab_name] = {}

        column_number=0
        for heading in self.player_gui_headings:
            
            if column_number in self.pf_separator_columns:
                # create a column for the separator
                self.player_frame[tab_name].columnconfigure(column_number, weight=1)
                self.pf_separator_elements[tab_name][str(column_number)] = ttk.Separator(self.player_frame[tab_name], orient="vertical")
                self.pf_separator_elements[tab_name][str(column_number)].grid(row=0 , rowspan=1, column = column_number, sticky='ns', padx=2)

                column_number += 1
            
            # create a column for the heading
            self.player_frame[tab_name].columnconfigure(column_number, weight=1)
        
            # add heading labels
            self.pf_heading_elements[tab_name][heading] = tk.Label(self.player_frame[tab_name], text=heading, font=('Arial', 18))
            self.pf_heading_elements[tab_name][heading].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=10)

            column_number += 1

    def check_manual_player_entry(self, name_entry, number_entry):
        """Checks whether the user input is valid"""

        # set an error as the default
        error_message = None

        # check the number first, so name error overrides. Start with check for integer
        try:
            player_number = int(number_entry)
        except ValueError:
            error_message = "Number entered must be an integer with no other characters"
        else:
            if player_number < 0:
                error_message = "Player number must be at least zero"
            elif player_number > 99:
                error_message = "Player number must be less than 100"
            else:
                # check if this number is already taken
                for player in self.roster:
                    if player_number == self.roster[player].number:
                        error_message = "Player number already taken"
                        break
            
        # then check if the name is a valid string
        try:
            name_entry = name_entry[:-1] # take off the new line that gets added
            if len(name_entry) > 10:
                error_message = "Name entered cannot be longer than 10 characters"
            elif name_entry == self.team_name:
                error_message = "Name cannot match the team name"
            elif name_entry in self.roster:
                error_message = "Name already taken, please choose another"
        except Exception:
            error_message = "Unknown error, please enter name again"

        if error_message == None:
            # add the player to the roster
            self.new_player_entry(name_entry, player_number)
            error_message = "Player successfully added to roster"
            self.parent.player_name_box.delete('1.0', tk.END)
            self.parent.player_number_box.delete('1.0', tk.END)
        
        return error_message

    def new_player_entry(self, player_name, player_number):
        """Creates a class to for a new player"""
        
        # increment the number of players
        self.number_of_players += 1

        # check if the total number of players is sufficient for a game
        if self.number_of_players == self.parent.number_of_players_at_once:
            # allow for the first game to begin
            self.parent.new_game_button.state(["!disabled"])

        # increment the row for which this player will be displayed on the gui
        self.display_row_number += 1

        # create a new teammate data profile in each other player class
        for teammate in self.roster:
            self.roster[teammate].add_teammate_to_list(player_name)

        # create a new class
        self.roster[player_name] = Player(self, player_name, player_number, self.display_row_number)

        # add the player to the home page data frame
        self.add_player_to_main_DF(player_name)

        # add the player to the existing stats pages on the GUI
        for tab_name in self.game_stats_pages:
            self.roster[player_name].prepare_to_receive_data(tab_name)
            
            # redraw separators
            for separator in self.pf_separator_elements[tab_name]:
                self.pf_separator_elements[tab_name][separator].grid(row=0 , rowspan=self.display_row_number+1, column = int(separator), sticky='ns', padx=2)

        self._sort_player_order()

    def _sort_player_order(self):
        """When a new player is added to the roster, they need to be included at the right alphabetical location and all previous
        displays should be updated"""

        list_of_players = list(self.roster.keys())
        list_of_players.sort()
        player_order_number = 0
        for player in list_of_players:
            player_order_number += 1
            self.roster[player].display_row_number = player_order_number

            for game in self.game_stats_pages:
                self.roster[player].update_display_rows(game)


    def add_players_to_stats_page(self, tab_name):
        """For a new stats page, we need to add a row for each player already on the roster"""

        # add the player information to the new data tab
        for player in self.roster:
            self.roster[player].prepare_to_receive_data(tab_name)
        
        # redraw separators
        for separator in self.pf_separator_elements[tab_name]:
            self.pf_separator_elements[tab_name][separator].grid(row=0 , rowspan=self.display_row_number+1, column = int(separator), sticky='ns', padx=2)

    def add_player_to_main_DF(self, player_name):
        """When a new player is added to the roster, this method adds a new column to the DataFrames"""

        # add the new player to the list of data frame headings
        self.parent.data_frame_headings.append(player_name)

        # add a new column of zeros for the o possessions
        new_o_column = []
        for possession in self.parent.o_df["Success"]:
            new_o_column.append(0)
        
        self.parent.o_df[player_name] = new_o_column

        # add a new column of zeros for the d possessions
        new_d_column = []
        for possession in self.parent.d_df["Success"]:
            new_d_column.append(0)
        
        self.parent.d_df[player_name] = new_d_column

    def end_of_game_calcs(self):
        """Calls each player class to run their comparison calcs"""

        # work out the minimum number of possessions required to be considered noteworthy (20%)
        team_o_poss = self.team_record.data_dict[self.parent.active_game]["pitch"]["no. offence possessions"]
        self.requ_o_possessions = round(team_o_poss * self.player_v_team_ratio)
        team_d_poss = self.team_record.data_dict[self.parent.active_game]["pitch"]["no. offence possessions"]
        self.requ_d_possessions = round(team_d_poss * self.player_v_team_ratio)

        # work out the performance of the team
        self.team_record.update_team_performance()

        # prompt each player class to calcualte their end of game calculations
        for player in self.roster:
            self.roster[player].calculate_comparison_stats()
        
        # then prompt each player to calc their entanglement factors (all other player calcs must have resolved first)
        for player in self.roster:
            self.roster[player].calculate_entanglement_factor()
        
        # update awards
        self.awards_class.calcualte_awards()
