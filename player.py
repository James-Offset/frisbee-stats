"""Any data that needs to be stored or processed at the player level is stored here

Not sure if this is necessary at this point, but we can set up a class if needed. 
"""

# create a dictionary to store performance data for each player
for player in self.imported_roster:
    self.imported_roster[player][game_class_name] = {
        "Points Played" : 0,
        "Points Scored" : 0,
        "Points Won" : 0,
        "Turns Won" : 0,
        "Turns Lost" : 0
    }