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


"""My Code"""
from data_extractor import DataExtractor




class HomePage():
    """This class is the home page for the app and calls all the subclasses and functions.
    The core initial function is to collect tournament metadata"""

    def __init__(self):
        """Initialise the programme. For now this means to import the data and start the first game"""

        # start by importing all the data
        extraction_tool = DataExtractor()
        self.tournament_metadata, self.roster, self.raw_game_data = extraction_tool.import_stock_data()

# call the main code
if __name__ == "__main__":
    the_tournament = HomePage()

    print("Check results")