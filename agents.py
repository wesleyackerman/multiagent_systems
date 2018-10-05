import random

# Each agent should have an "act" function that uses their state to choose an action. Agents can use "update_state" to update
# their state with past actions. E.G. tit-for-two-tats would store a length-2 list of the past 2 actions their opponent has performed.
# That list will then be used in "act" to decide what to do.
#
# Any agent that stores state should clear it in "clear_state" so that it doesn't try to act based on actions from a previous game.
#
class Agent:
    def __init__(self, action_list):
	self.actions = action_list
	self.score = 0

    def act(self):
	# Every inheritor of Agent class should have their own action function
	raise NotImplementedError()

    def update_state(self, my_action, their_action):
	# inheritors may not need this if they don't keep track of state (like "always defect"). Both "my" and "their" actions are passed, in case either/both are needed 
	pass

    def clear_state(self):
	# This will be called when a game against a single opponent has been completed. Any state the agent has should be cleared in preparation for a new game.
	pass

    def __str__(self):
	return str(self.__class__) + ":" + str(self.score) 

class RandomAgent(Agent):
    def act(self):
	return random.choice(self.actions)
