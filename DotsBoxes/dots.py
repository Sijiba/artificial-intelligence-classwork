"""Othello, built on Norvig's Game class

"""

from utils import *
from tkinter import *
import random, re, time

# from myothello import boardstate_utility_fn, alphabeta_parameters

# give names to the internal piece value representations
Outer = 0
Dot = 1
A = 2
B = 3
Line_mark = 4
Empty_line = 5
Empty_blank = 6

W = 7
H = 7

All_Directions = [-11, -10, -9, -1, 1, 9, 10, 11]
BigInitialValue = 1000000

# Constants for graphics
GridSize = 50  # size in pixels of each square on playing board
PieceSize = GridSize - 8  # size in pixels of each playing piece
Offset = 2  # offset in pixels of board from edge of canvas
BoardColor = '#008000'  # color of board - medium green
HiliteColor = '#00a000'  # color of highlighted square - light green
PlayerColors = ('', '#000000', '#ffffff')  # rgb values for black, white
PlayerNames = ('', 'Black', 'White')  # Names of players as displayed to the user
MoveDelay = 1000  # pause 1000 msec (1 sec) between moves
fn_array = [None, None]  # array to hold user-defined functions


def opponent(player):
    """Return the opponent of player or None if player is not valid."""
    if player == A:
        return B
    elif player == B:
        return A
    else:
        return None


# ______________________________________________________________________________
# Minimax Search

def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Fig. 6.4]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -BigInitialValue
        for (a, s) in game.successors(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = BigInitialValue
        for (a, s) in game.successors(state):
            v = min(v, max_value(s))
        return v

    # Body of minimax_decision starts here:
    action, state = argmax(game.successors(state),
                           #                       lambda ((a, s)): min_value(s))
                           lambda a_s: min_value(a_s[1]))
    return action


# ______________________________________________________________________________

def alphabeta_full_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Fig. 6.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -BigInitialValue
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = BigInitialValue
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    action, state = argmax(game.successors(state),
                           #                           lambda ((a, s)): min_value(s, -BigInitialValue, BigInitialValue))
                           lambda a_s: min_value(a_s[1], -BigInitialValue, BigInitialValue))
    return action


count = 0
testing = 0


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    global count
    global testing

    player = game.to_move(state)
    count = 0
    starttime = time.clock()

    def max_value(state, alpha, beta, depth):
        global count, testing
        if testing:
            print("  " * depth, "Max  alpha: ", alpha, " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  " * depth, "Max cutoff returning ", eval_fn(state))
            return eval_fn(state)
        v = -BigInitialValue
        succ = game.successors(state)
        count = count + len(succ)
        if testing:
            print("  " * depth, "maxDepth: ", depth, "Total:", count, "Successors: ", len(game.successors(state)))
        for (a, s) in succ:
            v = max(v, min_value(s, alpha, beta, depth + 1))
            if testing:
                print("  " * depth, "max best value:", v)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        global count
        if testing:
            print("  " * depth, "Min  alpha: ", alpha, " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  " * depth, "Min cutoff returning ", eval_fn(state))
            return eval_fn(state)
        v = BigInitialValue
        succ = game.successors(state)
        count = count + len(succ)
        if testing:
            print("  " * depth, "minDepth: ", depth, "Total:", count, "Successors: ", len(game.successors(state)))
        for (a, s) in succ:
            v = min(v, max_value(s, alpha, beta, depth + 1))
            if testing:
                print("  " * depth, "min best value:", v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, game.current_player))
    action, state = argmax(game.successors(state),
                           #                           lambda ((a, s)): min_value(s, -BigInitialValue, BigInitialValue, 0))
                           lambda a_s: min_value(a_s[1], -BigInitialValue, BigInitialValue, 0))

    stoptime = time.clock()
    elapsed = stoptime - starttime
    print("Final count: ", count, "Time: ", end=",")
    print(" %.2f seconds" % elapsed)
    if count > 0:
        spm = elapsed / count
    else:
        spm = -1
    print(" %.7f seconds per move for player %s, depth %d" % (spm, player, d))
    return action


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


