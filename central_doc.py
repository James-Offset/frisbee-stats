"""This is the base document that will call all of the other functions and classes"""

"""
The Plan:

Ideally this would be hosted online or in some kind of app, where the user can enter data.
Until then, I will just import the information from excel.

One account per tournament

We first need to establish the team roster and tournament metadata
Then the user will set up new games and enter the metadata for the game
Then we get all the raw points and turnover information.

At some point we trigger the programme to calculate all the data.
Probably based on a game end confirmation

Then we will offer a prompt to print off the key data.
And that's it I think.
"""

"""Third Party Code"""
import tkinter as tk
from tkinter import ttk

"""My Code"""
from data_extractor import DataExtractor
from frisbee_match import FrisbeeGame
from team_roster import Team



class MainGUI():
    """This class is the home page for the app and calls all the subclasses and functions.
    The core initial function is to collect tournament metadata"""

    def __init__(self):
        """Set up the GUI and allow the user to call subsequent functions"""

        # create GUI window
        self.root = tk.Tk()

        # set root settings
        self.root.geometry("600x600")
        self.root.title("Ultimate Statistics User Interface")

        # build notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        self.game_tabs = {}

        # set up key tabs
        self._build_homepage()

        # Create supporting classes
        self.team = Team(self)

        # create a blank dictionary to store our game classes
        self.games = {}
        self.number_of_games = 0 

        # set up a few markers
        self.data_extracted = False
                

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

        # add a checkbox for custom data, and a button for data collection
        self.checkstate = tk.IntVar()
        self.check = tk.Checkbutton(self.home_page, text="Input Own Data", font=('Arial', 14), variable=self.checkstate)
        self.check.pack(padx=10,pady=10)
        self.data_button = tk.Button(self.home_page, text="Import Data", font=('Arial', 16), command=self.extract_stock_data)
        self.data_button.pack(padx=10,pady=10)

        # add a status label
        self.status_label = tk.Label(self.home_page, text="Please click for data input")
        self.status_label.pack()

        # add new game button
        self.new_game_button = tk.Button(self.home_page, text="New Game", font=('Arial', 16), command=self.start_new_game)
        self.new_game_button.pack(padx=20, pady=20)
    

    def extract_stock_data(self):
        """Looks at the provided excel file and creates dictionaries of all player and game data"""

        if self.data_extracted == False:
            # set the falg to True
            self.data_extracted = True

            # import all the data
            extraction_tool = DataExtractor()
            self.tournament_metadata, self.imported_roster, self.raw_game_data = extraction_tool.import_stock_data()

            # change button text once data is extracted !! move this later
            resultsContents = tk.StringVar()
            self.status_label['textvariable'] = resultsContents
            resultsContents.set('Data extracted')

            # create player classes
            for player in self.imported_roster:
                self.team.new_player_entry(player, self.imported_roster[player]['Player Number'])

            # create game classes
            self._create_game_classes_from_import()
                    


    def _create_game_classes_from_import(self):
        """Creates a class for each game played and runs the relevant functions"""

        # create a loop for each game
        for game_number in range(self.tournament_metadata['Number of Games']):
            self.start_new_game()

            # find the set of raw data that applies to that game
            for game_data in self.raw_game_data:
                if self.active_game in game_data:
                    break
            
            self.games[self.active_game].crunch_data_from_import(self.raw_game_data[game_data]['Turns per Point'])


    def start_new_game(self):
        """Creates the class for a new game when button pressed by user"""
        
        # increment game number
        self.number_of_games += 1

        # Assign a name to the game
        game_class_name = "Game " + str(self.number_of_games)

        # create a new class with the assembled input data
        self.games[game_class_name] = FrisbeeGame(self, game_class_name)

        # make a note of what the active game is called
        self.active_game = game_class_name

# call the main code
if __name__ == "__main__":
    tournament_gui = MainGUI()

    print("Check results")