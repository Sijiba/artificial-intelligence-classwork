#  Modified by Spencer Berg
from myothello import *


class CandyLandPlayer(othello_player):
    #  This will be called once at the beginning of the game, after
    #  a few random moves have been made.  Boardstate is the initial
    #  boardstate for the game, totalTime is the total amount of time
    #  (in seconds) in the range 60-1800 that your player will get for
    #  the game.  For our tournament, I will generally set this to 300.
    #  color is one of Black or White (which are just constants defined
    #  in the othello.py file) saying what color the player will be
    #  playing.
    def initialize(self, boardstate, totalTime, color):
        self.name = "CandyLander"
        print("Initializing", self.name)
        self.mycolor = color
        pass

    # This should return the utility of the given boardstate.
    # It can access (but not modify) the to_move and _board fields.
    def calculate_utility(self, boardstate):
        my_weight = 0
        thy_weight = 0

        risky = 16  # anything 1 tile from any wall
        center = 17 # 4x4 square in middle
        wall = 19   # walls, but not next to corners
        corner = 20  # corners

        for row in range(0,8):
            for col in range(0,8):
                if boardstate._board[row*10 + col + 11] == self.mycolor:
                    # Add weighted board position for self
                    if (1 < row < 6) & (1 < col < 6):
                        my_weight = my_weight + center
                    elif (row % 7 == 0) & (col % 7 == 0):
                        my_weight = my_weight + corner
                    elif (row % 7 == 0) & (1 < col < 6):
                        my_weight = my_weight + wall
                    else:
                        my_weight = my_weight + risky
                elif boardstate._board[row*10 + col + 11] == opponent(self.mycolor):
                    # Add weighted board position for opponent
                    if (1 < row < 6) & (1 < col < 6):
                        thy_weight = thy_weight + center
                    elif (row % 7 == 0) & (col % 7 == 0):
                        thy_weight = thy_weight + corner
                    elif (row % 7 == 0) & (1 < col < 6):
                        thy_weight = thy_weight + wall
                    else:
                        thy_weight = thy_weight + risky

        return my_weight - thy_weight

    def alphabeta_parameters(self, boardstate, remainingTime):
        # This should return a tuple of (cutoffDepth, cutoffTest, evalFn)
        # where any (or all) of the values can be None, in which case the
        # default values are used:
        #        cutoffDepth default is 4
        #        cutoffTest default is None, which just uses cutoffDepth to
        #            determine whether to cutoff search
        #        evalFn default is None, which uses your boardstate_utility_fn
        #            to evaluate the utility of board states.
        moves = len(boardstate.legal_moves())

        if (boardstate._board.count(Empty) < 12):
            # plan endgame
            if count_difference(boardstate) < 0 | remainingTime > 400:
                return 12, None, self.calculate_utility
            elif remainingTime > 120:
                return 8, None, self.calculate_utility
        elif remainingTime < 30:
            # panic
            return 2, None, self.calculate_utility
        elif moves <= 5:
            return 6, None, self.calculate_utility
        else:
            return 4, None, self.calculate_utility

    def mycount_difference(self, boardstate):
        return (boardstate._board.count(self.mycolor) -
                boardstate._board.count(opponent(self.mycolor)))


def count_difference(boardstate):
    return (boardstate._board.count(boardstate.to_move)
            - boardstate._board.count(opponent(boardstate.to_move)))
