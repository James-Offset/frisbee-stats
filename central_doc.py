"""This is the base document that will call all of the other functions and classes"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import json

"""My Code"""
from data_extractor import DataExtractor
from frisbee_match import FrisbeeGame
from team_roster import Team
from live_game import LiveGame
from game_data_window import NewGameWindow
from machine_learning import MachineLearning


class MainGUI():
    """This class is the home page for the app and calls all the subclasses and functions.
    The core initial function is to collect tournament metadata"""

    def __init__(self):
        """Set up the GUI and allow the user to call subsequent functions"""

        # create GUI window
        self.root = tk.Tk()

        # set root settings
        self.gui_width = 850
        self.gui_height = 700
        geometry_set = str(self.gui_width) + "x" + str(self.gui_height)
        self.root.geometry(geometry_set)
        self.root.title("Ultimate Statistics User Interface")

        # build notebook to store all the info tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # build the home page tab
        self._build_homepage()
        
        # create a blank dictionary to store our game classes
        self.games = {}
        self.number_of_games = 0 
                
        # run the app
        self.root.mainloop()
        print("check") #!! this just sets a stop so I can review the code

    def _build_homepage(self):
        """Creates all the widgets and layouts for the homepage"""

        # create the page and add it to the notebook
        self.home_page = tk.Frame(self.notebook)
        self.home_page.pack()
        self.notebook.add(self.home_page, text="Home Page")

        # add a heading at the top
        self.heading = tk.Label(self.home_page, text="Frisbee Stats Homepage", font=('Arial', 18))
        self.heading.pack(padx=20, pady= 20)

        # add a label prompting the user for where to start
        self.start_label = tk.Label(self.home_page, text="Click below to start")
        self.start_label.pack(pady=2)

        # add a button to start the program
        self.program_start_button = ttk.Button(self.home_page, text="Start Program", command=self.user_starts_tournament)
        self.program_start_button.pack(padx=10,pady=10)

        # add a status label
        self.status_label_text = tk.StringVar()
        self.status_label_text.set("Alternatively, click below to import a dataset:")
        self.import_status_label = tk.Label(self.home_page, textvariable=self.status_label_text)
        self.import_status_label.pack(pady=5)

        # add a load tournament info button
        self.load_data_button = ttk.Button(self.home_page, text="Load Tournament Data", command=self.load_data)
        self.load_data_button.pack(padx=20, pady=5)

        # add a save tournament info button
        self.save_data_button = ttk.Button(self.home_page, text="Save Tournament Data", command=self.save_data)
        self.save_data_button.pack(padx=20, pady=5)
        
        # add a status label
        self.player_entry_status_label = tk.Label(self.home_page, text="Click the button below to start a new game")
        self.player_entry_status_label.pack(pady=20)

        # add new game button
        self.new_game_button = ttk.Button(self.home_page, text="Start New Game", command=self.manual_game_start)
        self.new_game_button.pack(padx=20, pady=10)

        # add a button to run the analysis
        self.ml_button = ttk.Button(self.home_page, text="Do Machine Learning!", command=self.run_machine_learning_analysis, state=["disabled"])
        self.ml_button.pack(padx=20, pady=20)

        # disable buttons not immediately useful
        self.new_game_button.state(["disabled"])
        
    def user_starts_program(self):
        """This method is called when the user first pushes the start program button"""

        """!! This method is currently unused in favor of the start tournament method. To be resotred if I implement scrimmage functionality"""
        
        # create a new class to handle the data entry window
        window = NewGameWindow(self.root, "new program")

        # collect the returned info
        data_provision_success, provided_info = window.return_info()

        if data_provision_success == True:
            # if we successfully get the data, copy it out, if not then nothing happens
            self.program_type = provided_info[0]
            self.environment = provided_info[1]
            self.number_of_players_at_once = int(provided_info[2]) 

            # reconfigure for the next data entry
            if self.program_type == "Tournament":
                self.program_start_button.config(command=self.manual_metadata_receive)
                self.program_start_button.config(text="Enter Info")
                self.start_label.config(text="Click the button below to enter tournament infomation")

    def user_starts_tournament(self):
        """This method is called when the user first pushes the start program button"""

        """!! This method is currently unused in favor of the start tournament method. To be resotred if I implement scrimmage functionality"""
        
        # create a new class to handle the data entry window
        window = NewGameWindow(self.root, "tournament (temporary)")

        # collect the returned info
        data_provision_success, provided_info = window.return_info()

        if data_provision_success == True:
            # if we successfully get the data, copy it out
            self.tournament_name = provided_info[0]
            self.team_name = provided_info[1]
            self.environment = provided_info[2]
            self.number_of_players_at_once = int(provided_info[3]) 

            # continue with the set up
            self.complete_set_up()

        # if not then nothing happens

    def manual_metadata_receive(self):
        """This is the method that will trigger when the metadata button is pushed"""

        # create a new class to handle the data entry window
        window = NewGameWindow(self.root, "new tournament")

        # collect the returned info
        data_provision_success, provided_info = window.return_info()

        if data_provision_success == True:
            # if we successfully get the data, copy it out
            self.tournament_name = provided_info[0]
            self.team_name = provided_info[1]

            # continue with the set up
            self.complete_set_up()

        # if not then nothing happens

    
    def complete_set_up(self):
        """Once the metadata for the tournament is in, run this code to allow for the full app to run"""

        # Create supporting classes
        self.team = Team(self)

        # change the status of buttons
        self.program_start_button.state(["disabled"])
        self.status_label_text.set("Manual Data Provided")
        
        # set up storage for tournament data for machine learning
        self.mldf = {}
        for poss_type in ("offence", "defence"):
            self.mldf[poss_type] = pd.DataFrame({
                "Success" : [],
            })

        # add an empty headings list
        self.data_frame_headings = []

        # add a flag for the exisitance of a machine learning class
        self.ml_flag = False

    def extract_stock_data(self, filename, file_type):
        """Looks at the provided excel file and creates dictionaries of all player and game data"""

        # import all the data
        if file_type == "json":
            self.tournament_metadata = self.loaded_data["metadata"]
            self.imported_roster = self.loaded_data["players"]
            self.raw_game_data = self.loaded_data["game_data"] 
        else:
            extraction_tool = DataExtractor()
            self.tournament_metadata, self.imported_roster, self.raw_game_data = extraction_tool.import_stock_data(filename)

        # copy out the metadata
        self.tournament_name = self.tournament_metadata["Tournament Name"]
        self.team_name = self.tournament_metadata["Team Name"]
        self.number_of_players_at_once = self.tournament_metadata["Players per Point"]
        self.environment = self.tournament_metadata["Environment"]

        # now we have the metadata, we can complete the set up
        self.complete_set_up()

        # create player classes
        for player in self.imported_roster:
            self.team.roster_tab.add_player_to_records(player, self.imported_roster[player]['Player Number'])

        # create game classes
        self._create_game_classes_from_import()

        # change flags and markers
        self.status_label_text.set('Data imported')
        self.load_data_button.state(["disabled"])
                    
    def _create_game_classes_from_import(self):
        """Creates a class for each game played and runs the relevant functions"""

        # create a loop for each game
        for game in self.raw_game_data:

            # call the new game method
            self.start_new_game(self.raw_game_data[game]["Opponent"], self.raw_game_data[game]["Starting on Defence"])

            # find the set of raw data that applies to that game
            for name_of_considered_game in self.raw_game_data:
                if self.active_game in name_of_considered_game:
                    break
            
            # call the method from the game class to process the imported data
            self.games[self.active_game].crunch_data_from_import(self.raw_game_data[name_of_considered_game]['Turns per Point'], self.raw_game_data[name_of_considered_game]["Active Players"])
            
            # once all data has been processed, we end the live game
            self.live_game.end_game()

    def manual_game_start(self):
        """Creates the class for a new game when button pressed by user"""

        # create a new class to handle the data entry window
        window = NewGameWindow(self.root, "new game")

        # collect the returned info
        data_provision_success, provided_info = window.return_info()

        if data_provision_success == True:
            # if we successfully get the data, then start the new game
            self.start_new_game(provided_info[0], provided_info[1])

            # if not then nothing happens

    def start_new_game(self, opp_name, team_on_defence):
        """Sets up all the classes and methods needed for a new game"""
        
        # disable the new game button
        self.new_game_button.state(["disabled"])

        # increment game number
        self.number_of_games += 1

        # Assign a name to the game
        game_class_ref = "Game " + str(self.number_of_games)

        # add the new opposition team to the main DF (same as for a player)
        self.team.add_player_to_main_DF(opp_name)

        # if the game is played outdoors, add a factor for the wind as well
        if self.environment == "Outdoors":
            wind_name = game_class_ref + " Wind"
            self.team.add_player_to_main_DF(wind_name)
        else:
            wind_name = None

        # create a new class with the assembled input data
        self.games[game_class_ref] = FrisbeeGame(self, self.number_of_games, opp_name, team_on_defence, wind_name)

        # make a note of what the active game is called
        self.active_game = game_class_ref

        # create a game team stats tab
        self.team.build_game_stats_page(game_class_ref)

        # add the players to the new stats page
        self.team.add_players_to_stats_page(game_class_ref)

        # create a live game tab
        self.live_game = LiveGame(self, opp_name, self.number_of_games, team_on_defence)

    def run_machine_learning_analysis(self):
        """This method calls the machine learning class"""

        # collect a list of opponents
        opponents = []
        for game in self.games:
            opponents.append(self.games[game].opp_name)

        if self.ml_flag ==False:
            # create the class for machine learning
            self.ml_class = MachineLearning()

            self.ml_flag = True
            
        else:
            self.ml_class.destroy_notebook_tab()
        
        # call the class to carry out the machine learning #!!neaten this all later
        self.ml_class.carry_out_machine_learning(self, self.mldf, self.environment, self.team.roster_tab.player_dictionary, opponents)
        
        # disable the button
        self.ml_button.state(['disabled'])

    def save_data(self):
        """Saves all the data acquired so far into a json file"""

        # establish file name
        half_filename = filedialog.asksaveasfilename()
        #filename = "stored_data/" + self.tournament_name + ".json" !!
        print(half_filename)

        # add the .json file type to the filename
        filename = half_filename + ".json"

        # check the user actually selected a file
        try: 
            # collect tournament metadata
            self.tournament_metadata = {
                "Team Name" : self.team_name,
                "Tournament Name" : self.tournament_name,
                "Players per Point" : self.number_of_players_at_once,
                "Number of Games" : self.number_of_games,
                "Environment" : self.environment,
            }

            # establish a list of players
            player_dict = {}
            for player in self.team.roster:
                player_dict[player] = {
                    "Player Number" : self.team.roster[player].number
                }
            
            # wrap up game info
            games_dict = {}
            for game in self.games:
                games_dict[game] = {
                    "Opponent" : self.games[game].opp_name,
                    "Starting on Defence" : self.games[game].defence_start,
                    "Turns per Point" : self.games[game].list_of_numbers_of_turns,
                    "Active Players" : [],
                }

                # add point line ups
                for point in self.games[game].point_lineups:
                    games_dict[game]["Active Players"].append(self.games[game].point_lineups[point])

            # wrap everything into a single dictionary
            dict_to_save = {
                "file tag" : "frisbee is awesome",
                "metadata" : self.tournament_metadata,
                "players" : player_dict,
                "game_data" : games_dict,
            }

            # save the information
            with open(filename, 'w') as f:
                json.dump(dict_to_save, f, indent=4)
        
        except Exception:
            pass

    def load_data(self):
        """Loads a saved json file for a tournament"""

        #choose file to load
        # filename = "stored_data/Glasto 2019.json"
        filename = filedialog.askopenfilename()

        # check the user actually selected a file
        try:
            print(filename)
            if filename[-4:] == "xlsx":
                file_type = "Excel"
            elif filename[-4:] == "json":
                file_type = "json" #!! put in some kind of notification for an invalid file choice

                # load data into a python dictionary
                with open(filename) as f:
                    self.loaded_data = json.load(f)    

        except Exception:
            pass
        else:
            # call the data extraction function
            self.extract_stock_data(filename, file_type)  

# call the main code
if __name__ == "__main__":
    print("Program starting...")
    tournament_gui = MainGUI()

    print("Check results")