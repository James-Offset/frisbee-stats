"""This file contains a class for the game metadata popup window"""

import tkinter as tk
from tkinter import ttk

class NewGameWindow():
    def __init__(self, gui_root, entry_type):

        # copy out the root of the window and the entry required
        self.root = gui_root
        self.mode = entry_type

        # set a marker for what data we want
        self.request_number = -1
        self.output_data = []
        self.all_data_aquired = False
        self._establish_entries_required()

        # create the window and add widgets
        self._create_window()

        # stop the main GUI from running
        self._set_run_conditions()

    def _establish_entries_required(self):    
        """Based on what kind of data we want the user to input, we use different setting for this window"""

        if self.mode == "new game":
            self.config_dict = {
                "title" : "New Game Info",
                "heading" : "New Game:",
                "requests" : [
                    {
                    "prompt" : "Enter the name of the opposing team:",
                    "radio options" : None 
                    },
                    {
                    "prompt" : "Please enter which team starts on defence:",
                    "radio options" : ["My Team" , "Opposition Team"]
                    },
                ]
            }

        elif self.mode == "new program":
            self.config_dict = {
                "title" : "Program Set Up",
                "heading" : "New Analysis Program",
                "requests" : [
                    {
                    "prompt" : "Choose the program you want to run:",
                    "radio options" : ["Tournament", "Scrimmage"]
                    },
                ]
            }

        elif self.mode == "new tournament":
            self.config_dict = {
                "title" : "New Tournament",
                "heading" : "Tournment Info",
                "requests" : [
                    {
                    "prompt" : "Please enter the tournament name",
                    "radio options" : None
                    },
                    {
                    "prompt" : "Please enter your team name",
                    "radio options" : None
                    },
                    {
                    "prompt" : "How many players per side?",
                    "radio options" : ["5", "7"]
                    },
                ]
            }
            
        # count the number of entries we are expecting
        self.request_threshold = len(self.config_dict["requests"]) - 1

    def _create_window(self):
        """Creates the new window and adds the necessary widgets"""
        # create a new window
        self.game_metadata_window = tk.Toplevel(self.root)
        self.game_metadata_window.geometry("400x250")
        self.game_metadata_window.attributes("-topmost", 1)
        self.game_metadata_window.title(self.config_dict["title"])
        
        # add a heading
        self.heading_label = tk.Label(self.game_metadata_window, text=self.config_dict["heading"], font=('Arial', 16))
        self.heading_label.pack(pady=10)

        # put in the first request
        self.build_request_widgets()

    def build_request_widgets(self):
        """When we ask the user for new information, we create a new frame containing the right widgets"""

        # increment the request number
        self.request_number += 1

        # create a sub frame to hold the widgets for one request
        self.request_frame = tk.Frame(self.game_metadata_window)
        self.request_frame.pack(pady=10)

        # add label asking for information
        request_text = self.config_dict["requests"][self.request_number]["prompt"]
        self.request_label = tk.Label(self.request_frame, text=request_text, font=('Arial', 14))
        self.request_label.pack(pady=10)

        # add the user entry widget
        if self.config_dict["requests"][self.request_number]["radio options"] == None:
            # must be a text entry, add a box for the user to enter text information
            self.entry_box = tk.Text(self.request_frame, height=1, width=20, font=('Arial', 16))
            self.entry_box.pack(pady=5)
            self.entry_box.bind("<Return>", self.submit_info)
        else:
            # add a set of radio buttons
            self.choice = tk.StringVar()
            self.radio_dict = {}
            for option in self.config_dict["requests"][self.request_number]["radio options"]:
                self.radio_dict[option] = ttk.Radiobutton(self.request_frame, text=option, variable=self.choice, value=option)
                self.radio_dict[option].pack(pady=3)

        # add a submit button
        self.submit_button = ttk.Button(self.request_frame, text="Submit", command=self.submit_info)
        self.submit_button.pack(padx=10, pady=5)

        # add label giving the status
        self.status_label = tk.Label(self.request_frame, text="", font=('Arial', 14))
        self.status_label.pack(pady=5)

    def _set_run_conditions(self):
        """This code means that the window will exist and prevent anything from happening until it is completed or closed.
        For some reason it needs to be called last."""

        # prevent the rest of the programme doing anything until the data entry is resolved
        self.game_metadata_window.protocol("WM_DELETE_WINDOW", self.return_info) # intercept close button
        self.game_metadata_window.transient(self.root)   # dialog window is related to main
        self.game_metadata_window.wait_visibility() # can't grab until window appears, so we wait
        self.game_metadata_window.grab_set()        # ensure all input goes to our window
        self.game_metadata_window.wait_window()     # block until window is destroyed

    def submit_info(self, none=1):
        """Gets the written information and checks if it is good"""

        if self.config_dict["requests"][self.request_number]["radio options"] == None:
            # must be a text entry
            self.check_text_entry()
        else:
            # must be a radio entry
            self.check_radio_entry()

    def check_text_entry(self):
        """Checks whether the user has submitted a valid text entry"""

        # get the entry from the box
        entry = self.entry_box.get('1.0', tk.END)
        entry = entry[:-1] # take off the new line that gets added

        if len(entry) > 10 or len(entry) < 1:
            status_message = "Entry does not meet length requirements (max 10 characters)"
            self.status_label.config(text=status_message)
        else:
            # add the information to the output list
            self.output_data.append(entry)

            # see what needs to happen next
            self.follow_successful_entry()

    def check_radio_entry(self):
        """Check to see if the user has picked an option"""

        # get the chosen variable
        x = self.choice.get()

        if x in self.config_dict["requests"][self.request_number]["radio options"]:
            # add the information to the output list
            self.output_data.append(x)

            # see what needs to happen next
            self.follow_successful_entry()
        else:
            # the user must have not chosen an option yet.
            status_message = "Please select an option, then click submit"
            self.status_label.config(text=status_message)

    def follow_successful_entry(self):

        if self.request_number >= self.request_threshold: # we have all the info we want

            self.all_data_aquired = True

            # close the window
            self.close_window()

        else:
            # get rid of the old request widget frame
            self.request_frame.destroy()

            # ask for the next piece of info
            self.build_request_widgets()

    def close_window(self):
        self.game_metadata_window.grab_release()
        self.game_metadata_window.destroy()

    def return_info(self):
        """When called by the main file, this will return the user submitted data"""

        return self.all_data_aquired, self.output_data