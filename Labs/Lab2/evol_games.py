from numpy.random import choice
from agents import *
import copy
import numpy as np

class GamesRunner:
    def __init__(self, game="SH", verbose=False, n_a1=.33, n_a2=.33, n_tft=.34, n_ntft=0, n_generations=15, games_per_generation=2500, interaction='REP', gamma = .95):
        self.interaction = interaction
        self.n_generations = n_generations
        self.game = game
        self.n_agents = 900
        self.actions = ['C','D']        
        
        self.n_a1 = n_a1
        self.n_a2 = n_a2
        self.n_tft = n_tft
        self.n_ntft = n_ntft

        if interaction == 'REP':
            self.games_per_generation = games_per_generation
            self.create_agent_lists()

        if game == "BS":
            for agent in self.agents:
                agent.type = choice([0,1])

        self.gamma = gamma
        self.n_games_played = 0
        self.total_rounds_played = 0
        self.n_agents = len(self.agents)
        self.verbose = verbose # Debugging printouts

        if game == "PD":
            self.R = 3
            self.T = 5
            self.P = 2
            self.S = 1
        elif game == "SH":
            self.R = 2
            self.T = 1
            self.P = 1
            self.S = 0
        # Battle of the sexes rewards (together + likes activity, together + dislikes activity, apart)
        self.TL = 3
        self.TD = 2
        self.A = 0

        self.payoffs = self.calc_payoffs(self.game)

    def run(self):
        for i in range(self.n_generations):
            print("A1:" + str(len(self.a1_players)) + "--A2:" + str(len(self.a2_players)) + "--TFT:" + str(len(self.tft_players)) + "--nTFT:" + str(len(self.ntft_players)))
            self.play_cycle()
            avg_payoffs = self.avg_payoffs()
            avg = self.avg_payoff(self.agents)
            print(avg)
            print(len(self.agents))
            self.n_a1 += self.n_a1 * (self.avg_payoff(self.a1_players) / avg - 1)
            self.n_a2 += self.n_a2 * (self.avg_payoff(self.a2_players) / avg - 1)
            self.n_tft += self.n_tft * (self.avg_payoff(self.tft_players) / avg - 1)
            self.n_ntft += self.n_ntft * (self.avg_payoff(self.ntft_players) / avg - 1)
            print((int(round(self.n_a1 * self.n_agents)) + int(round(self.n_a2 * self.n_agents)) + int(round(self.n_tft * self.n_agents)) + int(round(self.n_ntft * self.n_agents))))
            assert((int(round(self.n_a1 * self.n_agents)) + int(round(self.n_a2 * self.n_agents)) + int(round(self.n_tft * self.n_agents)) + int(round(self.n_ntft * self.n_agents))))
            self.create_agent_lists()

    def play_cycle(self):
        if self.interaction == "REP":
            counter = 0
            while counter < self.games_per_generation:
                a0 = random.choice(self.agents)
                a1 = random.choice(self.agents)
                if self.game == 'BS' and a0.type == a1.type:
                    continue
                elif self.game == 'BS':
                    # In battle of the sexes, it is assumed the agents have different preferences, and that the agent in position 0 prefers the first action
                    if a0.type == 1:
                        temp = a1
                        a1 = a0
                        a0 = temp
                self.play_game(a0, a1)
                counter += 1

    def play_game(self, agent0, agent1):
        payoffs = self.payoffs[(self.convert_agent_type(agent0), self.convert_agent_type(agent1))]
        agent0.score += payoffs[0]
        agent1.score += payoffs[1]
    
    def convert_agent_type(self, agent):
        if agent.agent_type() == 'AlwaysCooperate':
            return 'A1'
        elif agent.agent_type() == 'AlwaysDefect':
            return 'A2'
        elif agent.agent_type() == 'TitForTat':
            return 'TFT' 
        elif agent.agent_type() == 'NotTitForTat':
            return 'nTFT'

    def create_agent_lists(self):
        if self.interaction == 'REP':
            self.a2_players = [AlwaysDefect(self.actions)] * int(round(self.n_a2 * self.n_agents))
            self.a1_players = [AlwaysCooperate(self.actions)] * int(round(self.n_a1 * self.n_agents))
            self.tft_players = [TitForTat(self.actions)] * int(round(self.n_tft * self.n_agents))
            self.ntft_players = [NotTitForTat(self.actions)] * int(round(self.n_ntft * self.n_agents))
            self.agents = self.a1_players + self.a2_players + self.tft_players + self.ntft_players

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

    def avg_payoffs(self):
        return [self.avg_payoff(self.a1_players), self.avg_payoff(self.a2_players), self.avg_payoff(self.tft_players), self.avg_payoff(self.ntft_players)]

    def avg_payoff(self, agents):
        if len(agents) == 0:
            return 0
        avg = 0
        for agent in agents:
            avg += agent.score
        return avg / float(len(agents))

    def calc_payoffs(self, game=None):
        if game is None:
            game = self.game
        agent_types = ['A1', 'A2', 'TFT', 'nTFT']
        if game == 'PD':
            return self.calc_payoffs_pd(agent_types)
        elif game == 'SH': # same structure as PD, but different values
            return self.calc_payoffs_pd(agent_types)
        elif game == 'BS':
            return self.calc_payoffs_bs(agent_types)

    def calc_payoffs_pd(self, agent_types):
        payoffs = {}
        payoffs[('A1', 'A1')] = (self.R / (1-self.gamma), self.R / (1-self.gamma))
        payoffs[('A1', 'A2')] = (self.S / (1-self.gamma), self.T / (1-self.gamma))
        payoffs[('A1', 'TFT')] = (self.R / (1-self.gamma), self.R / (1-self.gamma))
        payoffs[('A1', 'nTFT')] = (self.S / (1-self.gamma), self.T / (1-self.gamma))

        payoffs[('A2', 'A1')] = (self.T / (1-self.gamma), self.S / (1-self.gamma))
        payoffs[('A2', 'A2')] = (self.P / (1-self.gamma), self.P / (1-self.gamma))
        payoffs[('A2', 'TFT')] = (self.T + self.gamma * (self.P / (1-self.gamma)), self.S + self.gamma * (self.P / (1-self.gamma)))
        payoffs[('A2', 'nTFT')] = (self.P + self.gamma * (self.T / (1-self.gamma)), self.P + self.gamma * (self.S / (1-self.gamma)))

        payoffs[('TFT', 'A1')] = (self.R / (1-self.gamma), self.R / (1-self.gamma))
        payoffs[('TFT', 'A2')] = (self.S + self.gamma * (self.P / (1-self.gamma)), self.T + self.gamma * (self.P / (1-self.gamma)))
        payoffs[('TFT', 'TFT')] = (self.R / (1-self.gamma), self.R / (1-self.gamma))
        payoffs[('TFT', 'nTFT')] = (self.S / (1 - self.gamma ** 4) + ((self.gamma * self.P) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.T) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.R) / (1 - self.gamma ** 4)),
                                   (self.T / (1 - self.gamma ** 4) + ((self.gamma * self.P) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.S) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.R) / (1 - self.gamma ** 4))))

        payoffs[('nTFT', 'A1')] = (self.T / (1-self.gamma), self.S / (1-self.gamma))
        payoffs[('nTFT', 'A2')] = (self.P + self.gamma * (self.S / (1-self.gamma)), self.P + self.gamma * (self.T / (1-self.gamma)))
        payoffs[('nTFT', 'TFT')] =  (self.T / (1 - self.gamma ** 4) + ((self.gamma * self.P) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.S) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.R) / (1 - self.gamma ** 4)),
                                     (self.S / (1 - self.gamma ** 4) + ((self.gamma * self.P) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.T) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.R) / (1 - self.gamma ** 4))))
        payoffs[('nTFT', 'nTFT')] = (self.P / (1 - self.gamma ** 2) + ((self.gamma * self.R) / (1 - self.gamma ** 2)),
                                     self.P / (1 - self.gamma ** 2) + ((self.gamma * self.R) / (1 - self.gamma ** 2)))
        return payoffs

    def calc_payoffs_bs(self, agent_types):
        payoffs = {}
        payoffs[('A1', 'A1')] = (self.TL / (1-self.gamma), self.TD / (1-self.gamma))
        payoffs[('A1', 'A2')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))
        payoffs[('A1', 'TFT')] = (self.TL / (1-self.gamma), self.TD / (1-self.gamma))
        payoffs[('A1', 'nTFT')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))

        payoffs[('A2', 'A1')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))
        payoffs[('A2', 'A2')] = (self.TD / (1-self.gamma), self.TL / (1-self.gamma))
        payoffs[('A2', 'TFT')] = (self.A + self.gamma * (self.TD / (1-self.gamma)), self.A + self.gamma * (self.TL / (1-self.gamma)))
        payoffs[('A2', 'nTFT')] = (self.TD + self.gamma * (self.A / (1-self.gamma)), self.TL + self.gamma * (self.A / (1-self.gamma)))

        payoffs[('TFT', 'A1')] = (self.TL / (1-self.gamma), self.TD / (1-self.gamma))
        payoffs[('TFT', 'A2')] = (self.A + self.gamma * (self.TD / (1-self.gamma)), self.A + self.gamma * (self.TL / (1-self.gamma)))
        payoffs[('TFT', 'TFT')] = (self.TL / (1-self.gamma), self.TD / (1-self.gamma))
        payoffs[('TFT', 'nTFT')] = (self.A / (1 - self.gamma ** 4) + ((self.gamma * self.TD) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.A) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.TL) / (1 - self.gamma ** 4)),
                                   (self.A / (1 - self.gamma ** 4) + ((self.gamma * self.TL) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.A) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.TD) / (1 - self.gamma ** 4))))

        payoffs[('nTFT', 'A1')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))
        payoffs[('nTFT', 'A2')] = (self.TD + self.gamma * (self.A / (1-self.gamma)), self.TL + self.gamma * (self.A / (1-self.gamma)))
        payoffs[('nTFT', 'TFT')] = (self.A / (1 - self.gamma ** 4) + ((self.gamma * self.TD) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.A) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.TL) / (1 - self.gamma ** 4)),
                                   (self.A / (1 - self.gamma ** 4) + ((self.gamma * self.TL) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.A) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.TD) / (1 - self.gamma ** 4))))

        payoffs[('nTFT', 'nTFT')] = (self.TD / (1 - self.gamma ** 2) + ((self.gamma * self.TL) / (1 - self.gamma ** 2)),
                                     self.TL / (1 - self.gamma ** 2) + ((self.gamma * self.TD) / (1 - self.gamma ** 2)))
        return payoffs


class InvalidActionError(BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    gr = GamesRunner()
    gr.run()

 




