"""Any data that needs to be stored or processed at the player level is stored here"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk
import copy

class Player():
    """A class for all the data and functions that relate to a single player"""

    def __init__(self, parent, name, number, row_number, stat_list):
        """Sets up the data fields for the player"""

        # copy out required info
        self.parent = parent
        self.name = name
        self.number = number
        self.display_row_number = row_number
        self.dictionary_of_stats = copy.deepcopy(stat_list)
        self.dictionary_of_stats["name"]["Start Value"] = self.name
        self.dictionary_of_stats["number"]["Start Value"] = self.number

        self.tournament_name = self.parent.parent.tournament_name

        # set up the data structures for the class
        self._create_data_structures()

        # create a dictionary to track how often this player is on the pitch with each teammate
        self._create_teammates_dictionary()


    def _create_data_structures(self):
        """ Creates all the dictionaries that player data and gui information will be stored, as well as templates for sub-dictionaries"""

        # performance data will be stored in a series of nesting dictionaries of levels 0-3

        # Level 3 holds the stats

        # template zone stat holds one copy of each data point. This will later be copied for the "pitch" and "bench" zones
        self.template_zone_stats = {}

        for stat in self.dictionary_of_stats:
            self.template_zone_stats[stat] = self.dictionary_of_stats[stat]["Start Value"]

        # level 2 is where data will need to be sorted into two categories:
        # Data that applies when the player was on the pitch
        # Data that applies when the player was on the bench 
        # There will also be another dictionary to store the comparison between the previous two

        self.template_game_stats = {
            "pitch" : copy.deepcopy(self.template_zone_stats),
            "bench" : copy.deepcopy(self.template_zone_stats),
        }
        
        # Level 1 is a new dictionary for each game played, plus the tournament as a whole
        # Level 0 is a dictionary to hold all these game dictionaries
        self.data_dict = {}

        # create a dictionary to hold all the stats that will be averaged across the whole tournament
        self.tournament_display_dict = {}
        for stat in self.dictionary_of_stats:
            if self.dictionary_of_stats[stat]["Start Value"] == "-": 
                self.tournament_display_dict[stat] = "-"

        # create a dictionary that will store all the gui labels that will display data. This is level 0, along with data dict
        self.gui_labels_dicts = {}


    def _create_teammates_dictionary(self):
        """Adds a sub dictionary for each team mate into the dictionary of teammate comparison entries"""

        # create a dictionry to store all the comparison data with the other players
        self.teammate_records = {}

        # create a template that will include the names of all the other players
        self.teammate_list_template = {}

        # create a template for what is used for team mate. 
        self.teammate_template = {
            "number of points played" : 0,
            "no. offence possessions" : 0,
            "no. defence possessions" : 0,
            "number of possessions played" : 0,
            "turnovers conceded" : 0,
            "turnovers won" : 0,

            "offence poss without" : "-",
            "defence poss without" : "-", #!! mayber delete these two
            "with o conv" : "-",
            "without o conv" : "-",
            "with d conv" : "-",
            "without d conv" : "-",
            "offence entanglement factor" : "-",
            "defence entanglement factor" : "-",
        } # >>> partially copied from match class 

        for player in self.parent.roster:
            if player == self.name: # this is the player for this class, for which we can't compare
                pass
            else:
                # create a new entry for the team mate
                self.add_teammate_to_list(player)

    def add_teammate_to_list(self, player_name):
        """When a new player is added to the roster, this methods adds that player to the team mate list for each other player"""

        # add the player to the list for future games
        self.teammate_list_template[player_name] = copy.deepcopy(self.teammate_template)

        # retroactively add the player to the lists for established games
        for game in self.teammate_records:
            self.teammate_records[game][player_name] = copy.deepcopy(self.teammate_template)

    def prepare_to_receive_data(self, data_tab):
        """when a new stats roster tab is created this function creates sub-dictionaries to recieve data and adds the player details to the table"""

        # find out what the reference for the new data tab is (tournament name or game ref)
        self.live_game_ref = data_tab

        # create a new sub-dictionary to store input data for that game
        self.data_dict[self.live_game_ref] = copy.deepcopy(self.template_game_stats)

        if self.display_row_number < 0:
            # must be the full team stats class
            self.add_player_class_for_whole_team_to_gui()
        else:
            # add the player to the relevant stats tab
            self.add_player_to_gui_tab()
            
            # create a new sub-dictionary of teammate stats for the game
            self.teammate_records[data_tab] = copy.deepcopy(self.teammate_list_template)

    def add_player_class_for_whole_team_to_gui(self):
        """Adds team info to the team frame on the stats page"""

        # create a sub-dictionary to hold all of the gui elements that will go into the stats tab
        self.gui_labels_dicts[self.live_game_ref] = {}

        # each stat will be shown on a new row
        row_number = 0

        for stat in self.dictionary_of_stats:
            if self.dictionary_of_stats[stat]["Display Type"] in [-1, 2]:
                # increment row number
                row_number += 1

                # create a label for the stat description
                stat_text = stat.capitalize()
                self.gui_labels_dicts[self.live_game_ref][stat] = tk.Label(self.parent.team_frame[self.live_game_ref], text=stat_text, font=('Arial', 16))
                self.gui_labels_dicts[self.live_game_ref][stat].grid(row=row_number, column=0, sticky='ew')

                # create a label for the data point
                value_text = self.data_dict[self.live_game_ref]["pitch"][stat]
                self.gui_labels_dicts[self.live_game_ref][stat] = tk.Label(self.parent.team_frame[self.live_game_ref], text=value_text, font=('Arial', 16))
                self.gui_labels_dicts[self.live_game_ref][stat].grid(row=row_number, column=1, sticky='ew')
            

    def add_player_to_gui_tab(self):
        """Sets up the GUI elements that track for that player on the active stats tab"""
        
        # create a sub-dictionary to hold all of the gui elements that will go into the stats tab
        self.gui_labels_dicts[self.live_game_ref] = {}

        # for each data point that will need to be shown, create a label to hold it and add it to the grid. (both fixed and variable data)
        column_number = 0
        
        # we will need a column for the player name, number, basic stats and the marginal stats
        for stat in self.dictionary_of_stats:
            if self.dictionary_of_stats[stat]["Display Type"] > 0: # stat should be displayed

                # create a label for the data point
                text_value = self.dictionary_of_stats[stat]["Start Value"]
                self.gui_labels_dicts[self.live_game_ref][stat] = tk.Label(self.parent.player_frame[self.live_game_ref], text=text_value, font=('Arial', 16))
                self.gui_labels_dicts[self.live_game_ref][stat].grid(row=self.display_row_number, column=column_number, sticky='ew')
                
                # increment column number then check if we want a separator
                column_number += 1
                if column_number in self.parent.pf_separator_columns:
                    column_number += 1 # skip over columns with separators

    def update_display_rows(self, game_tab):
        """When a new player is added and the order of the players changes, this function changes the rows of the display elements"""

        # go through each gui element tied to this player on the target tab and reconfigure the grid row number
        for element in self.gui_labels_dicts[game_tab]:
            self.gui_labels_dicts[game_tab][element].grid_configure(row=self.display_row_number)

    def update_point_data(self, stats_input, point_line_up):
        """If a player was on the pitch for a point, this function will be called at the end to update the records for the player"""

        # check whether the player was on the pitch (or it's the team class)
        if self.name in point_line_up:
            zone = "pitch"
        else:
            zone = "bench"
        
        # store each statistic in both the game dictionaries and the tournament dictionary
        for game_data_set in (self.live_game_ref, self.tournament_name):
            for stat_from_last_point in stats_input:
                # use the dictionary of counts from the point that just ended to update each input stat in turn
                self.data_dict[game_data_set][zone][stat_from_last_point] += stats_input[stat_from_last_point]

                # add this information for the teammate subdictionary for each team mate on the pitch
                if zone == "pitch" and self.name != self.parent.team_name:
                    for teammate in point_line_up:
                        if teammate == self.name: # skip comparison with itself
                            pass
                        else:
                            self.teammate_records[game_data_set][teammate][stat_from_last_point] += stats_input[stat_from_last_point]

            # calculate the output stats (possession conversion rates) for this player in this game so far
            self.calculate_conversion_rates(game_data_set, zone)
            
            # add the newly accumluated stats and the calculated possession conversion ratios to the GUI.
            self.update_gui_for_basic_stats(game_data_set)


    def calculate_conversion_rates(self, data_set, zone):
        """takes the new count data from the most recent point and works out the players performance"""

        # calculate the offence and defence conversion rates
        try:
            o_conv = round(100 * (1 - (self.data_dict[data_set][zone]["turnovers conceded"] / self.data_dict[data_set][zone]["no. offence possessions"])))
        except ZeroDivisionError:
            o_conv = "-"
        
        try:
            d_conv = round(100 * (self.data_dict[data_set][zone]["turnovers won"] / self.data_dict[data_set][zone]["no. defence possessions"]))
        except ZeroDivisionError:
            d_conv = "-"

        # update dictionary with calculated outputs
        self.data_dict[data_set][zone]["offence conversion rate"] = o_conv 
        self.data_dict[data_set][zone]["defence conversion rate"] = d_conv
        
    def update_gui_for_basic_stats(self, data_set):
        """Updates the labels on the relevant stats tab"""
        
        # update the text on the label for each stat on the roster tab
        for stat in self.dictionary_of_stats:
            if self.dictionary_of_stats[stat]["Display Type"] == 2: # stat should be displayed
                self.gui_labels_dicts[data_set][stat].config(text=self.data_dict[data_set]["pitch"][stat])

    def calculate_comparison_stats(self):
        """Compares the on- and off- pitch performance for the player at the end of the game"""

        # data sufficiency checks, player must have done and not done at least 5 offence and defence possessions
        sufficient_data = False

        if self.data_dict[self.live_game_ref]["bench"]["no. offence possessions"] < self.parent.min_num_possessions:
            pass # player was not on the bench for at least the requred number of o possessions
        elif  self.data_dict[self.live_game_ref]["bench"]["no. defence possessions"] < self.parent.min_num_possessions:
            pass # player was not on the bench for at least the requred number of d possessions
        elif self.data_dict[self.live_game_ref]["pitch"]["no. offence possessions"] < self.parent.min_num_possessions:
            pass # player was not on the pitch for at least the requred number of o possessions
        elif self.data_dict[self.live_game_ref]["pitch"]["no. defence possessions"] > self.parent.min_num_possessions - 1:
            sufficient_data = True

        # for the game that has just ended, calculate the stats
        if sufficient_data == True:

            # calculate the o-line and d-line score for the player
            for zone in ("pitch", "bench"):
                self.calculate_performance_scores(zone)

            # do a quick sum to work out the difference between pitch and bench scores
            for stat in self.dictionary_of_stats:
                if self.dictionary_of_stats[stat]["Calc Flag"] == 2: # we need to calculate the marginal stat

                    try:
                        stat_difference = self.data_dict[self.live_game_ref]["pitch"][stat] - self.data_dict[self.live_game_ref]["bench"][stat]
                    except TypeError: # this will skip over stats with text entries
                        pass
                    else:
                        # augment the stat name
                        marginal_stat_name = "marginal " + stat

                        # store the marginal stat in the "pitch" zone of the data dict
                        self.data_dict[self.live_game_ref]["pitch"][marginal_stat_name] = stat_difference

                        # put the marginal stat on the gui
                        self.gui_labels_dicts[self.live_game_ref][marginal_stat_name].config(text=stat_difference)

                        # calculate what the average performance across all games is
                        self.average_stats_across_all_games(marginal_stat_name)

        # do the pair comparisons with teammates
        self.calculate_teammate_conversions()

    def calculate_performance_scores(self, zone):
        """Calculates the o-line and d-line scores"""
        o_score_pt1 = (100 - self.data_dict[self.live_game_ref][zone]["offence conversion rate"]) * self.data_dict[self.live_game_ref][zone]["defence conversion rate"]
        o_score_pt2 = self.data_dict[self.live_game_ref][zone]["offence conversion rate"] * 100 / ( 10000 - o_score_pt1)
        self.data_dict[self.live_game_ref][zone]["o-line score"] = round(o_score_pt2 * 100)

        d_score_pt1 = self.data_dict[self.live_game_ref][zone]["defence conversion rate"] * o_score_pt2
        self.data_dict[self.live_game_ref][zone]["d-line score"] = round(d_score_pt1)

        self.data_dict[self.live_game_ref][zone]["total score"] = round((d_score_pt1 + o_score_pt2 * 100) / 2)

    def average_stats_across_all_games(self, marginal_stat):
        """Averages a stat across all games so it can be put on the tournament-level display"""
    
        # set a blank variable to be updated with the performance in each game
        stat_aggregate = 0
        number_of_games = 0

        for game in self.data_dict:
            if game == self.tournament_name: # skip this as it is not a real game
                pass
            else:
                try:
                    stat_aggregate += self.data_dict[game]["pitch"][marginal_stat] 
                except TypeError:
                    pass # there must be insufficient data from a previous game.
                else:
                    number_of_games+=1
        
        if number_of_games > 0:
            # average the result across all games
            averaged_result = round(stat_aggregate / number_of_games)

            # store it in the dictionary (used for awards)
            self.data_dict[self.tournament_name]["pitch"][marginal_stat] = averaged_result

            # add that result to the gui for the full tournament
            self.gui_labels_dicts[self.tournament_name][marginal_stat].config(text=averaged_result)

    def update_team_performance(self):
        """The o scores and d scores for the whole team are not marginal, so must be calculated slightly differently"""

        # Use the offence and defence conversion rates to calculate an overall score for the team performance
        self.calculate_performance_scores("pitch")

        # process the new data
        for stat in self.dictionary_of_stats:
            if self.dictionary_of_stats[stat]["Calc Flag"] == 2: # we need to calculate the marginal stat

                # update the gui with the performance score for the most recent game
                self.gui_labels_dicts[self.live_game_ref][stat].config(text = self.data_dict[self.live_game_ref]["pitch"][stat])

                # work out the average across all games
                self.average_stats_across_all_games(stat)

    def calculate_teammate_conversions(self):
        """At the end of the game, this method is called to calculate the offensive and deffensive conversion rates 
        for the player in combination with each other player. This is then made marginal versus everyone else"""
        
        for teammate in self.parent.roster:
            if teammate == self.name or self.name == self.parent.team_name:
                pass
            else:
                # work out how many o possesions this player had with and without their teammate
                op_with = self.teammate_records[self.live_game_ref][teammate]["no. offence possessions"]
                op_without = self.data_dict[self.live_game_ref]["pitch"]["no. offence possessions"] - op_with
                self.teammate_records[self.live_game_ref][teammate]["offence poss without"] = op_without

                # check for sufficient offensive possessions
                if op_with >= self.parent.min_num_crossovers and op_without >= self.parent.min_num_crossovers:
                    # calcualte key inputs
                    tc_with = self.teammate_records[self.live_game_ref][teammate]["turnovers conceded"]
                    tc_without = self.data_dict[self.live_game_ref]["pitch"]["turnovers conceded"] - tc_with

                    # calculate and record conversion rate
                    self.teammate_records[self.live_game_ref][teammate]["with o conv"] = round(100 * (1 - (tc_with / op_with)))
                    self.teammate_records[self.live_game_ref][teammate]["without o conv"] = round(100 * (1 - (tc_without / op_without)))

                # work out how many o possesions this player had with and without their teammate
                dp_with = self.teammate_records[self.live_game_ref][teammate]["no. defence possessions"]
                dp_without = self.data_dict[self.live_game_ref]["pitch"]["no. defence possessions"] - dp_with
                self.teammate_records[self.live_game_ref][teammate]["defence poss without"] = dp_without
                
                # check for sufficient offensive possessions
                if dp_with >= self.parent.min_num_crossovers and dp_without >= self.parent.min_num_crossovers:
                    # calcualte key inputs
                    tw_with = self.teammate_records[self.live_game_ref][teammate]["turnovers won"]
                    tw_without = self.data_dict[self.live_game_ref]["pitch"]["turnovers won"] - tw_with

                    # calculate and record conversion rate
                    self.teammate_records[self.live_game_ref][teammate]["with d conv"] = round(100 * (1 - (tw_with / dp_with)))
                    self.teammate_records[self.live_game_ref][teammate]["without d conv"] = round(100 * (1 - (tw_without / dp_without)))

    def calculate_entanglement_factor(self):                
        """Calculate the entanglement factor with each player for o and d"""

        for teammate in self.parent.roster:
            if teammate == self.name:
                pass
            else:
                for poss_type in ("offence", "defence"):
                    stat = poss_type + " poss without"
                    stat2 = "no. " + poss_type + " possessions"
                    stat3 = poss_type + " entanglement factor"
                    
                    # fetch the number of possessions without the team mate
                    poss_without = self.teammate_records[self.live_game_ref][teammate][stat]

                    # fetch how the other player views this player
                    other_poss_without = self.parent.roster[teammate].teammate_records[self.live_game_ref][self.name][stat]

                    # fetch the total number of possessions played by the team 
                    team_poss = self.parent.team_record.data_dict[self.live_game_ref]["pitch"][stat2]

                    # calculate the entanglement factor
                    ef = 1 - ((poss_without + other_poss_without) / team_poss) * 2
                    self.teammate_records[self.live_game_ref][teammate][stat3] = round(ef, 2)
                    #!! print(f"{self.live_game_ref} {self.name} and {teammate} {poss_type} ef = {ef}")
        