# File missionary.py
# Implements the missionary and cannibal puzzle for state space search

from search import *


class MissionaryState(ProblemState):
    """
    The missionaries and cannibals puzzle: Suppose that you are given 3
    missionaries and 3 cannibals. A boat can send 1 or 2 people to the other
    side of a river, so long as groups of ministers aren't outnumbered by groups
    of cannibals.

    Each operator returns a new instance of this class representing
    the successor state.  
    """

    def __init__(self, mini, cann, boatonleft):
        # values represent people on left of river
        self.mini = mini
        self.cann = cann
        self.boatonleft = boatonleft

    def __str__(self):
        """
        Required method for use with the Search class.
        Returns a string representation of the state.
        """
        return "(" + str(self.mini) + "," + str(self.cann) + "," + str(self.boatonleft) + ")"

    def illegal(self):
        """
        Required method for use with the Search class.
        Tests whether the state is illegal.
        """
        if self.mini < 0 or self.cann < 0:
            return 1
        if self.mini > 3 or self.cann > 3:
            return 1
        if self.mini == 1 and self.cann != 1:
            return 1
        if self.mini == 2 and self.cann != 2:
            return 1

        return 0

    def equals(self, state):
        """
        Required method for use with the Search class.
        Determines whether the state instance and the given
        state are equal.
        """
        return self.mini == state.mini and self.cann == state.cann and self.boatonleft == state.boatonleft

    def move2min(self):
        if self.boatonleft:
            return MissionaryState(self.mini - 2, self.cann, False)
        else:
            return MissionaryState(self.mini + 2, self.cann, True)

    def move1min(self):
        if self.boatonleft:
            return MissionaryState(self.mini - 1, self.cann, False)
        else:
            return MissionaryState(self.mini + 1, self.cann, True)

    def move2can(self):
        if self.boatonleft:
            return MissionaryState(self.mini, self.cann - 2, False)
        else:
            return MissionaryState(self.mini, self.cann + 2, True)

    def move1can(self):
        if self.boatonleft:
            return MissionaryState(self.mini, self.cann - 1, False)
        else:
            return MissionaryState(self.mini, self.cann + 1, True)

    def move1each(self):
        if self.boatonleft:
            return MissionaryState(self.mini - 1, self.cann - 1, False)
        else:
            return MissionaryState(self.mini + 1, self.cann + 1, True)

    def operatorNames(self):
        """
        Required method for use with the Search class.
        Returns a list of the operator names in the
        same order as the applyOperators method.
        """
        return ["move2min", "move1min", "move2can", "move1can",
                "move1each"]

    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of possible successors to the current
        state, some of which may be illegal.  
        """
        return [self.move2min(), self.move1min(),
                self.move2can(), self.move1can(),
                self.move1each()]


Search(MissionaryState(3, 3, True), MissionaryState(0, 0, False))
