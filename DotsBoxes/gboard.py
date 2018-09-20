"""An implementation of a game board for the game Dots-And-Boxes.

Danny Yoo (dyoo@hkn.eecs.berkeley.edu)

Dots-And-Boxes is a game played between two people.  For the purposes
of this board, let's label these two players 0 and 1.  The two players
take turns drawing horizontal or vertical lines between adjacent
points.  If a player's move connects four dots as a square, then that
player captures that square, and gets to make another move.  Whoever
captures the most squares wins!


I got inspired to write this once I started reading Elwyn Berlekamp's
'The Dots and Boxes Game, Sophisticated Child's Play':

    http://www.akpeters.com/book.asp?bID=111


I haven't seen a canonical way of representing moves in the literature
I've read.  I had to decide something, so I'll represent a move as a
2-sequence of coordinate tuples, played on the first coordinate region
of a graph.  For example,

    ((0, 0), (1, 0))

should represent a horizontal line right at the bottom left corner.  I
think I'll wuss out and say that it's up to the user interface to make
inputting moves nicer.  (I'd like to write some Pygame GUI code to make
it easier to play the game, so that's my next target if I have time.)


I'm mostly happy with this implementation, except for the definitions
of GameBoard._isSquareMove() and GameBoard.__str__(); they seem a bit
complicated, but I'm not seeing an easy way to simplify them yet."""
from othello import Game

class GameBoard(Game):
    def __init__(self, width=5, height=5, to_move=0, utility=None, board=None, moves=None):
        """Initializes a rectangular gameboard."""
        if board is None:
            board = {}
        self.width, self.height = width, height
        assert 2 <= self.width and 2 <= self.height, \
            "Game can't be played on this board's dimension."
        self.board = board
        self.utility = utility
        self.squares = {}
        self.moves = moves
        self.player = to_move

    def isGameOver(self):
        """Returns true if no more moves can be made.

        The maximum number of moves is equal to the number of possible
        lines between adjacent dots.  I'm calculating this to be
        $2*w*h - h - w$; I think that's right.  *grin*
        """
        w, h = self.width, self.height
        return len(self.board.keys()) == 2 * w * h - h - w

    def _isSquareMove(self, move):
        """Returns a true value if a particular move will create a
        square.  In particular, returns a list of the the lower left
        corners of the squares captured by a move.

        (Note: I had forgotten about double crossed moves.  Gregor
        Lingl reported the bug; I'd better fix it now!  *grin*) """
        b = self.board
        mmove = self._makeMove  ## just to make typing easier
        ((x1, y1), (x2, y2)) = move
        captured_squares = []
        if self._isHorizontal(move):
            for j in [-1, 1]:
                if (mmove((x1, y1), (x1, y1 - j)) in b
                    and (mmove((x1, y1 - j), (x1 + 1, y1 - j))) in b
                    and (mmove((x1 + 1, y1 - j), (x2, y2))) in b):
                    captured_squares.append(min([(x1, y1), (x1, y1 - j),
                                                 (x1 + 1, y1 - j), (x2, y2)]))
        else:
            for j in [-1, 1]:
                if (mmove((x1, y1), (x1 - j, y1)) in b
                    and (mmove((x1 - j, y1), (x1 - j, y1 + 1))) in b
                    and (mmove((x1 - j, y1 + 1), (x2, y2))) in b):
                    captured_squares.append(min([(x1, y1), (x1 - j, y1),
                                                 (x1 - j, y1 + 1), (x2, y2)]))
        return captured_squares

    def _isHorizontal(self, move):
        "Return true if the move is in horizontal orientation."
        return abs(move[0][0] - move[1][0]) == 1

    def _isVertical(self, move):
        "Return true if the move is in vertical orientation."
        return not self._isHorizontal(move)

    def play(self, move):
        """Place a particular move on the board.  If any wackiness
        occurs, raise an AssertionError.  Returns a list of
        bottom-left corners of squares captured after a move."""
        assert (self._isGoodCoord(move[0]) and
                self._isGoodCoord(move[1])), \
            "Bad coordinates, out of bounds of the board."
        move = self._makeMove(move[0], move[1])
        assert (not (move) in self.board), \
            "Bad move, line already occupied."
        self.board[move] = self.player
        ## Check if a square is completed.
        square_corners = self._isSquareMove(move)
        if square_corners:
            for corner in square_corners:
                self.squares[corner] = self.player
        else:
            self._switchPlayer()
        return square_corners

    def _switchPlayer(self):
        self.player = (self.player + 1) % 2

    def getPlayer(self):
        return self.player

    def getSquares(self):
        """Returns a dictionary of squares captured.  Returns
        a dict of lower left corner keys marked with the
        player who captured them."""
        return self.squares

    def __str__(self):
        """Return a nice string representation of the board."""
        buffer = []

        ## do the top line
        for i in range(self.width - 1):
            if ((i, self.height - 1), (i + 1, self.height - 1)) in self.board:
                buffer.append("+--")
            else:
                buffer.append("+  ")
        buffer.append("+\n")

        ## and now do alternating vertical/horizontal passes
        for j in range(self.height - 2, -1, -1):
            ## vertical:
            for i in range(self.width):
                if (((i, j), (i, j + 1))) in self.board:
                    buffer.append("|")
                else:
                    buffer.append(" ")
                if ((i, j)) in self.squares:
                    buffer.append("%s " % self.squares[i, j])
                else:
                    buffer.append("  ")
            buffer.append("\n")

            ## horizontal
            for i in range(self.width - 1):
                if (((i, j), (i + 1, j))) in self.board:
                    buffer.append("+--")
                else:
                    buffer.append("+  ")
            buffer.append("+\n")

        return ''.join(buffer)

    def _makeMove(self, coord1, coord2):
        """Return a new "move", and ensure it's in canonical form.
        (That is, force it so that it's an ordered tuple of tuples.)
        """
        ## TODO: do the Flyweight thing here to reduce object creation
        xdelta, ydelta = coord2[0] - coord1[0], coord2[1] - coord1[1]
        assert ((abs(xdelta) == 1 and abs(ydelta) == 0) or
                (abs(xdelta) == 0 and abs(ydelta) == 1)), \
            "Bad coordinates, not adjacent points."
        if coord1 < coord2:
            return (coord1, coord2)
        else:
            return (tuple(coord2), tuple(coord1))

    def _isGoodCoord(self, coord):
        """Returns true if the given coordinate is good.

        A coordinate is "good" if it's within the boundaries of the
        game board, and if the coordinates are integers."""
        return (isinstance(coord[0], int)
                and isinstance(coord[1], int)
                and 0 <= coord[0] < self.width
                and 0 <= coord[1] < self.height)
        # return (0 <= coord[0] < self.width
        # and 0 <= coord[1] < self.height
        # and isinstance(coord[0], int)
        # and isinstance(coord[1], int))


