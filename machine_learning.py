"""This file will hold the class that creates a new tab and carries out the machine learning methods"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV

import tkinter as tk
from tkinter import ttk

import pandas as pd

class MachineLearning():
    def __init__(self, parent, game_data, environment, player_dictionary, list_of_opponents):
        """establish variables and call main methods"""

        self.parent = parent
        self.game_data = game_data
        self.environment = environment
        self.player_dictionary = player_dictionary
        self.list_of_opponents = list_of_opponents

        self.player_list = self.player_dictionary.keys()

        # create a new tab in the notebook
        self._create_notebook_tab()

        # run the algorithm
        self.set_up_process()



    def _create_notebook_tab(self):
        """Creates a new tab in the notebook and sets up scroll capability"""

        # create the new tab
        self.tab_page = tk.Frame(self.parent.notebook)
        self.tab_page.pack()
        self.parent.notebook.add(self.tab_page, text="Deep Analysis")

        # create the canvas and scrollbar
        self.canvas = tk.Canvas(self.tab_page)
        self.v_scrollbar = ttk.Scrollbar(self.tab_page, orient='vertical', command=self.canvas.yview)
        self.canvas['yscrollcommand'] = self.v_scrollbar.set
        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        # add a new frame to the canvas
        self.stats_frame = tk.Frame(self.canvas)
        self.scrollable_window = self.canvas.create_window((0,0), anchor='nw', window=self.stats_frame)

        # extra scrolling functionality
        self.stats_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.resize_scrollable_frame)

        # fill out the inner frame
        self._create_stats_grid_content()

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

    def _create_stats_grid_content(self):
        """"Adds the GUI label elements into a grid inside the scrollable frame"""

        # create a dictionary to hold the details of the GUI columns
        self.gui_columns = {
            "heading text" : ["Player Name", "Player Number", "Offence Coefficient", "Defence Coefficient"],
            "column weighting" : [2, 2, 2, 2],
            "label elements" : {}
        }

        self.number_of_columns = len(self.gui_columns["heading text"])

        # create dictionaries to hold the gui labels (organised by player/factor)
        self.gui_labels = {}

        # create columns in turn according to above configuration
        column_number=0
        for column in self.gui_columns["heading text"]:

            # create a column
            self.stats_frame.columnconfigure(column_number, weight=self.gui_columns["column weighting"][column_number])
        
            # add heading labels
            if "separator" in column:
                self.gui_columns["label elements"][column] = ttk.Separator(self.stats_frame, orient="vertical")
                self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky='ns', padx=2)
            else:
                self.gui_columns["label elements"][column] = tk.Button(self.stats_frame, text=self.gui_columns["heading text"][column_number], font=('Arial', 16), command=lambda t=column: self.sort_gui_labels(t))
                self.gui_columns["label elements"][column].grid(row=0 , column = column_number, sticky=tk.W + tk.E, pady=10)

            column_number += 1
        
        # horizontal Separator
        s0 = ttk.Separator(self.stats_frame, orient='horizontal')
        s0.grid(row=1, column = 0, sticky=tk.W + tk.E, columnspan=self.number_of_columns , pady=2)

        # add award columns
        self.number_of_player_rows = 1

    
    def set_up_process(self):
        """When called this method will run all the necessary functions to produce the player coefficients"""

        # set up necessary dictionarys to hold offence and defence variables
        self.variable_factors = {}
        self.success_counts = {}
        self.input_training_data = {}
        self.input_test_data = {}
        self.output_training_data = {}
        self.output_test_data = {}
        self.output_predictions = {}
        self.results_dictionary = {}

        
        self.factor_list = self.game_data["offence"].columns[1:]
        player_numbers = []
        for factor in self.factor_list:
            if factor in self.player_list:
                player_numbers.append(self.player_dictionary[factor]["number"])
            else:
                player_numbers.append(1000)

        self.compilation_table = pd.DataFrame({
            "Player Name" : self.factor_list,
            "Player Number" : player_numbers,
        },
        index= self.factor_list
        )

        for poss_type in ("offence", "defence"):

            # creat a new sub dictionary for the results
            self.results_dictionary[poss_type] = {}

            # run the calculations
            self.machine_learning_computation(poss_type)

        # update the GUI
        self._update_GUI()
                
        # sort the display elements
        self.sort_gui_labels("Offence Coefficient")

    def machine_learning_computation(self, poss_type):
        """Runs the computational steps for offence or defence"""

        print(f"\n--- Analysing {poss_type} data: ---\n")

        # create our matricies that capture the x and y data for machine learning, aka separate the inputs and outputs
        self.variable_factors[poss_type] = self.game_data[poss_type].drop(columns=["Success"])
        self.success_counts[poss_type] = self.game_data[poss_type]["Success"]
        
        # split the data into training and test datasets
        self.input_training_data[poss_type], self.input_test_data[poss_type], self.output_training_data[poss_type], self.output_test_data[poss_type] = train_test_split(self.variable_factors[poss_type], self.success_counts[poss_type], test_size=0.25, random_state=14)

        # Initialize logistic regression model with L2 regularization (default)
        self.model = LogisticRegression(penalty='l2', solver='lbfgs', max_iter=1000)

        # Fit the model to the training data
        self.model.fit(self.input_training_data[poss_type], self.output_training_data[poss_type])

        # Predict on the test set
        self.output_predictions[poss_type] = self.model.predict(self.input_test_data[poss_type])

        print(f"\n** Default Settings **")

        self.print_machine_learning_outputs(poss_type)

        print(f"\n** Grid Search Settings **")

        self.refine_parameters(poss_type)
        self.print_machine_learning_outputs(poss_type)

    def refine_parameters(self, poss_type):
        """Uses cross validation to refine the machine learning model"""

        # Define the parameter grid
        param_grid = {
            'C': [0.01, 0.1, 0.5, 1],  # Inverse of regularization strength
            'penalty': ['l2'],
            'solver': ['lbfgs'],
        }

        # Initialize the grid search
        grid_search = GridSearchCV(LogisticRegression(max_iter=1000), param_grid, cv=3, scoring='accuracy' ,return_train_score=True, verbose=10)
        grid_search.fit(self.input_training_data[poss_type], self.output_training_data[poss_type])

        # Best parameters
        print("Best parameters:", grid_search.best_params_)

        # show the parameters for the best version
        best_model = grid_search.best_estimator_
        print(best_model.score(self.input_test_data[poss_type], self.output_test_data[poss_type]))

        # Predict on the test set
        self.output_predictions[poss_type] = best_model.predict(self.input_test_data[poss_type])

        # update the display table
        coefficients = self.model.coef_[0]
        rounded_coefficients = []
        for i in coefficients:
            rounded_coefficients.append(round(i,2))
        column_title = poss_type.capitalize() + " Coefficient"
        self.compilation_table[column_title] = rounded_coefficients



    def print_machine_learning_outputs(self, poss_type):
        """prints the outputs of the machine learning analysis"""

        # Evaluate performance
        print("Accuracy:", accuracy_score(self.output_test_data[poss_type], self.output_predictions[poss_type]))
        print("\nConfusion Matrix:\n", confusion_matrix(self.output_test_data[poss_type], self.output_predictions[poss_type]))
        print("\nClassification Report:\n", classification_report(self.output_test_data[poss_type], self.output_predictions[poss_type]))

        # Get the coefficients
        coefficients = self.model.coef_[0]  # Coefficients for each feature
        players = self.variable_factors[poss_type].columns            # Feature names

        # Combine into a DataFrame for easy interpretation
        player_performance = pd.DataFrame({
            'Player': players,
            'Impact': coefficients
        }).sort_values(by='Impact', ascending=False)

        print(player_performance)

    def _update_GUI(self):
        """Once the algorithm has worked out the coefficients, we update the GUI"""
        
        print(self.compilation_table)
        for factor in self.factor_list:
            if factor in self.gui_labels:
                pass
            else:
                self.add_factors_to_gui(factor)
                #!! need to come up with something or the non-player factors


    
    def add_factors_to_gui(self, player):
        """Adds a player to the GUI"""

        # increment the row number 
        self.number_of_player_rows += 1

        # create a new sub-dictionary for the player labels
        self.gui_labels[player] = {}

        column_number = 0

        # create a new label for each column
        for column in self.gui_columns["heading text"]:
            
            # add info label
            self.gui_labels[player][column] = tk.Label(self.stats_frame, text=self.compilation_table[column][player], font=('Arial', 14))
            self.gui_labels[player][column].grid(row=self.number_of_player_rows , column = column_number, sticky=tk.W + tk.E, pady=2)

            # increment column number
            column_number += 1


    def sort_gui_labels(self, sort_column):
        """sorts the rows of the gui by offence coefficient of defence"""

        # set the sort order
        if "Coefficient" in sort_column:
            sort_ascending = False
        else:
            sort_ascending = True

        # sort the table of data by that column
        self.sorted_table = self.compilation_table.sort_values(by=sort_column, ascending=sort_ascending)

        # start the row count at 0
        display_row = 1

        for factor in self.sorted_table["Player Name"]:
            # increment row number
            display_row += 1

            for column in self.gui_columns["heading text"]:          
                # change grid configuration
                self.gui_labels[factor][column].grid_configure(row=display_row)