class dots_player:
    def __init__(self, name):
        self.name = name

    def initialize(self, boardstate, totalTime, color):
        print("Initializing", self.name)

        pass;

    def claculate_utility(self, boardstate):
        return boardstate.count_difference()

    def alphabeta_parameters(self, boardstate, remainingTime):
        # modify later if needed
        return (2, None, None)

    def play_dot_and_boxes(game=None, initalTime=1800,
                           player1=dots_player("A"), player2=dots_player("B")):
        state = game.initial
        players = (player1, player2)
        clocks = {player1: initialTime, player2: initialTime}
        player1.initialize(state, initialTime, Black)
        player2.initialize(state, initialTime, White)


class othello_player:
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


def play_game(game, *players):
    "Play an n-person, move-alternating game."
    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.make_move(move, state)
            game.display(state)
            if game.terminal_test(state):
                return game.utility(state, players[0])


def play_othello(game=None, initialTime=1800,
                 player1=othello_player("p1"), player2=othello_player("p2")):
    "Play an 2-person, move-alternating Othello game."
    # This is play_game with stuff added to keep track of time.
    game = game or Othello()
    state = game.initial
    players = (player1, player2)
    # initialize the amount of time for each player.  Units are seconds.
    # 1800 seconds is 30 minutes
    clocks = {player1: initialTime, player2: initialTime}
    player1.initialize(state, initialTime, Black)
    player2.initialize(state, initialTime, White)
    previousPass = 0
    while True:
        for player in players:
            game.current_player = player
            # game.calculate_utility = player.calculate_utility
            params = player.alphabeta_parameters(state, clocks[player])
            startTime = time.clock()
            move = alphabeta_search(state, game, params[0], params[1], params[2])
            endTime = time.clock()
            moveTime = endTime - startTime
            if moveTime > clocks[player]:
                print("Player", player.name, "took too much time and loses.")
                if player is player1:
                    print("Player", player2.name, "WINS")
                else:
                    print("Player", player1.name, "WINS")
                # Should really just return some utility that reflects player losing.
                return state.count_difference()
            else:
                clocks[player] -= moveTime
            if move == None:
                print("Player", player.name, "is passing.")
                # this means the player passes, so remember that
                if previousPass:
                    # game over because both players passed
                    diff = state.count_difference()
                    if state.to_move == Black:
                        if diff > 0:
                            print("Player", player1.name, "WINS")
                        else:
                            print("Player", player2.name, "WINS")
                    else:
                        if diff > 0:
                            print("Player", player2.name, "WINS")
                        else:
                            print("Player", player1.name, "WINS")
                    return state.count_difference()
                else:
                    # remember that this player passed
                    previousPass = 1
            else:
                # No passing, so just make move normally
                previousPass = 0
            state = game.make_move(move, state)
            print("Time remaining player 1:", clocks[player1], "player 2:", clocks[player2])
            game.display(state)
            if game.terminal_test(state):
                return state.count_difference()


# ______________________________________________________________________________
# Some Sample Games

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test. You may
    override display and successors or you can inherit their default
    methods. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        abstract()

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        abstract()

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract()

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        m = [(move, self.make_move(move, state))
             for move in self.legal_moves(state)]
        # print "succ len: ", len(m)
        return m

    #        return [(move, self.make_move(move, state))
    #                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


# ______________________________________________________________________________
# Beginning of Othello classes