def _test(width, height, p1, p2):
    """A small driver to make sure that the board works.  It's not
    safe to use this test function in production, because it uses
    input()."""
    board = GameBoard(width, height)
    strategies = (p1, p2)
    p1.initialize(game.initial, initialTime, 0)
    p2.initialize(game.initial, initialTime, 1)
    turn = 1
    scores = [0, 0]
    while not board.isGameOver():
        player = board.getPlayer()
        print("Turn %d (Player %s)" % (turn, player))
        print(board)
        move = input("Move? ")
        squares_completed = board.play(move)
        if squares_completed:
            print("Square completed.")
            scores[player] += len(squares_completed)
        turn = turn + 1
        print("\n")
    print("Game over!")
    print("Final board position:")
    print(board)
    print()
    print("Final score:\n\tPlayer 0: %s\n\tPlayer 1: %s" %
          (scores[0], scores[1]))

# ______________________________________________________________________________
# Players for Games

def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    return num_or_str(input('Your move? '))


def random_player(game, state):
    "A player that chooses a legal move at random."
    # Added state argument to legal_moves AJG 8/9/04
    return random.choice(game.legal_moves(state))


def alphabeta_player(game, state):
    return alphabeta_search(state, game)


def alphabeta_full_player(game, state):
    return alphabeta_full_search(state, game)


def alphabeta_depth1_player(game, state):
    return alphabeta_search(state, game, 1)

class game_player:
    def __init__(self, name):
        self.name = name

    def initialize(self, boardstate, totalTime, color):
        print("Initializing", self.name)
        # self.mycolor = color

        pass;

    def calculate_utility(self, boardstate):
        return boardstate.count_difference()

    def alphabeta_parameters(self, boardstate, remainingTime):
        # This should return a tuple of (cutoffDepth, cutoffTest, evalFn)
        # where any (or all) of the values can be None, in which case the
        # default values are used:
        #        cutoffDepth default is 4
        #        cutoffTest default is None, which just uses cutoffDepth to
        #            determine whether to cutoff search
        #        evalFn default is None, which uses your boardstate_utility_fn
        #            to evaluate the utility of board states.
        return (2, None, None)


if __name__ == "__main__":
    """If we're provided arguments, try using them as the
    width/height of the game board."""
    import sys

    if len(sys.argv[1:]) == 2:
        _test(int(sys.argv[1]), int(sys.argv[2]),game_player("hi"),game_player("yo"))
    elif len(sys.argv[1:]) == 1:
        _test(int(sys.argv[1]), int(sys.argv[1]),game_player("hi"),game_player("yo"))
    else:
        _test(5, 5,game_player("hi"),game_player("yo"))
