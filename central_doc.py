"""This is the base document that will call all of the other functions and classes"""

"""
Now we are changing the way we do the scores so that we have comparisons with each player individually
"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV

"""My Code"""
from data_extractor import DataExtractor
from frisbee_match import FrisbeeGame
from team_roster import Team
from live_game import LiveGame



class MainGUI():
    """This class is the home page for the app and calls all the subclasses and functions.
    The core initial function is to collect tournament metadata"""

    def __init__(self):
        """Set up the GUI and allow the user to call subsequent functions"""

        # create GUI window
        self.root = tk.Tk()

        # set root settings
        self.gui_width = 700
        self.gui_height = 700
        geometry_set = str(self.gui_width) + "x" + str(self.gui_height)
        self.root.geometry(geometry_set)
        self.root.title("Ultimate Statistics User Interface")

        # build notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # set up key tabs
        self._build_homepage()
        
        # create a blank dictionary to store our game classes
        self.games = {}
        self.number_of_games = 0 

        # set up a few markers
        self.data_extracted = False
        self.game_import = False
        self.live_game_active = False
        self.metadata_flag = 0

        #!! Set up some temporary opp names
        self.opp_name_count = 0

                
        # run the app
        self.root.mainloop()
        print("check")

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
        self.new_game_button = ttk.Button(self.home_page, text="Start New Game", command=self.start_new_game)
        self.new_game_button.pack(padx=20, pady=20)

        # add a button to run the analysis
        self.ml_button = ttk.Button(self.home_page, text="Do Machine Learning!", command=self.run_machine_learning_analysis)
        self.ml_button.pack(padx=20, pady=20)

        # add a save tournament info and load tournament info buttons
        self.save_data = ttk.Button(self.home_page, text="Save Tournament Data", command=self.start_new_game)
        self.save_data.pack(padx=20, pady=5)

        self.load_data = ttk.Button(self.home_page, text="Load Tournament Data", command=self.start_new_game)
        self.load_data.pack(padx=20, pady=5)

        # disable buttons not immediately useful
        self.new_game_button.state(["disabled"])
        self.new_player_button.state(["disabled"])
        
    
    def manual_metadata_receive(self):
        """This is the method that will trigger when the metadata button is pushed"""

        box_entry = self.metadata_box.get('1.0', tk.END)

        self.metadata_message = "Unknown Error"

        try:
            if self.metadata_flag == 0:
                team_name = box_entry[:-1]
                if len(team_name) < 20 and len(team_name) > 2:
                    self.team_name = team_name
                    self.metadata_flag = 1
                    self.metadata_message = "Please enter the tournament name"
                    self.metadata_box.delete('1.0', tk.END)
                else:
                    self.metadata_message = "Team name length must be no more than 20 characters"
            elif self.metadata_flag == 1:
                tournament_name = box_entry[:-1]
                if len(tournament_name) < 20 and len(tournament_name) > 2:
                    self.tournament_name = tournament_name
                    self.metadata_flag = 2
                    self.metadata_message = "Please enter the number of players on at once (5 or 7)"
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

        self.metadata_label.config(text=self.metadata_message)

    def extract_stock_data(self):
        """Looks at the provided excel file and creates dictionaries of all player and game data"""

        if self.data_extracted == False:
            # set the falg to True
            self.data_extracted = True

            # Tournament metadata for input
            #self.tournament_name = "MIR2017"
            #self.team_name = "Mythago"
            #!!self.number_of_players_at_once = 5
            self.tournament_name = "Glasto 2019"
            self.team_name = "Mythagone"
            self.number_of_players_at_once = 7

            # now we have the metadata, we can complete the set up
            self.complete_set_up()

            # import all the data
            extraction_tool = DataExtractor()
            self.tournament_metadata, self.imported_roster, self.raw_game_data = extraction_tool.import_stock_data()

            # change button text once data is extracted !! move this later
            self.resultsContents = tk.StringVar()
            self.import_status_label['textvariable'] = self.resultsContents
            self.resultsContents.set('Import Game Data')

            # create player classes
            for player in self.imported_roster:
                self.team.new_player_entry(player, self.imported_roster[player]['Player Number'])

        elif self.game_import == False:
            # create game classes
            self._create_game_classes_from_import()
            self.game_import = True
            self.resultsContents.set('Data extracted')
            self.import_data_button.state(["disabled"])
                    
    def _create_game_classes_from_import(self):
        """Creates a class for each game played and runs the relevant functions"""

        # create a loop for each game
        for game_number in range(self.tournament_metadata['Number of Games']):
            self.start_new_game()

            # find the set of raw data that applies to that game
            for name_of_considered_game in self.raw_game_data:
                if self.active_game in name_of_considered_game:
                    break
            
            self.games[self.active_game].crunch_data_from_import(self.raw_game_data[name_of_considered_game]['Turns per Point'], self.raw_game_data[name_of_considered_game]["Active Players"])
            
            self.live_game.end_game()

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
        

    def manual_player_input(self):
        """Takes the user entry in the text boxes and checks it. If ok, adds a new player"""

        # copy out the user entries
        name_entry = self.player_name_box.get('1.0', tk.END)
        number_entry = self.player_number_box.get('1.0', tk.END)

        # pass to function in team class
        return_message = self.team.check_manual_player_entry(name_entry, number_entry)

        # show the message communicating whether the data entry was successful or not
        self.player_entry_status_label.config(text=return_message)

        # self.player_name_box.delete

    def disable_newline(self, event):
        """If someone tries to hit enter while putting in an entry, it will do nothing"""
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

    def start_new_game(self):
        """Creates the class for a new game when button pressed by user"""
        
        if self.live_game_active == False:
            # increment game number
            self.number_of_games += 1

            #!! Get new game metadata here
            self.opp_name_count += 1
            self.opp_name = "Opp " + str(self.opp_name_count)

            # add the new opposition team to the main DF (same as for a player)
            self.team.add_player_to_main_DF(self.opp_name)

            # Assign a name to the game
            game_class_name = "Game " + str(self.number_of_games)

            # create a new class with the assembled input data
            self.games[game_class_name] = FrisbeeGame(self, game_class_name, self.opp_name)

            # make a note of what the active game is called
            self.active_game = game_class_name

            # create a game team stats tab
            self.team.build_game_stats_page(game_class_name)

            # add the players to the new stats page
            self.team.add_players_to_stats_page(game_class_name)

            # create a live game tab
            self.live_game_active = True
            self.live_game = LiveGame(self, self.opp_name)

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


# call the main code
if __name__ == "__main__":
    tournament_gui = MainGUI()

    print("Check results")