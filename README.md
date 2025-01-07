# frisbee-stats


-- Overview-- 

This project attempts to take an analytical approach to player evaluation in a game of ultimate frisbee. This can be done using data input across a series of games, for example a weekend-long tournament.  

It will output a number of statistics on player performance that will compare the effectiveness of the team when that player is on the field vs when they are not. These are explained more below.

To enter information into the program you will need a record of which players were on the field for each point, and how many turnovers there were on those points.

Note that to be effective the line up of players should change each point with as many different combinations of players on the field as possible. Having fixed offense and defense lines will not produce any results.

*Disclaimer* I'm not a software engineer or a statistician, nor is this a professional project, so I expect there to be many flaws.

-- Program start -- 

The program is run from the central_doc.

There are two options for data input, either this can be done manually by clicking on the "start program" button or by loading tournament data.
Loaded data must be in excel based on the provided template, or in a json file produced by the program when you click "save data".

Using a manual start, the user should input the prompted data. Note that a tournament name is still required even if you wish to evaluate a single game.

Once that metadata is entered, navigate to the roster tab and enter the player names and numbers. New players may be added to the roster at any time.

-- New Game --

Once there are sufficient players for a game, you will be able to select "start new game" from the home page.

The user will be prompted to enter details for the game.

A new game will create three new tabs. One presents stats from the game, another records the key events from each point and the third will be the "Live Game" tab. There can only be one Live Game at a time.

The live game tab allows the user to input the players present on the field for each point and count the number of turnovers. This information is submitted by clicking on "End Point", and the score will be updated accordingly. 

Preliminary stats are updated for each point and visible on the game stats tab.

Enter information for each point and then click "End Game". There is also a button to record half time. 

-- Post Game --

Following the end of a game, or the loading of previous data, more detailed stats will be calculated. These can be seen on the various stats pages. Furthermore the "Awards" section of the program will be updated. 

The user will then be able to run the machine learning algorithm and/or start a new game.

-- Explaination of Stats -- 

Basic stats are calcualted for the team and each player.
These are:

PP - number of Points Played

OP - the number of Offensive Possessions played

DP - the number of Defensive Possessions played

OC - the rate at which the team has an Offensive possession and Converts this into a goal (as opposed to conceding a turnover) while the player is on the field. This is a percentage score. For example if a player plays 10 offensive possession and the team score 6 times, then at player's offensive converstion rate will be 60%.

DC - the rate at which the team is on Defence for a possession and Converts this into a turnover (as opposed to conceding a goal) while the player is on the field. This is a percentage score 

O-Score (OS) - this is the percentage likelihood that the team will win a point when starting on offence and the target player is on the field. This means either scoring on offence, or if the disc is ever turned over the team will win it back and have another chance to score. 
The formula for this is OS = OC / (1 - (1 - OC)*DC)

D-Score (DS) - this is the percentage likelihood that the team will win a point when starting on defence and the target player is on the field. This means the team will win it back the disc however many times it takes to score. It is the same as O-Score, but the team must first win a turnover to gain first possession of the disc. 
The formula for this is DS = OS * DC

At the end of each game the marginal stats will be calcualted for each player. 
This will only happen if the player has at least four possessions where they are on the pitch and 4 where they are not, for offence and deffence. This is so there are sufficient data points where the team is playing with/without this player that that individual's impact on the team can be distinguished. 

A marginal stat is equal to the difference in a base stat when a player is on the field vs when they are not. For example if the team scores 60% of possessions when Player A is on the field, but only 40% of offensive possessions when they are not, then Player A's Marginal Offensive Score (MOC) is equal to 60% - 40% = +20%. If the team performs better when a player is not on the field, that player will have a negative marginal score. 

Conversion rates and marginal scores for each player on the tournament summary tab are the mean value of their scores for each game. They are not calculated based on aggregated counts of turnovers and points across the whole tournament. 


-- Machine Learning -- 

After the first game, the option will be available to run the machine learning algorithm from the home page. I do not know the amount of data required to produce reliable predicitons, but I expect it would be after at least 3 or 4 games. 

Clicking this button will open up an new tab and display the coefficients assigned to each player and opponent (and wind direction if playing outdoors). A larger positive coefficient indicates the player is significantly above average, while a negative coefficient suggests they are below average. Essentially, a higher score is better. Note that the equation is not linear, and so a score of 0.06 does not literally translate into an increased probability of 6%, and is not twice as good as a score of 0.03. 

This program uses a logistic regression algorithm, that tries to predict for an offensive or defensive possession whether the team will get a positive outcome based on the players on the field, opponent and wind. 

https://en.wikipedia.org/wiki/Logistic_regression

There is no functionality to make predictions based on the model, only to see the coefficients. 

The machine learning results will need to be recalculated after each game by clicking the button again.

The outputs of machine learning do not count towards the awards.


-- Final words -- 

I've put as much effort into this as I want to as a learning exercise. I appreciate it is far from perfect, and maybe quite clunky, but I hope it may be useful to some. I have ideas for improvements but no plans to implement them as of yet.

Please feel free to get in touch or continue the work yourself. 