class BoardState:
    """Holds one state of the Dots and Boxes board."""

    def __init__(self, to_move=None, utility=None, board=None, moves=None):
        if to_move:  # assume if to_move is not None, then neither are the rest
            self.to_move = to_move
            self._utility = utility
            self._board = board
            self._moves = moves
        else:
            self.create_initial_boardstate()

    def getPlayer(self):
        return self.to_move

    def create_initial_boardstate(self):
        """Create an initial boardstate with the default start state."""
        # b = array.array('b',chr(0) * 100)
        # above makes an array, but this array is uncopyable, making it almost useless
        b = [[0 for x in range(W)] for y in range(H)]

        for i in range(W):
            for j in range(H):

                if i == 0 or j == 0 or i == W or j == H:
                    b[i][j] = Outer
                elif i % 2 == 1 and j % 2 == 1:
                    b[i][j] = Dot
                elif i % 2 == 0 and j % 2 == 0:
                    b[i][j] = Empty_blank
                else:
                    b[i][j] = Empty_line

        self._board = b

        self.to_move = Black  # Black has the first move
        self._moves = self.calculate_legal_moves()

        ##utility based on spaces, change/delete?
        self._utility = self.count_difference()

    def find_bracketing_piece(self, square, player, dir):
        "Return the square number of the bracketing piece."

        if self._board[square] == player:
            return square
        elif self._board[square] == opponent(player):
            return self.find_bracketing_piece(square + dir, player, dir)
        else:
            return None


    def legal_p(self, move):
        "A legal move must be into an empty square and it must flip an opposing piece"
        if self._board[move[0]][move[1]] == Empty_line:
            return True
        else:
            return None

    def legal_moves(self):
        "Return a list of legal moves for player."
        return self._moves

    def getxyMoves(self):
        "Return a list of (x, y) pairs for legal moves."
        moves = []
        for move in self._moves:
            if move != None:
                moves.append(((move // 10) - 1, (move % 10) - 1))
        return tuple(moves)

    def calculate_legal_moves(self):
        """Calculate the legal moves in the current BoardState."""
        moves = []
        for i in range(1, W - 1):
            for j in range(1, H - 1)
                if self.legal_p(i, j):
                    moves.append((i, j))
        # if there are no legal moves, append None (meaning pass)
        if len(moves) == 0:
            moves.append(None)
            # print "appending None to indicate no legal moves"
        return moves

    def make_move(self, move):
        "Return a new BoardState reflecting move made from given board state."
        newboard = BoardState(opponent(self.to_move), None, self._board[:], None)
        if move != None:
            newboard._board[move] = self.to_move
            for dir in All_Directions:
                newboard.make_flips(move, self.to_move, dir)
        newboard._moves = newboard.calculate_legal_moves()
        # utility for the new state is calculated in the game version of
        # this method.  That is kind of an ugly hack, but necessary to make
        # it easier to allow a per-player utility function.
        return newboard

    def getPieces(self):
        "Make a dictionary of (x, y): player for each occupied square of the game."
        pieces = {}
        for row in range(0, H):
            if self._board[row][row] != Outer:
                for col in range(0, W):
                    if self._board[row][col] == A or self._board[row][col] == B:
                        pieces[(row, col)] = self._board[row][col]
                        # print "row", row, "col", col, pieces[(row,col)]
        return pieces

    def count_difference(self):
        "Return count of player's pieces minus opponent's pieces."
        return self._board.count(self.to_move) - self._board.count(opponent(self.to_move))


class Othello(Game):
    """Play Othello on an 8 x * board with Max (first player) playing 'B' (for Black).
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of whatever."""

    def __init__(self):
        self.current_state = BoardState()
        self.initial = self.current_state

    def display(self, boardstate):
        print(' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        for row in range(1, 9):
            print(row, end=" ")
            for col in range(1, 9):
                print({Empty: '.',
                       Black: 'B',
                       White: 'W'}[boardstate._board[col + 10 * row]], end=" ")
            print()
        print()

    def legal_moves(self, boardstate):
        return boardstate.legal_moves()

    def make_move(self, move, boardstate):
        "Return a new BoardState reflecting move made from given board state."
        newBoard = boardstate.make_move(move)
        # This is actually going to call the player's calculate_utility
        # method, because the player's method is hooked up just before
        # alphabeta_search is called.  Ugggggggggly. . .
        # newBoard._utility = self.calculate_utility(newBoard)
        return newBoard

    def terminal_test(self, boardstate):
        return len(boardstate._moves) == 0

    def calculate_utility(self, boardstate):
        return boardstate.count_difference()

    def utility(self, boardstate, player):
        return player.calculate_utility(boardstate)


class Dots(Game):
    """Play Dots and Boxes"""

    def __init__(self):
        self.current_state = BoardState()
        self.initial = self.current_state

    def display(self, boardstate):
        print(' ', ' ', 'a', ' ', 'b', ' ', 'c', ' ', 'd', ' ', 'e')
        for row in range(1, 10):
            print({Dot: '\u00b7',
                   A = 'A',
                       B = 'B',
                           Line_h = '-',
                                    Line_v = '|',
                                             Empty_l = ' ',
                                                       Empty_b = ' '}[boardstate._board[col + 10 * row]], end = " ")
            print()
        print()


def legal_moves(self, boardstate):
    return boardstate.legal_moves()


def make_move(self, move, boardstate):
    newBoard = boardstate.make_move(move)
    return newBoard


def terminal_test(self, boardstate):
    return len(boardstate._moves) == 0


def calculate_utility(self, boardstate):
    return boardstate.count_difference()


def utility(self, boardstate, player):
    return player.calculate_utility(boardstate)


# return boardstate._utility
##        if boardstate.to_move == player:
##            return boardstate._utility
##        else:
##            return -boardstate._utility


class Board:
    "Holds the Tk GUI and the current board state"

    class Square:
        "Holds data related to a square of the board"

        def __init__(self, x, y):
            self.x, self.y = x, y  # location of square (in range 0-7)
            self.ref = (x * 10) + y + 11  # location of square in internal board representation
            self.player = 0  # number of player occupying square
            self.squareId = 0  # canvas id of rectangle
            self.pieceId = 0  # canvas id of circle

    def __init__(self, game, strategies=(), initialTime=1800):
        '''Initialize the interactive game board.  An optional list of
           computer opponent strategies can be supplied which will be
           displayed in a menu to the user.
        '''

        self.game = game
        self.initialTime = initialTime
        self.passedTest = ''
        # create a Tk frame to hold the gui
        self._frame = Frame()
        # set the window title
        self._frame.master.wm_title('Pythello')
        # build the board on a Tk drawing canvas
        size = 8 * GridSize  # make room for 8x8 squares
        self._canvas = Canvas(self._frame, width=size, height=size)
        self._canvas.pack()
        # add button for starting game
        self._menuFrame = Frame(self._frame)
        self._menuFrame.pack(expand=Y, fill=X)
        self._newGameButton = Button(self._menuFrame, text='New Game', command=self._newGame)
        self._newGameButton.pack(side=LEFT, padx=5)
        Label(self._menuFrame).pack(side=LEFT, expand=Y, fill=X)
        # add menus for choosing player strategies
        self._strategies = {}  # strategies, indexed by name
        optionMenuArgs = [self._menuFrame, 0, 'Human']
        for s in strategies:
            name = s.name
            optionMenuArgs.append(name)
            self._strategies[name] = s
        self._strategyVars = [0]  # dummy entry so strategy indexes match player numbers
        # make an menu for each player
        for n in (1, 2):
            label = Label(self._menuFrame, anchor=E, text='%s:' % PlayerNames[n])
            label.pack(side=LEFT, padx=10)
            var = StringVar();
            var.set('Human')
            var.trace('w', self._strategyMenuCallback)
            self._strategyVars.append(var)
            optionMenuArgs[1] = var
            #            menu = apply(OptionMenu, optionMenuArgs)
            menu = OptionMenu(*optionMenuArgs)
            menu.pack(side=LEFT)
        # add a label for showing the status
        self._status = Label(self._frame, relief=SUNKEN, anchor=W)
        self._status.pack(expand=Y, fill=X)
        # map the frame in the main Tk window
        self._frame.pack()

        # track the board state
        self._squares = {}  # Squares indexed by (x,y)
        self._enabledSpaces = ()  # list of valid moves as returned by BoardState.getmoves()
        for x in range(8):
            for y in range(8):
                square = self._squares[x, y] = Board.Square(x, y)
                x0 = x * GridSize + Offset
                y0 = y * GridSize + Offset
                square.squareId = self._canvas.create_rectangle(x0, y0,
                                                                x0 + GridSize, y0 + GridSize,
                                                                fill=BoardColor)

        # _afterId tracks the current 'after' proc so it can be cancelled if needed
        self._afterId = 0

        # ready to go - start a new game!
        self._newGame()

    def play(self):
        'Play the game! (this is the only public method)'
        self._frame.mainloop()

    def _postStatus(self, text):
        # updates the status line text
        self._status['text'] = text

    def _strategyMenuCallback(self, *args):
        # this is called when one of the player strategies is changed.
        # _updateBoard will keep everything in sync
        p1 = self._strategies.get(self._strategyVars[1].get())
        p2 = self._strategies.get(self._strategyVars[2].get())

        self.clocks = {p1: self.initialTime, p2: self.initialTime}
        self._updateBoard()

    def _newGame(self):
        # delete existing pieces
        for s in self._squares.values():
            if s.pieceId:
                self._canvas.delete(s.pieceId)
                s.pieceId = 0
        # create a new board state and display it
        self._state = BoardState()

        # get the players to make it easier to reset the clocks
        p1 = self._strategies.get(self._strategyVars[1].get())
        p2 = self._strategies.get(self._strategyVars[2].get())
        # reset the timing clocks
        self.clocks = {p1: self.initialTime, p2: self.initialTime}

        self._updateBoard()

    def _updateBoard(self):
        # cancel 'after' proc, if any
        if self._afterId:
            self._frame.after_cancel(self._afterId)
            self._afterId = 0
        # reset any enabled spaces
        self._disableSpaces()
        # update canvas display to match current state
        for pos, player in self._state.getPieces().items():
            square = self._squares[pos]
            if square.pieceId:
                if square.player != player:
                    self._canvas.itemconfigure(square.pieceId, fill=PlayerColors[player])
            else:
                x, y = pos
                x0 = x * GridSize + Offset + 4
                y0 = y * GridSize + Offset + 4
                square.pieceId = self._canvas.create_oval(x0, y0,
                                                          x0 + PieceSize, y0 + PieceSize,
                                                          fill=PlayerColors[player])
        # prepare for next move, either human or ai
        player = self._state.getPlayer()
        moves = self._state.legal_moves()
        # check for game over
        if not moves:
            self._gameOver()
            return
        # check for a pass
        if len(moves) == 1 and moves[0] == None:
            # fix this later. . .
            # must pass - do it now
            ##            self._state = moves[0][2]
            ##            moves = self._state.getMoves()
            ##            if not moves:
            ##                self._gameOver()
            ##                return
            ##            # prepend status message with passed message
            # if we passed on the previous move too
            if self.passedText:
                self._gameOver()
                return
            self.passedText = PlayerNames[player] + ' must pass - '
            # update player
            player = self._state.getPlayer()
        else:
            # player can't pass
            self.passedText = ''

        # get strategy (if not human)
        ai = self._strategies.get(self._strategyVars[player].get())
        if ai:
            # ai: we have to schedule the ai to run
            self._postStatus(self.passedText + "%s (%s) (%s time left) is thinking" % \
                             (ai.name, PlayerNames[player], self.clocks[ai]))
            self._afterId = self._frame.after_idle(self._processAi, ai, moves)
        else:
            # human: just enable legal moves and wait for a click
            self._postStatus(self.passedText + PlayerNames[player] + "'s turn")
            self._enabledSpaces = self._state.getxyMoves()
            self._enableSpaces()

    def _processAi(self, ai, moves):
        # calls the strategy to determine next move
        if len(moves) == 1:
            # only one choice, don't both calling strategy
            self._state = self._state.make_move(moves[0])
        else:
            # self.game.calculate_utility = ai.calculate_utility
            # update the current_player as each player considers their move
            self.game.current_player = ai
            params = ai.alphabeta_parameters(self._state, self.clocks[ai])
            startTime = time.clock()
            move = alphabeta_search(self._state, self.game, params[0], params[1], params[2])
            endTime = time.clock()
            moveTime = endTime - startTime
            if moveTime > self.clocks[ai]:
                print("Player", ai.name, "took too much time and loses.")
                self._gameOver()
                return
            else:
                self.clocks[ai] -= moveTime

            # call strategy
            # move = ai(self.game, self._state)
            # x,y,boardstate = ai.getNextMove(self._state.getPlayer(), moves)
            self._state = self._state.make_move(move)
        self._afterId = self._frame.after(MoveDelay, self._updateBoard)

    def _enableSpaces(self):
        # make spaces active where a legal move is possible (only used for human players)
        for x, y in self._enabledSpaces:
            if x == -1: break
            id = self._squares[x, y].squareId
            self._canvas.tag_bind(id, '<ButtonPress>',
                                  lambda e, s=self, x=x, y=y: s._selectSpace(x, y))
            self._canvas.tag_bind(id, '<Enter>',
                                  lambda e, c=self._canvas, id=id: \
                                      c.itemconfigure(id, fill=HiliteColor))
            self._canvas.tag_bind(id, '<Leave>',
                                  lambda e, c=self._canvas, id=id: \
                                      c.itemconfigure(id, fill=BoardColor))

    def _disableSpaces(self):
        # remove event handlers for all enabled spaces
        for x, y in self._enabledSpaces:
            if x == -1: break
            id = self._squares[x, y].squareId
            self._canvas.tag_unbind(id, '<ButtonPress>')
            self._canvas.tag_unbind(id, '<Enter>')
            self._canvas.tag_unbind(id, '<Leave>')
            self._canvas.itemconfigure(id, fill=BoardColor)
        self._enabledSpaces = ()

    def _selectSpace(self, x, y):
        # this is called when a human clicks on a space to place a piece
        self._state = self._state.make_move(x * 10 + y + 11)
        self._updateBoard()

    def _gameOver(self):
        # the game is over.  Count up the pieces and declare the winner.
        count = [0, 0, 0]  # first entry is a dummy
        for player in self._state.getPieces().values():
            count[player] = count[player] + 1
        self._postStatus('Game Over,  %s: %d  -  %s: %d' % \
                         (PlayerNames[1], count[1], PlayerNames[2], count[2]))


def start_graphical_othello_game(p1, p2, initialTime=1800):
    strategies = (p1, p2)
    game = Othello()
    p1.initialize(game.initial, initialTime, Black)
    p2.initialize(game.initial, initialTime, White)
    board = Board(game, strategies, initialTime)
    # board.initialTime = initialTime
    board.play()

    ## To start a graphical game type:
    ##   start_graphical_othello_game(othello_player("Bob"), othello_player("Fred"))
    ## where othello_player can be replaced by MyPlayer or whatever you choose to
    ## call your class.

    ## To start a textual game (where you can have different AI players) type:
    ##  play_othello() will just start a default game,
    ##  play_othello(Othello(), 1800, MyPlayer("Name"), othello_player("Othername"))
    ## where MyPlayer is your class (which can have whatever name you want)
    ## and othello_player is just the dumb default.  You can have BobPlayer play
    ## FredPlayer if you define those two classes, for example.