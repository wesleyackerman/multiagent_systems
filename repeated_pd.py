from numpy.random import choice
from agents import RandomAgent

class GamesRunner:
    def __init__(self):
	self.actions = ["C", "D"]
	self.agents = [RandomAgent(self.actions), RandomAgent(self.actions), RandomAgent(self.actions), RandomAgent(self.actions)]
	self.n_rounds = 5 # if greater than or equal to 1, play that many rounds. If between 0 and 1, after each round have that probability of playing another
	self.n_games_played = 0
	self.total_rounds_played = 0
	self.n_agents = len(self.agents)
	self.verbose = False # Debugging printouts	

	# Payoff values specific to prisoner's dilemma
	self.R = 3
	self.T = 5
	self.S = 1
	self.P = 2

    def run(self):
	for i in range(self.n_agents):
	    if self.verbose: print("~~~~~~~~~~~~~~~~\n" + "Agent" + str(i) + "\n~~~~~~~~~~~~~~~~")
	    # Each agent should only play each opponent once, so iterate with each agent playing all agents that come AFTER them in the list
	    agent0 = self.agents[i]
	    n_opponents = self.n_agents - 1 - i
	    for j in range(n_opponents):
		opp_idx = i + j + 1
		assert(opp_idx > i)
		if self.verbose: print("Agent" + str(opp_idx))
		agent1 = self.agents[opp_idx]
		self.play_game(agent0, agent1)
	
	if self.verbose: print("Total rounds played: " + str(self.total_rounds_played))
	print("Games played: " + str(self.n_games_played))
	for agent in self.agents:
            print(agent)
    
    def play_game(self, agent0, agent1):
	if self.verbose: print("Playing game...")

        if self.n_rounds >= 1:
	    # play n rounds
	    for i in range(self.n_rounds):
		self.play_and_score(agent0, agent1)
	else:
	    # probability n of playing next round. Keep looping until "cont" is False
	    while True:
		self.play_and_score(agent0, agent1)
	        cont = choice([True, False], p=[self.n_rounds, 1-self.n_rounds])
	        if not cont:
		    break 

	self.n_games_played += 1
	agent0.clear_state()
	agent1.clear_state()

    def play_and_score(self, agent0, agent1):
	if self.verbose: print("Playing round...")
	self.total_rounds_played += 1
	payoff0, payoff1 = self.prisoners_dilemma(agent0, agent1)
        agent0.score += payoff0
        agent1.score += payoff1

    def prisoners_dilemma(self, agent0, agent1):
	a0 = agent0.act()
	a1 = agent1.act()
	payoff0 = -1
	payoff1 = -1

	if self.verbose: print(a0 + "," + a1)	

	agent0.update_state(a0, a1)
	agent1.update_state(a1, a0)

	if a0 == "C":
	    if a1 == "C":
		payoff0, payoff1 = self.R, self.R
	    elif a1 == "D":
		payoff0, payoff1 = self.S, self.T
	elif a0 == "D":
	    if a1 == "C":
		payoff0, payoff1 = self.T, self.S
	    elif a1 == "D":
		payoff0, payoff1 = self.P, self.P

	if payoff0 == -1 or payoff1 == -1:
 	    raise InvalidActionError("Action wasn't C or D")
	
	if self.verbose: print("Payoffs:" + str(payoff0) + "," + str(payoff1))
	return payoff0, payoff1

class InvalidActionError(BaseException):
    def __init__(self, value):
	self.value = value
    def __str__(self):
	return repr(self.value)

if __name__ == '__main__':
    gr = GamesRunner()
    gr.run()

 




