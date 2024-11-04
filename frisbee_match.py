"""This file holds the class for a single frisbee game

The main purpose of this class will be to capture the line-ups for each point and the number of turn-overs per point.
Ideally we would have some kind of readout displaying the live score

Meta data would be the game number, opposition name, maybe date and time, who starts on offence

Functions:
Capture the line-up for a point (maybe by calling a function within the point class)
Work out what the live score is + print whether last point was a hold or a break
Initiate half time
calculate stats for just this game > maybe call another class



Calculate overall game stats: num_points, num_turns, num_o_starts, num_possessions, avg_poss_per_point
Turns Won
Turns Lost
No. O Posessions
No. D Posessions

Score rate
Pos Loss Rate
Concede rate
Pos Win Rate

Predicted Goals for
Predicted Goals Against
Net

O start goal
O start concede
D start goal
D start concede

O goal rate
O concede rate
D goal rate
D concede rate

Pos / OG
Pos / OC
Pos / DG
Pos / DC

No. O / OG
No. D / OG
No. D / DG
No. O / DG

"""

class FrisbeeMatch():
    def __init__(self):
        """This stores the core infomation"""