# This function solves the 8 puzzle.

#              Node Expansions
# Problem   BFS     A*(tiles)   A*(dist)
# A         7       3           3
# B         91      8           7
# C         156     19          10
# D         690     48          30
# E         856     48          30
# F         1621    102         21
# G         8361    337         56
# H         50312   3529        208

from informedSearch import *
import copy


class EightState(InformedProblemState):
    """
    The 8 puzzle: 8 tiles from 0 - 9. 0 can be moved up, down, left, or
    right by swapping it with the tile adjacent.

    Each operator returns a new instance of this class representing
    the successor state.
    """

    def __init__(self, ul, um, ur, ml, mm, mr, ll, lm, lr):
        # values represent people on left of river
        self.grid = [[ul, um, ur],
                     [ml, mm, mr],
                     [ll, lm, lr]]

    @classmethod
    def from_grid(cls, grid):
        return cls(grid[0][0], grid[0][1], grid[0][2],
                   grid[1][0], grid[1][1], grid[1][2],
                   grid[2][0], grid[2][1], grid[2][2])

    def __str__(self):
        """
        Required method for use with the Search class.
        Returns a string representation of the state.
        """
        return "(" + str(self.grid[0]) + "," + str(self.grid[1]) + "," + str(self.grid[2]) + ")"

    def illegal(self):
        """
        Required method for use with the Search class.
        Tests whether the state is illegal.
        """
        for row in self.grid:
            for value in row:
                if value is None:
                    return 1

        return 0

    def equals(self, state):
        """
        Required method for use with the Search class.
        Determines whether the state instance and the given
        state are equal.
        """
        return self.grid == state.grid

    def heuristic(self, goal):
        """
        For use with informed search.  Returns the estimated
        cost of reaching the goal from this state.
        """
        value = 0
        heuristicnum = 2
        if heuristicnum == 1:
            # Return number of tiles not matching goal state
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] is None:
                        value = value + 9999
                    elif self.grid[row][col] != goal.grid[row][col]:
                        value = value + 1
            return value
        if heuristicnum == 2:
            # return sum of manhattan distances from each tile to its goal
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] is None:
                        value = value + 9999
                    elif self.grid[row][col] != goal.grid[row][col]:
                        goalplace = self.find_value(goal.grid, self.grid[row][col])
                        value = value + abs(row - goalplace[0]) + abs(col - goalplace[1])
            return value
        return 0

    @staticmethod
    def find_value(grid, val):
        row = 0
        while row < len(grid):
            column = 0
            while column < len(grid[row]):
                if val == grid[row][column]:
                    return [row, column]
                column = column + 1
            row = row + 1

        return [-1, -1]

    def move0up(self):
        grid = copy.deepcopy(self.grid)
        place = self.find_value(grid, 0)
        if place[0] == 0:
            grid[place[0]][place[1]] = None
            return EightState.from_grid(grid)
        elif place[0] > 0:
            temp = grid[place[0]][place[1]]
            grid[place[0]][place[1]] = grid[place[0] - 1][place[1]]
            grid[place[0] - 1][place[1]] = temp
            return EightState.from_grid(grid)
        return EightState.from_grid(self.grid)

    def move0down(self):
        grid = copy.deepcopy(self.grid)
        place = self.find_value(grid, 0)
        if place[0] == len(grid) - 1:
            grid[place[0]][place[1]] = None
            return EightState.from_grid(grid)
        elif place[0] >= 0:
            temp = grid[place[0]][place[1]]
            grid[place[0]][place[1]] = grid[place[0] + 1][place[1]]
            grid[place[0] + 1][place[1]] = temp
            return EightState.from_grid(grid)
        return EightState.from_grid(self.grid)

    def move0left(self):
        grid = copy.deepcopy(self.grid)
        place = self.find_value(grid, 0)
        if place[1] == 0:
            grid[place[0]][place[1]] = None
            return EightState.from_grid(grid)
        elif place[1] > 0:
            temp = grid[place[0]][place[1]]
            grid[place[0]][place[1]] = grid[place[0]][place[1] - 1]
            grid[place[0]][place[1] - 1] = temp
            return EightState.from_grid(grid)
        return EightState.from_grid(self.grid)

    def move0right(self):
        grid = copy.deepcopy(self.grid)
        place = self.find_value(grid, 0)
        if place[1] == len(grid[place[0]]) - 1:
            grid[place[0]][place[1]] = None
            return EightState.from_grid(grid)
        elif place[1] >= 0:
            temp = grid[place[0]][place[1]]
            grid[place[0]][place[1]] = grid[place[0]][place[1] + 1]
            grid[place[0]][place[1] + 1] = temp
            return EightState.from_grid(grid)
        return EightState.from_grid(self.grid)

    def operatorNames(self):
        """
        Required method for use with the Search class.
        Returns a list of the operator names in the
        same order as the applyOperators method.
        """
        return ["move0up", "move0down", "move0left", "move0right"]

    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of possible successors to the current
        state, some of which may be illegal.
        """
        return [self.move0up(), self.move0down(),
                self.move0left(), self.move0right()]


print("Problem A")
InformedSearch(EightState(1, 3, 0, 8, 2, 4, 7, 6, 5), EightState(1, 2, 3, 8, 0, 4, 7, 6, 5))

print("Problem B")
InformedSearch(EightState(1, 3, 4, 8, 6, 2, 0, 7, 5), EightState(1, 2, 3, 8, 0, 4, 7, 6, 5))

print("Problem C")
InformedSearch(EightState(0, 1, 3, 4, 2, 5, 8, 7, 6), EightState(1, 2, 3, 8, 0, 4, 7, 6, 5))

print("Problem D")
InformedSearch(EightState(7, 1, 2, 8, 0, 3, 6, 5, 4), EightState(1, 2, 3, 8, 0, 4, 7, 6, 5))

print("Problem E")
InformedSearch(EightState(8, 1, 2, 7, 0, 4, 6, 5, 3), EightState(1, 2, 3, 8, 0, 4, 7, 6, 5))

print("Problem F")
InformedSearch(EightState(2, 6, 3, 4, 0, 5, 1, 8, 7), EightState(1, 2, 3, 8, 0, 4, 7, 6, 5))

print("Problem G")
InformedSearch(EightState(7, 3, 4, 6, 1, 5, 8, 0, 2), EightState(1, 2, 3, 8, 0, 4, 7, 6, 5))

print("Problem H")
InformedSearch(EightState(7, 4, 5, 6, 0, 3, 8, 1, 2), EightState(1, 2, 3, 8, 0, 4, 7, 6, 5))
