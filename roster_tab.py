"""This is a file just to hold the notebook tab with the GUI elements showing the basic roster
It also has the button and the method to add new players"""

import tkinter as tk
from tkinter import ttk

from game_data_window import NewGameWindow

class RosterTab():
    def __init__(self, parent):
        self.parent = parent

        # keep a count of how many players we have
        self.player_count = -1
        self.taken_entries = []
        self.player_dictionary = {}

        # start by setting up the GUI tab
        self._create_notebook_tab()

    def _create_notebook_tab(self):
        """Creates a simple new tab where the user can see the players available and add new ones"""
        
        # create the new tab
        self.roster_tab = tk.Frame(self.parent.parent.notebook)
        self.roster_tab.pack()
        self.parent.parent.notebook.add(self.roster_tab, text="Team Roster")

        self._create_new_player_frame()
        self._create_player_name_canvas()


    def _create_new_player_frame(self):
        """Creates a frame at the top where the new player button will be"""

        # add a new frame to the notebook tab
        self.top_frame = tk.Frame(self.roster_tab)
        self.top_frame.pack()
        
        # add new player entry button
        self.new_player_button = ttk.Button(self.top_frame, text="Add New Player", command=self.manual_player_input)
        self.new_player_button.pack(pady=10)

        # add a label with the number of players
        self.label_for_player_number = tk.Label(self.top_frame, text="hello", font=("Arial", 14))
        self.label_for_player_number.pack(pady=5)

        # fix the label text
        self.update_count_label()
                
        # add a horizontal Separator
        s0 = ttk.Separator(self.top_frame, orient='horizontal')
        s0.pack(expand=True, fill="both", pady=2)

    def _create_player_name_canvas(self):
        """Creates the scollable canvas where the player names go"""

        # create the canvas and scrollbar
        self.canvas = tk.Canvas(self.roster_tab)
        self.v_scrollbar = ttk.Scrollbar(self.roster_tab, orient='vertical', command=self.canvas.yview)
        self.canvas['yscrollcommand'] = self.v_scrollbar.set
        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        # add a new frame to the canvas
        self.frame_of_names = tk.Frame(self.canvas)
        self.scrollable_window = self.canvas.create_window((0,0), anchor='nw', window=self.frame_of_names)

        # extra scrolling functionality
        self.frame_of_names.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.resize_scrollable_frame)

        # fill out the inner frame
        self._set_up_player_list()

    def resize_scrollable_frame(self, event):
        # Ensure the frame width matches the canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_window, width=canvas_width)

    def update_scroll_region(self, event):
        # Update the scroll region when the frame changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        # Enable mousewheel scrolling
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def _set_up_player_list(self):
        """This section creates a new frame that will hold a list of all the player names and numbers"""

        # create a dictionary to hold the details of the GUI columns
        self.gui_columns = {
            "heading text" : ["Player Name", "Player Number"],
            "column weighting" : [2, 2],
            "label elements" : {}
        }

        # create dictionaries to hold the gui labels
        self.gui_player_names = {}
        self.gui_player_numbers = {}

        # create columns in turn according to above configuration
        column_number=0
        for column in self.gui_columns["heading text"]:
            # create a column
            self.frame_of_names.columnconfigure(column_number, weight=self.gui_columns["column weighting"][column_number])
        
            # add heading labels
            self.gui_columns["label elements"][column] = tk.Label(self.frame_of_names, text=self.gui_columns["heading text"][column_number], font=('Arial', 18))
            self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=10)

            column_number += 1
        
        # horizontal Separator
        s0 = ttk.Separator(self.frame_of_names, orient='horizontal')
        s0.grid(row=1, column = 0, sticky=tk.W + tk.E, columnspan=2 , pady=2)

        # add player columns
        self.row_number = 1

    def update_count_label(self):
        """Updates the label that displays how many players are in the roster"""
        
        # increment the count
        self.player_count += 1

        # update the text
        text_string = str(self.player_count) + " players in roster"
        self.label_for_player_number.config(text=text_string)

    def manual_player_input(self):
        """This method will open a window to as for user input"""

        # create a new class to handle the data entry window
        window = NewGameWindow(self.roster_tab, "new player", self.taken_entries)

        # collect the returned info
        data_provision_success, provided_info = window.return_info()

        if data_provision_success == True:
            # if we successfully get the data, copy it out, if not then nothing happens
            self.add_player_to_records(provided_info[0], provided_info[1])

    def add_player_to_records(self, player_name, player_number):
        """If we have a valid name and number, add it to the necessary records"""

        # add the player info to the player dictionary
        self.player_dictionary[player_name] = {
            "name" : player_name,
            "number" : player_number,
        }

        # add the name and number to a list of taken values
        self.taken_entries.append(player_name)
        self.taken_entries.append(player_number)

        # feed the player info into the rest of the program
        self.parent.new_player_entry(player_name, player_number)

        # update the count label
        self.update_count_label()

        # add the player to the GUI
        self.add_player_to_GUI()

        # sort the players alphabetically
        self.sort_players()

    def add_player_to_GUI(self, name, number):
        """Adds a new row to the frame of names with the player details"""

        # increment row number
        self.row_number += 1

        # add name label
        self.gui_player_names[name] = tk.Label(self.frame_of_names, text=name, font=('Arial', 16))
        self.gui_player_names[name].grid(row=self.row_number , column = 0, sticky=tk.W + tk.E, pady=4)

        # add number label
        self.gui_player_numbers[name] = tk.Label(self.frame_of_names, text=number, font=('Arial', 16))
        self.gui_player_numbers[name].grid(row=self.row_number , column = 1, sticky=tk.W + tk.E, pady=4)

    def sort_players(self):
        """When called by the team class, sorts the players on the GUI"""

        # get the list of players and sort the list
        list_of_players = list(self.player_dictionary.keys())
        list_of_players.sort()

        # reset the row count
        self.row_number = 1

        # move the name and number for each player to the new spot
        for player in list_of_players:
            # increment row number
            self.row_number += 1

            # move labels
            self.gui_player_names[player].grid_configure(row=self.row_number)
            self.gui_player_numbers[player].grid_configure(row=self.row_number)
            