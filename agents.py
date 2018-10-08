import random

# Each agent should have an "act" function that uses their state to choose an action. Agents can use "update_state" to update
# their state with past actions. E.G. tit-for-two-tats would store a length-2 list of the past 2 actions their opponent has performed.
# That list will then be used in "act" to decide what to do.
#
# Any agent that stores state should clear it in "clear_state" so that it doesn't try to act based on actions from a previous game.
#

"""
An agent who employs the one-shot equilibrium solution (always defect)
An agent who chooses randomly
An agent who always cooperates with you (and never confesses)
An agent who employs the tit-for-tat strategy (reviewed below), and
An agent who employs the tit-for-two-tats strategy (also reviewed below).
An agent who uses the Pavlov strategy (reviewed below).
An agent who uses the Win-Stay/Lose-Shift strategy (reviewed below).
An agent who uses the Never Forgive strategy (reviewed below).
"""

class Agent:
    def __init__(self, action_list):
        self.actions = action_list
        self.score = 0
        self.state = None
        self.current_action = None

    def act(self):
        # Every inheritor of Agent class should have their own action function
        raise NotImplementedError()

    def update_state(self, my_action, their_action, payoff):
        # inheritors may not need this if they don't keep track of state (like "always defect"). Both "my" and "their" actions are passed, in case either/both are needed 
        # pass current payoff (needed for win/lose shift
        pass

    def clear_state(self):
        # This will be called when a game against a single opponent has been completed. Any state the agent has should be cleared in preparation for a new game.
        pass

    def __str__(self):
        return str(self.__class__) + ":" + str(self.score) 

class RandomAgent(Agent):
    def act(self):
        return random.choice(self.actions)

class AlwaysDefect(Agent):
    def act(self):
        return "D"

class AlwaysCooperate(Agent):
    def act(self):
        return "C"

class NeverForgive(Agent):
    def __init__(self, action_list):
        super().__init__(action_list)
        self.clear_state()

    def clear_state(self):
        self.current_action = "C"

    def update_state(self, my_action, their_action, payoff):
        if their_action == "D":
            self.current_action = "D"

    def act(self):
        return self.current_action

class TitForTat(Agent):
    def __init__(self, action_list):
        super().__init__(action_list)
        self.clear_state()

    def clear_state(self):
        self.current_action = "C"

    def update_state(self, my_action, their_action, payoff):
        self.current_action = their_action

    def act(self):
        return self.current_action

class TitFor2Tat(Agent):
    """
    The tit-for-two-tats strategy is similar, except that P2 only defects if the other agent defects twice in a row, but cooperates immediately after the other agent cooperates.
    """

    def __init__(self, action_list):
        super().__init__(action_list)
        self.clear_state()

    def clear_state(self):
        self.state = []
        self.current_action = "C"

    def update_state(self, my_action, their_action, payoff):
        if their_action == "C":
            self.state = []
            self.current_action = "C"
        elif their_action == "D":
            if not self.state:
                self.state=["D"]
            else:
                self.state = ["D","D"]
                self.current_action = "D"

    def act(self):
        return self.current_action


class Pavlov(Agent):
    """ Defect if exactly one person defected last time
    """

    def __init__(self, action_list):
        super().__init__(action_list)
        self.clear_state()

    def clear_state(self):
        self.current_action = "C"
        self.state = None

    def update_state(self, my_action, their_action, payoff):
        if my_action != their_action:
            self.current_action = "D"
        else:
            self.current_action = "C"

    def act(self):
        return self.current_action

class WinStayLoseShift(Agent):
    """ The WinStay/LoseShift (WSLS) strategy begins by cooperating, but then changes its behavior (C goes to D or D goes to C) whenever the agent doesn't win.
    Winning occurs whenever the agent gets either its most preferred or next most preferred result.
    """
    def __init__(self, action_list):
        super().__init__(action_list)
        self.best_payoffs = [5,3]
        self.clear_state()

    def clear_state(self):
        self.current_action = "C"

    def update_state(self, my_action, their_action, payoff):
        if payoff in self.best_payoffs:
            self.current_action = my_action
        else:
            # switch to other action
            self.current_action = "D" if my_action == "C" else "C"

    def act(self):
        return self.current_action

class Alternater(Agent):
    """ Alternate C and D. Frequency specifies how often to switch.
    """

    def __init__(self, action_list, freq=1):
        super().__init__(action_list)
        self.freq = freq
        self.clear_state()

    def clear_state(self):
        self.state = ["C"]
        self.current_action = "C"

    def update_state(self, my_action, their_action, payoff):
        if self.state == ["C"]*self.freq:
            self.state = ["D"]
            self.current_action = "D"
        elif self.state == ["D"]*self.freq:
            self.state = ["C"]
            self.current_action = "C"
        else:
            self.state.append(self.current_action)

    def act(self):
        return self.current_action