"""This is the base document that will call all of the other functions and classes"""



"""Third Party Code"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV
import json

"""My Code"""
from data_extractor import DataExtractor
from frisbee_match import FrisbeeGame
from team_roster import Team
from live_game import LiveGame
from game_data_window import NewGameWindow


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

        # set up a few markers
        self.data_extracted = False
        self.game_import = False
        self.metadata_flag = 0
        self.load_from_json = False #!! move this later when adding import selection

        #!! Set up some temporary opp names
        self.opp_name_count = 0

                
        # run the app
        self.root.mainloop()
        print("check") #!! this just sets a stop so I can review the code

    def _build_homepage(self):
        """Creates all the widgets and layouts for the homepage"""

        # create the page and add it to the notebook
        self.home_page = tk.Frame(self.notebook)
        self.home_page.pack()
        self.notebook.add(self.home_page, text="Home Page")

        # add a label at the top
        self.label = tk.Label(self.home_page, text="Frisbee Stats Homepage", font=('Arial', 18))
        self.label.pack(padx=20, pady= 20)

        # add a textbox for manual metadata info !! change this to an entry widget later
        self.metadata_label = tk.Label(self.home_page, text="Enter your team name to start")
        self.metadata_label.pack(pady=2)
        self.metadata_box = tk.Text(self.home_page, height=1, width=15, font=('Arial', 16))
        self.metadata_box.pack(pady=2)
        self.metadata_box.bind("<Return>", self.submit_metagame_info)
        self.metadata_button = ttk.Button(self.home_page, text="Submit Info", command=self.manual_metadata_receive)
        self.metadata_button.pack(padx=10,pady=10)

        # add a button to import the data we already have
        self.import_data_button = ttk.Button(self.home_page, text="Import Data", command=self.extract_stock_data)
        self.import_data_button.pack(padx=10,pady=10)

        # add a status label
        self.import_status_label = tk.Label(self.home_page, text="Please click for roster import")
        self.import_status_label.pack(pady=5)

        # add label asking for new player name
        self.player_name_label = tk.Label(self.home_page, text="Enter the name for a new player below")
        self.player_name_label.pack(pady=2)

        # add new player text entry box !! change this to an entry widget later
        self.player_name_box = tk.Text(self.home_page, height=1, width=10, font=('Arial', 16))
        self.player_name_box.pack(pady=2)
        self.player_name_box.bind("<Return>", self.disable_newline)

        # add label asking for new player name
        self.player_number_label = tk.Label(self.home_page, text="Enter the number for a new player below")
        self.player_number_label.pack(pady=2)

        self.player_number_box = tk.Text(self.home_page, height=1, width=5, font=('Arial', 16))
        self.player_number_box.pack(pady=2)
        self.player_number_box.bind("<Return>", self.submit_player_number)

        # add new player entry button
        self.new_player_button = ttk.Button(self.home_page, text="Enter Player", command=self.manual_player_input)
        self.new_player_button.pack(padx=20, pady=5)

        # add a status label
        self.player_entry_status_label = tk.Label(self.home_page, text="Click the button above to enter new player info")
        self.player_entry_status_label.pack(pady=2)

        # add new game button
        self.new_game_button = ttk.Button(self.home_page, text="Start New Game", command=self.manual_game_start)
        self.new_game_button.pack(padx=20, pady=20)

        # add a button to run the analysis
        self.ml_button = ttk.Button(self.home_page, text="Do Machine Learning!", command=self.run_machine_learning_analysis)
        self.ml_button.pack(padx=20, pady=20)

        # add a save tournament info and load tournament info buttons
        self.save_data_button = ttk.Button(self.home_page, text="Save Tournament Data", command=self.save_data)
        self.save_data_button.pack(padx=20, pady=5)

        self.load_data_button = ttk.Button(self.home_page, text="Load Tournament Data", command=self.load_data)
        self.load_data_button.pack(padx=20, pady=5)

        # disable buttons not immediately useful
        self.new_game_button.state(["disabled"])
        self.new_player_button.state(["disabled"])
        
    
    def manual_metadata_receive(self):
        """This is the method that will trigger when the metadata button is pushed"""

        # set a default error message
        self.metadata_message = "Unknown Error"

        # get the text that the user has entered
        box_entry = self.metadata_box.get('1.0', tk.END)

        try:
            if self.metadata_flag == 0: # no metadata yet
                team_name = box_entry[:-1]
                if len(team_name) < 20 and len(team_name) > 1: # check the team name is a suitable length
                    self.team_name = team_name
                    self.metadata_flag = 1
                    self.metadata_message = "Please enter the tournament name" # ask for next info
                    self.metadata_box.delete('1.0', tk.END) # empty the box
                else:
                    self.metadata_message = "Team name length must be no more than 20 characters"
            elif self.metadata_flag == 1: # now want tournament name
                tournament_name = box_entry[:-1]
                if len(tournament_name) < 20 and len(tournament_name) > 1:
                    self.tournament_name = tournament_name
                    self.metadata_flag = 2
                    self.metadata_message = "Please enter the number of teammates playing per point (5 or 7)"
                    self.metadata_box.delete('1.0', tk.END)
                else:
                    self.metadata_message = "Tournament name length must be no more than 20 characters"
            elif self.metadata_flag == 2:
                self.metadata_message = "Please enter 5 or 7 only"
                try:
                    number_of_players = int(box_entry)
                except ValueError:
                    pass
                else:
                    if number_of_players == 5 or number_of_players == 7:
                        self.number_of_players_at_once = number_of_players
                        self.metadata_flag = 3
                        self.metadata_message = "Metagame info entry complete"
                        self.metadata_box.delete('1.0', tk.END)
                        self.complete_set_up()
        except Exception:
            self.metadata_message = "Unknown error, please try again"

        # each time we call this method, we need to update the message for the user
        self.metadata_label.config(text=self.metadata_message)
    
    def complete_set_up(self):
        """Once the metadata for the tournament is in, run this code to allow for the full app to run"""

        # Create supporting classes
        self.team = Team(self)

        # change the status of buttons
        self.metadata_button.state(["disabled"])
        self.new_player_button.state(["!disabled"])
        
        # set up storage for tournament data for machine learning
        self.o_df = pd.DataFrame({
            "Success" : [],
        })

        self.d_df = pd.DataFrame({
            "Success" : [],
        })

        self.data_frame_headings = []

    def extract_stock_data(self):
        """Looks at the provided excel file and creates dictionaries of all player and game data"""

        # check if we have extracted the data already
        if self.data_extracted == False:

            # import all the data
            if self.load_from_json == True:
                self.tournament_metadata = self.loaded_data["metadata"]
                self.imported_roster = self.loaded_data["players"]
                self.raw_game_data = self.loaded_data["game_data"] 
            else:
                extraction_tool = DataExtractor()
                self.tournament_metadata, self.imported_roster, self.raw_game_data = extraction_tool.import_stock_data()

            # set the flag to True
            self.data_extracted = True

            # copy out the metadata
            self.tournament_name = self.tournament_metadata["Tournament Name"]
            self.team_name = self.tournament_metadata["Team Name"]
            self.number_of_players_at_once = self.tournament_metadata["Players per Point"]

            # now we have the metadata, we can complete the set up
            self.complete_set_up()

            # change button text once data is extracted !! move this later
            self.resultsContents = tk.StringVar()
            self.import_status_label['textvariable'] = self.resultsContents
            self.resultsContents.set('Import Game Data')

            # create player classes
            for player in self.imported_roster:
                self.team.new_player_entry(player, self.imported_roster[player]['Player Number'])

        elif self.game_import == False: #!! change this all to one step (from two) later
            # create game classes
            self._create_game_classes_from_import()

            # change flags and markers
            self.game_import = True
            self.resultsContents.set('Data extracted')
            self.import_data_button.state(["disabled"])
                    
    def _create_game_classes_from_import(self):
        """Creates a class for each game played and runs the relevant functions"""

        # create a loop for each game
        for game_number in range(self.tournament_metadata['Number of Games']):

            # establish the game tag
            game_tag = "Game " + str(game_number)

            # call the new game method
            self.start_new_game(self.raw_game_data[game_tag]["Opponent"], self.raw_game_data[game_tag]["Starting on Defence"])

            # find the set of raw data that applies to that game
            for name_of_considered_game in self.raw_game_data:
                if self.active_game in name_of_considered_game:
                    break
            
            # call the method from the game class to process the imported data
            self.games[self.active_game].crunch_data_from_import(self.raw_game_data[name_of_considered_game]['Turns per Point'], self.raw_game_data[name_of_considered_game]["Active Players"])
            
            # once all data has been processed, we end the live game
            self.live_game.end_game()
      
    def manual_player_input(self):
        """Takes the user entry in the text boxes and checks it. If ok, adds a new player"""

        # copy out the user entries
        name_entry = self.player_name_box.get('1.0', tk.END)
        number_entry = self.player_number_box.get('1.0', tk.END)

        # pass to function in team class
        return_message = self.team.check_manual_player_entry(name_entry, number_entry)

        # show the message communicating whether the data entry was successful or not
        self.player_entry_status_label.config(text=return_message)

    def disable_newline(self, event):
        """If someone tries to hit enter while typing in an entry this will prevent the box from adding a new line"""
        return "break"
    
    def submit_player_number(self, event):
        """If the user hits enter after their player number, it is submitted"""
        self.manual_player_input()
        return "break"
    
    def submit_metagame_info(self, event):
        """If the user hits enter after their metagame info, it is submitted"""
        if self.metadata_flag == 3:
            pass # do nothing
        else:
            self.manual_metadata_receive()
        return "break"

    def manual_game_start(self):
        """Creates the class for a new game when button pressed by user"""

        # create a new class to handle the data entry window
        window = NewGameWindow(self.root, "new game")

        # collect the returned info
        data_provision_success, provided_info = window.return_info()

        if data_provision_success == True:
            # if we successfully get the data, then copy it out to relevant variables
            self.opp_name = provided_info[0]
            self.team_on_defence = provided_info[1]

            # start the new game
            self.start_new_game()

            # if not then nothing happens

    def start_new_game(self):
        """Sets up all the classes and methods needed for a new game"""
        
        # disable the new game button
        self.new_game_button.state(["disabled"])

        # increment game number
        self.number_of_games += 1

        # add the new opposition team to the main DF (same as for a player)
        self.team.add_player_to_main_DF(self.opp_name)

        # Assign a name to the game
        game_class_ref = "Game " + str(self.number_of_games)

        # create a new class with the assembled input data
        self.games[game_class_ref] = FrisbeeGame(self, self.number_of_games, self.opp_name, self.team_on_defence)

        # make a note of what the active game is called
        self.active_game = game_class_ref

        # create a game team stats tab
        self.team.build_game_stats_page(game_class_ref)

        # add the players to the new stats page
        self.team.add_players_to_stats_page(game_class_ref)

        # create a live game tab
        self.live_game = LiveGame(self, self.opp_name, self.number_of_games, self.team_on_defence)

    def run_machine_learning_analysis(self):
        """When called this method will run all the necessary functions to produce the player coefficients"""

        # create our matricies that capture the x and y data for machine learning
        self.ml_poss_factors_o = self.o_df.drop(columns=["Success"])
        self.ml_success_o = self.o_df["Success"]
        
        # split the data into training and test datasets
        x_train_o, x_test_o, y_train_o, y_test_o = train_test_split(self.ml_poss_factors_o, self.ml_success_o, test_size=0.25, random_state=14)

        # Initialize logistic regression model with L2 regularization (default)
        model = LogisticRegression(penalty='l2', solver='lbfgs', max_iter=1000)

        # Fit the model to the training data
        model.fit(x_train_o, y_train_o)

        # Predict on the test set
        y_pred = model.predict(x_test_o)

        # Evaluate performance
        print("Accuracy:", accuracy_score(y_test_o, y_pred))
        print("\nConfusion Matrix:\n", confusion_matrix(y_test_o, y_pred))
        print("\nClassification Report:\n", classification_report(y_test_o, y_pred))

        # Get the coefficients
        coefficients = model.coef_[0]  # Coefficients for each feature
        players = self.ml_poss_factors_o.columns            # Feature names

        # Combine into a DataFrame for easy interpretation
        player_performance = pd.DataFrame({
            'Player': players,
            'Impact': coefficients
        }).sort_values(by='Impact', ascending=False)

        print(player_performance)

        #def refine_parameters(self):
        #"""Uses cross validation to refine the machine learning model"""

        # Define the parameter grid
        param_grid = {
            'C': [0.01, 0.1, 0.5, 1],  # Inverse of regularization strength
            'penalty': ['l2'],
            'solver': ['lbfgs'],
        }

        # Initialize the grid search
        grid_search = GridSearchCV(LogisticRegression(max_iter=1000), param_grid, cv=3, scoring='accuracy' ,return_train_score=True, verbose=10)
        grid_search.fit(x_train_o, y_train_o)

        # Best parameters
        print("Best parameters:", grid_search.best_params_)

        # show the parameters for the best version
        best_model = grid_search.best_estimator_
        print(best_model.score(x_test_o, y_test_o))

        # Predict on the test set
        y_pred = best_model.predict(x_test_o)

        # Evaluate performance
        print("Accuracy:", accuracy_score(y_test_o, y_pred))
        print("\nConfusion Matrix:\n", confusion_matrix(y_test_o, y_pred))
        print("\nClassification Report:\n", classification_report(y_test_o, y_pred))

        # Get the coefficients
        coefficients = best_model.coef_[0]  # Coefficients for each feature
        players = self.ml_poss_factors_o.columns            # Feature names

        # Combine into a DataFrame for easy interpretation
        player_performance = pd.DataFrame({
            'Player': players,
            'Impact': coefficients
        }).sort_values(by='Impact', ascending=False)

        print(player_performance)

    def save_data(self):
        """Saves all the data acquired so far into a json file"""

        # establish file name
        filename = "stored_data/" + self.tournament_name + ".json"

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
            "metadata" : self.tournament_metadata,
            "players" : player_dict,
            "game_data" : games_dict,
        }

        # save the information
        with open(filename, 'w') as f:
            json.dump(dict_to_save, f, indent=4)

    def load_data(self):
        """Loads a saved json file for a tournament"""

        #!! choose file to load
        filename = "stored_data/Glasto 2019.json"

        # load data into a python dictionary
        with open(filename) as f:
            self.loaded_data = json.load(f)    

        #!! set the flag and call the data extraction function
        self.load_from_json = True
        self.extract_stock_data()    

# call the main code
if __name__ == "__main__":
    tournament_gui = MainGUI()

    print("Check results")