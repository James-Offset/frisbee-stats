"""Any data that needs to be stored or processed at the player level is stored here

Not sure if this is necessary at this point, but we can set up a class if needed. 
"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk
import copy

class Player():
    """A class for all the data and functions that relate to a single player"""

    def __init__(self, parent, name, number, row_number):
        """Sets up the data fields for the player"""

        self.parent = parent
        self.name = name
        self.number = number
        self.display_row_number = row_number

        self.tournament_name = self.parent.parent.tournament_name

        # set up the data structures for the class
        self._create_data_structures()


    def _create_data_structures(self):
        """ Creates all the dictionaries that player data and gui information will be stored, as well as templates for sub-dictionaries"""

        # performance data will be stored in a series of nesting dictionaries of levels 0-4

        # Level 4 holds the stats
        # Level 3 combines these into one dictionary
        self.template_zone_stats = {
            "name" : self.name,
            "number" : self.number,
            
            "number of points played" : 0,
            "no. offence possessions" : 0,
            "no. defence possessions" : 0,
        
            "number of possessions played" : 0,
            "turnovers conceded" : 0,
            "turnovers won" : 0,
        
            "offence conversion rate" : "-",
            "defence conversion rate" : "-",
            "o-line score" : "-",
            "d-line score" : "-",
            "total score" : "-",
        }
        
        # level 2 is where data will need to be sorted into two categories:
        # Data that applies when the player was on the pitch
        # Data that applies when the player was on the bench 
        # There will also be another dictionary to store the comparison between the previous two

        self.template_game_stats = {
            "pitch" : copy.deepcopy(self.template_zone_stats),
            "bench" : copy.deepcopy(self.template_zone_stats),
            "comparison" : copy.deepcopy(self.template_zone_stats),
        }
        
        # Level 1 is a new dictionary for each game played, plus the tournament as a whole
        # Level 0 is a dictionary to hold all these game dictionaries
        self.data_dict = {}

        # create a dictionary that will store all the gui labels that will display data. This is level 0, along with data dict
        self.gui_labels_dicts = {}

        # create a list of data that will be displayed in the gui. Subset of all stats
        self.display_list = [
            "name",
            "number",
            
            "number of points played" ,
            "no. offence possessions" ,
            "no. defence possessions" ,
        
            "offence conversion rate" ,
            "defence conversion rate" ,
        ]

        self.extra_team_display = [
            "o-line score",
            "d-line score",
            "total score",
        ]

        # marginal stats are calculated between zones, so sit in a separate dictionary
        self.marginal_stats = {}
        
        self.template_marginal_stats = {
            "marginal offence conversion" : "-",
            "marginal defence conversion" : "-",
            "marginal o-line score" : "-",
            "marginal d-line score" : "-",
            "marginal total score" : "-",
        }

        # these also need to be displayed
        self.display_addendum = []
        for stat in self.template_marginal_stats:
            self.display_addendum.append(stat)


    def prepare_to_receive_data(self, data_tab):
        """when a new stats roster tab is created this function creates sub-dictionaries to recieve data and adds the player details to the table"""

        #!! consider re-drawing entire grid in alphabetical order

        # find out what the reference for the new data tab is (tournament name or game ref)
        self.live_game_ref = data_tab

        # create a new sub-dictionary to store input data for that game
        self.data_dict[self.live_game_ref] = copy.deepcopy(self.template_game_stats)
        self.marginal_stats[self.live_game_ref] = copy.deepcopy(self.template_marginal_stats)

        if self.display_row_number < 0:
            # must be the full team stats class
            self.add_player_class_for_whole_team_to_gui()
        else:
            # add the player to the relevant stats tab
            self.add_player_to_gui_tab()

    def add_player_class_for_whole_team_to_gui(self):
        """Adds team info to the team frame on the stats page"""

        # create a sub-dictionary to hold all of the gui elements that will go into the stats tab !! duplicated, so can be moved to __init__
        self.gui_labels_dicts[self.live_game_ref] = {}

        # each stat will be shown on a new row
        row_number = 0

        for stat in self.display_list + self.extra_team_display:

            if stat == "name" or stat == "number":
                pass # we don't want to display this info
            else:
                # increment row number
                row_number += 1

                # create a label for the stat description
                stat_text = stat #!! capitalise later
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
        
        for stat in self.display_list + self.display_addendum:
            # create a label for the data point
            self.gui_labels_dicts[self.live_game_ref][stat] = tk.Label(self.parent.player_frame[self.live_game_ref], text="-", font=('Arial', 16))
            self.gui_labels_dicts[self.live_game_ref][stat].grid(row=self.display_row_number, column=column_number, sticky='ew')
            
            # increment column number then check if we want a separator
            column_number += 1
            if column_number in self.parent.pf_separator_columns:
                column_number += 1
        
        # make sure the name and number are showing
        for stat in ("name" , "number"):
            self.gui_labels_dicts[self.live_game_ref][stat].config(text=self.template_zone_stats[stat])


    def update_point_data(self, stats_input, name_check):
        """If a player was on the pitch for a point, this function will be called at the end to update the records for the player"""

        # check whether the player was on the pitch (or it's the team class)
        if name_check == self.name:
            zone = "pitch"
        else:
            zone = "bench"
            #!! don't actually need to process bench data until the end
        
        # store each statistic in both the game dictionaries and the tournament dictionaries
        for data_set in (self.live_game_ref, self.tournament_name):
            for game_event in stats_input:
                # update each input stat in turn
                self.data_dict[data_set][zone][game_event] += stats_input[game_event]

            # calculate new output stats for that data set
            self.process_stats(data_set, zone)
            
            #!! will want to calc display stats for the full team at some point
            if self.display_row_number < 0:
                    # update the text on the label for each stat on the roster tab
                    for stat in self.display_list:
                        if stat == "name" or stat == "number":
                            pass # we don't want to display this info
                        else:
                            self.gui_labels_dicts[data_set][stat].config(text=self.data_dict[data_set]["pitch"][stat])

                    for stat in self.extra_team_display:
                        self.gui_labels_dicts[data_set][stat].config(text=self.data_dict[data_set]["pitch"][stat])
            else:

                # display those outputs
                self.update_gui_display(data_set)


    def process_stats(self, data_set, zone):
        """takes the new count data from the most recent point and works out the players performance"""

        # run calcualtions for each stat
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
        
    def update_gui_display(self, data_set):
        """Updates the labels on the relevant stats tab"""
        
        # update the text on the label for each stat on the roster tab
        for stat in self.display_list:
            self.gui_labels_dicts[data_set][stat].config(text=self.data_dict[data_set]["pitch"][stat])

        for stat in self.marginal_stats[self.live_game_ref]:
            self.gui_labels_dicts[data_set][stat].config(text=self.marginal_stats[data_set][stat])


    def calculate_comparison_stats(self):
        """Compares the on- and off- pitch performance for the player"""

        # data sufficiency checks, player must have done and not done at least 5 offence and defence possessions
        sufficient_data = False

        if self.data_dict[self.live_game_ref]["bench"]["no. offence possessions"] < self.parent.requ_o_possessions:
            pass
        elif  self.data_dict[self.live_game_ref]["bench"]["no. defence possessions"] < self.parent.requ_d_possessions:
            pass
        elif self.data_dict[self.live_game_ref]["pitch"]["no. offence possessions"] < self.parent.requ_o_possessions:
            pass
        elif self.data_dict[self.live_game_ref]["pitch"]["no. defence possessions"] > self.parent.requ_d_possessions - 1:
            sufficient_data = True

        # for the game that has just ended, calculate the stats
        if sufficient_data == True:

            # calculate performance scores
            self._calculate_performance_scores()

            # do a quick sum to work out the difference between pitch and bench scores
            for stat in self.data_dict[self.live_game_ref]["comparison"]:
                try:
                    self.data_dict[self.live_game_ref]["comparison"][stat] = self.data_dict[self.live_game_ref]["pitch"][stat] - self.data_dict[self.live_game_ref]["bench"][stat]
                except TypeError: # this will skip over stats with text entries
                    pass

            #!! copy comparison scores over to the marginal dictionary
            self._calculate_marginal_scores()

            # prompt the gui to update the display
            self.update_gui_display(self.live_game_ref)

            # calculate new weighted stats for the whole tournament
            self._calculate_tournament_marginal_stats()

    def _calculate_performance_scores(self):
        """Calculates the o-line and d-line scores"""
        for zone in ("pitch", "bench"):
            o_score_pt1 = (100 - self.data_dict[self.live_game_ref][zone]["offence conversion rate"]) * self.data_dict[self.live_game_ref][zone]["defence conversion rate"]
            o_score_pt2 = self.data_dict[self.live_game_ref][zone]["offence conversion rate"] * 100 / ( 10000 - o_score_pt1)
            self.data_dict[self.live_game_ref][zone]["o-line score"] = round(o_score_pt2 * 100)

            d_score_pt1 = self.data_dict[self.live_game_ref][zone]["defence conversion rate"] * o_score_pt2
            self.data_dict[self.live_game_ref][zone]["d-line score"] = round(d_score_pt1)

            self.data_dict[self.live_game_ref][zone]["total score"] = round((d_score_pt1 + o_score_pt2 * 100) / 2)

    def _calculate_marginal_scores(self):
        """Calculates the more complex marginal scores"""

        # add the marginal turnover rate values to the display dictionary
        marginal_oc = self.data_dict[self.live_game_ref]["comparison"]["offence conversion rate"]
        marginal_dc = self.data_dict[self.live_game_ref]["comparison"]["defence conversion rate"]

        self.marginal_stats[self.live_game_ref]["marginal offence conversion"] = marginal_oc
        self.marginal_stats[self.live_game_ref]["marginal defence conversion"] = marginal_dc

        #!! calculate other performance scores
        o_score = marginal_oc * 100 / ( 10000 - ( (100 - marginal_oc) * marginal_dc))
        d_score = o_score * self.marginal_stats[self.live_game_ref]["marginal defence conversion"] / 100
        total_score = (o_score + d_score) / 2

        self.marginal_stats[self.live_game_ref]["marginal o-line score"] = self.data_dict[self.live_game_ref]["comparison"]["o-line score"]
        self.marginal_stats[self.live_game_ref]["marginal d-line score"] = self.data_dict[self.live_game_ref]["comparison"]["d-line score"]
        self.marginal_stats[self.live_game_ref]["marginal total score"] = self.data_dict[self.live_game_ref]["comparison"]["total score"]

    def _calculate_tournament_marginal_stats(self):
        """Tournament marginal stats must be weighted for each game so are calculated differently. Only pitch matters for this"""

        for stat in self.template_marginal_stats:

            # set a blank variable to be updated with the performance in each game
            stat_aggregate = 0
            number_of_games = 0

            for game in self.data_dict:
                if game == self.tournament_name: # skip this as it is not a real game
                    pass
                else:
                    try:
                        stat_aggregate += self.marginal_stats[game][stat] 
                    except TypeError:
                        pass # there must be insufficient data from a previous game.
                    else:
                        number_of_games+=1

            
            # average the result across all games
            averaged_result = round(stat_aggregate / number_of_games)

            # add that result to the output dictionary
            self.marginal_stats[self.tournament_name][stat] = averaged_result

        # prompt the gui to update the display
        self.update_gui_display(self.tournament_name)


