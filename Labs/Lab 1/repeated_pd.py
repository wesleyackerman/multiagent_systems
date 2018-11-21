from numpy.random import choice
from agents import *
import copy
import numpy as np

class GamesRunner:
    def __init__(self, agents=None, verbose=False, n_rounds=5, play_self=False, n_cycles=10):
        self.actions = ["C", "D"]
        self.n_cycles = n_cycles

        if agents is None:
            # RandomAgent(self.actions)
            self.agents = [AlwaysDefect(self.actions),
                           RandomAgent(self.actions),
                           AlwaysCooperate(self.actions),
                           TitForTat(self.actions),
                           TitFor2Tat(self.actions),
                           Pavlov(self.actions),
                           WinStayLoseShift(self.actions),
                           NeverForgive(self.actions)]
        else:
            self.agents = agents

        self.n_rounds = n_rounds # if greater than or equal to 1, play that many rounds. If between 0 and 1, after each round have that probability of playing another
        self.n_games_played = 0
        self.total_rounds_played = 0
        self.n_agents = len(self.agents)
        self.verbose = verbose # Debugging printouts
        self.play_self = play_self
        self.scoreboard = np.zeros((self.n_agents, 2))	

        # Payoff values specific to prisoner's dilemma
        self.R = 3
        self.T = 5
        self.S = 1
        self.P = 2

    def run(self):
        for i in range(self.n_cycles):
            self.play_cycle()

        if self.verbose: print("Total rounds played: " + str(self.total_rounds_played))
        print("Games played: " + str(self.n_games_played))
        for agent in self.agents:
            print(agent)
            print("   Avg Rounds per cycle: {}".format(agent.rounds_played / self.n_cycles))
            print("   Avg Score: {0:.2f}".format(agent.score/agent.rounds_played))
        
        self.scoreboard /= self.n_cycles
        #if self.n_rounds > 1:
            #self.scoreboard /= self.n_rounds
        self.print_scoreboard()
        #print(self.scoreboard / self.n_cycles)
        return self.results

    def play_cycle(self):
        self.results = {}
        # Loop through all agents
        for i in range(self.n_agents):
            if self.verbose: print("~~~~~~~~~~~~~~~~\n" + "Agent" + str(i) + "\n~~~~~~~~~~~~~~~~")
            # Each agent should only play each opponent once, so iterate with each agent playing all agents that come AFTER them in the list
            agent0 = self.agents[i]

            # play_self_offset = 1 if not self.play_self else 0
            n_opponents = self.n_agents - i - 1

            # Play each opponent
            for j in range(n_opponents):
                opp_idx = i + j + 1
                assert(opp_idx > i )
                if self.verbose: print("Agent" + str(opp_idx))
                agent1 = self.agents[opp_idx]
                scores, result = self.play_game(agent0, agent1)
                self.results["{}:{}".format(i,j)] = result

		# if super agent is being played
                if agent1.agent_type() == "SuperAgent":
                    self.scoreboard[i] += np.array(scores)

            if self.play_self:
                agent1 = copy.deepcopy(agent0)
                scores, result = self.play_game(agent0, agent1)
                self.results["{}:{}".format(i,i)] = result
                if agent0.agent_type() == "SuperAgent":
                    self.scoreboard[i] += np.array(scores)

        #if self.verbose: print("Total rounds played: " + str(self.total_rounds_played))
        #print("Games played: " + str(self.n_games_played))
        #for agent in self.agents:
        #    print(agent)
        #    print("   Rounds: {}".format(agent.rounds_played))
        #    print("   Avg Score: {0:.2f}".format(agent.score/agent.rounds_played))
        #return self.results

    def play_game(self, agent0, agent1):
        a0_score = 0
        a1_score = 0
        round_count = self.n_rounds // 1.0
        if self.verbose: print("Playing game...")

        results = []
        if self.n_rounds >= 1:
            # play n rounds
            for i in range(self.n_rounds):
                a0, a1, result = self.play_and_score(agent0, agent1)
                a0_score += a0
                a1_score += a1
                results.append(result)
        else:
            # probability n of playing next round. Keep looping until "cont" is False
            while True:
                round_count += 1
                a0, a1, result = self.play_and_score(agent0, agent1)
                a0_score += a0
                a1_score += a1
                results.append(result)
                cont = choice([True, False], p=[self.n_rounds, 1-self.n_rounds])
                if not cont:
                    break 

        self.n_games_played += 1
        agent0.clear_state()
        agent1.clear_state()

        return (a0_score / round_count, a1_score / round_count), results

    def play_and_score(self, agent0, agent1):
        if self.verbose: print("Playing round...")
        self.total_rounds_played += 1
        payoff0, payoff1, result = self.prisoners_dilemma(agent0, agent1)
        agent0.score += payoff0
        agent1.score += payoff1
        agent0.rounds_played += 1
        agent1.rounds_played += 1

        return payoff0, payoff1, result

    def prisoners_dilemma(self, agent0, agent1):
        a0 = agent0.act()
        a1 = agent1.act()
        payoff0 = -1
        payoff1 = -1

        if self.verbose: print("Moves played: {},{}".format(a0,a1))

        # Calculate Payoffs
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

        if -1 in [payoff0, payoff1]:
             raise InvalidActionError("Action wasn't C or D")

        # Update Strategies (after payoff eval) - need this for WinStayLossShift and SuperAgent
        agent0.update_state(a0, a1, payoff0, payoff1)
        agent1.update_state(a1, a0, payoff1, payoff0)


        if self.verbose: print("Payoffs:" + str(payoff0) + "," + str(payoff1))
        result = a0+a1
        return payoff0, payoff1, result

    def print_scoreboard(self):
        for i,agent in enumerate(self.agents):
            print(agent.agent_type())
            print(self.scoreboard[i])

class InvalidActionError(BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    gr = GamesRunner()
    gr.run()

 




