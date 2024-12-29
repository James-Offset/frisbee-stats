"""This file contains a class for the game metadata popup window"""

import tkinter as tk
from tkinter import ttk

class NewGameWindow():
    def __init__(self, gui_root, entry_type):

        # copy out the root of the window and the entry required
        self.root = gui_root
        self.mode = entry_type

        # create the window and add widgets
        self._create_window()

        # set a marker for what data we want
        self.data_marker = 0
        self.output_data = []
        self.all_data_aquired = False
        self._establish_entries_required()

        # update window to configuration
        self._configure_window()

        # stop the main GUI from running
        self._set_run_conditions()

    def _create_window(self):
        """Creates the new window and adds the necessary widgets"""
        # create a new window
        self.game_metadata_window = tk.Toplevel(self.root)
        self.game_metadata_window.geometry("400x250")
        self.game_metadata_window.attributes("-topmost", 1)
        
        # add label asking for information
        self.title_label = tk.Label(self.game_metadata_window, text="", font=('Arial', 16))
        self.title_label.pack(pady=10)

        # add label asking for information
        self.window_label = tk.Label(self.game_metadata_window, text="", font=('Arial', 14))
        self.window_label.pack(pady=10)

        # add a box for the user to enter the information
        self.entry_box = tk.Text(self.game_metadata_window, height=1, width=20, font=('Arial', 16))
        self.entry_box.pack(pady=5)
        self.entry_box.bind("<Return>", self.submit_info)

        # add a submit button
        self.submit_button = ttk.Button(self.game_metadata_window, text="Submit", command=self.submit_info)
        self.submit_button.pack(padx=10, pady=5)

        # add label giving the status
        self.status_label = tk.Label(self.game_metadata_window, text="", font=('Arial', 14))
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

    def _establish_entries_required(self):    
        """Based on what kind of data we want the user to input, we use different setting for this window"""

        if self.mode == "new game":
            self.number_of_entries_req = 2
            self.config_dict = {
                "Title" : "New Game Info",
                "Heading" : "New Game:",
                "Request" : ["Enter the name of the opposing team:", "Please enter which team starts on defence"],
            }

    def _configure_window(self):
        """Updates the window according to the specific configuration settings"""

        self.game_metadata_window.title(self.config_dict["Title"])
        self.title_label.config(text=self.config_dict["Heading"])

        self.update_labels()

    def update_labels(self):
        """Updates labels to ask for the next piece of information"""

        # update the request label
        self.window_label.config(text=self.config_dict["Request"][self.data_marker])

        # empty the entry box
        self.entry_box.delete('1.0', tk.END)

        # clear the status label
        self.status_label.config(text="")

    def submit_info(self):
        """Gets the written information and checks if it is good"""

        # get the entry from the box
        entry = self.entry_box.get('1.0', tk.END)
        entry = entry[:-1] # take off the new line that gets added

        if len(entry) > 15 or len(entry) < 2:
            status_message = "Entry exceeds 15 characters"
            self.status_label.config(text=status_message)
        else:
            # add the information to the output list
            self.output_data.append(entry)

            # increment the info marker
            self.data_marker += 1

            if self.data_marker >= self.number_of_entries_req: # we have all the info we want

                self.all_data_aquired = True

                # close the window
                self.close_window()

            else:
                # ask for the next piece of info
                self.update_labels()

    def close_window(self):
        self.game_metadata_window.grab_release()
        self.game_metadata_window.destroy()

    def return_info(self):
        """When called by the main file, this will return the user submitted data"""

        return self.all_data_aquired, self.output_data