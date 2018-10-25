from random import choice
from agents import *
import copy
import numpy as np
import math
 
class GamesRunner:
    def __init__(self, game="BS", verbose=False, n_ac=0, n_ad=.75, n_tft=.25, n_ntft=.0, n_generations=15, games_per_generation=5000, interaction='REP', gamma = .95):
        print("<><><><><><><><><><><><><><><><>")
        self.interaction = interaction
        self.n_generations = n_generations
        self.game = game
        self.n_agents = 900
        self.actions = ['C','D']        

        self.n_ac = n_ac
        self.n_ad = n_ad
        self.n_tft = n_tft
        self.n_ntft = n_ntft

        if interaction == 'REP':
            self.games_per_generation = games_per_generation
            self.create_agent_lists()

        self.gamma = gamma
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
            if self.n_lists_empty([self.ad_players, self.ac_players, self.tft_players, self.ntft_players]) == 3:
                print("AC:" + str(len(self.ac_players)) + "--AD:" + str(len(self.ad_players)) + "--TFT:" + str(len(self.tft_players)) + "--nTFT:" + str(len(self.ntft_players)))
                break

            if i == self.n_generations - 1 or i == 0:
                print("AC:" + str(len(self.ac_players)) + "--AD:" + str(len(self.ad_players)) + "--TFT:" + str(len(self.tft_players)) + "--nTFT:" + str(len(self.ntft_players)))
            self.play_cycle()
            avg_payoffs = self.avg_payoffs()
            avg = self.avg_payoff(self.agents, all_agents=True)

            #ac = self.avg_payoff(self.ac_players)
            #tft = self.avg_payoff(self.tft_players)
            #print("AC {}, TFT {}, AVG {}".format(ac,tft,avg))

            self.n_ac += self.n_ac * (safe_div(self.avg_payoff(self.ac_players), avg) - 1)
            self.n_ad += self.n_ad * (safe_div(self.avg_payoff(self.ad_players), avg) - 1)
            self.n_tft += self.n_tft * (safe_div(self.avg_payoff(self.tft_players), avg) - 1)
            self.n_ntft += self.n_ntft * (safe_div(self.avg_payoff(self.ntft_players), avg) - 1)
            try:
                assert((int(round(self.n_ac * self.n_agents)) + int(round(self.n_ad * self.n_agents)) + int(round(self.n_tft * self.n_agents)) + int(round(self.n_ntft * self.n_agents))))
            except AssertionError:
                print("AssertionError")
                print ((int(round(self.n_ac * self.n_agents)), int(round(self.n_ad * self.n_agents)), int(round(self.n_tft * self.n_agents)), int(round(self.n_ntft * self.n_agents))))
                exit()
            self.create_agent_lists()

    def play_cycle(self):
        if self.interaction == "REP":
            counter = 0
            while counter < self.games_per_generation:
                a0 = random.choice(self.agents)
                a1 = random.choice(self.agents)
                #if self.game == 'BS' and a0.pref == a1.pref:
                #    continue
                #elif self.game == 'BS':
                    # In battle of the sexes, it is assumed the agents have different preferences, and that the agent in position 0 prefers the first action
                #    if a0.pref == 1:
                #        temp = a1
                #        a1 = a0
                #        a0 = temp
                self.play_game(a0, a1)
                counter += 1

    def play_game(self, agent0, agent1):
        payoffs = self.payoffs[(self.convert_agent_type(agent0), self.convert_agent_type(agent1))]
        agent0.score += payoffs[0]
        agent1.score += payoffs[1]
        self.update_game_counts([agent0, agent1])
    
    def update_game_counts(self, agent_list):
        for agent in agent_list:
            typ = self.convert_agent_type(agent)
            self.n_games_played[typ] += 1

    def convert_agent_type(self, agent):
        if agent.agent_type() == 'AlwaysCooperate':
            return 'AC'
        elif agent.agent_type() == 'AlwaysDefect':
            return 'AD'
        elif agent.agent_type() == 'TitForTat':
            return 'TFT' 
        elif agent.agent_type() == 'NotTitForTat':
            return 'nTFT'

    def assign_prefs(self, lists):
        for lst in lists:
            for agent in lst:
                agent.pref = choice([0,1])

    def create_agent_lists(self):
        if self.interaction == 'REP':
            self.ad_players = [AlwaysDefect(self.actions)] * int(round(self.n_ad * self.n_agents))
            self.ac_players = [AlwaysCooperate(self.actions)] * int(round(self.n_ac * self.n_agents))
            self.tft_players = [TitForTat(self.actions)] * int(round(self.n_tft * self.n_agents))
            self.ntft_players = [NotTitForTat(self.actions)] * int(round(self.n_ntft * self.n_agents))
            self.n_games_played = {"AC":0, "AD":0, "TFT":0, "nTFT":0}

            #if self.game == 'BS':
            #    self.assign_prefs([self.ad_players, self.ac_players, self.tft_players, self.ntft_players])

            self.agents = self.ac_players + self.ad_players + self.tft_players + self.ntft_players
        #if self.game == "BS":
        #    print("Sdfds  " + str(len(self.agents)))
        #    self.zero_agents = []
        #    self.one_agents = []
        #    for agent in self.agents:
        #        if agent.pref == 0:
        #            self.zero_agents.append(agent)
        #        elif agent.pref == 1:
        #            self.one_agents.append(agent)
        #        else:
        #            raise InvalidActionError("Agent has unknown preference type")
        #    print(len(self.zero_agents))
        #    print(len(self.one_agents)) 

    def avg_payoffs(self):
        return [self.avg_payoff(self.ac_players), self.avg_payoff(self.ad_players), self.avg_payoff(self.tft_players), self.avg_payoff(self.ntft_players)]

    def avg_payoff(self, agents, all_agents=False):
        if len(agents) == 0:
            return 0

        if all_agents:
           n_games_played = sum(self.n_games_played.values())
           total_score=0
           for agent_type in [self.ac_players, self.ad_players, self.tft_players, self.ntft_players]:
               if agent_type:
                   total_score += agent_type[0].score
        else:
           typ = self.convert_agent_type(agents[0])
           n_games_played = self.n_games_played[typ]
           total_score = agents[0].score
        if n_games_played == 0:
            print("DIVISION BY ZERO")
            return 0
        return total_score/float(n_games_played)

    def calc_payoffs(self, game=None):
        if game is None:
            game = self.game
        agent_types = ['AC', 'AD', 'TFT', 'nTFT']
        if game == 'PD':
            return self.calc_payoffs_pd(agent_types)
        elif game == 'SH': # same structure as PD, but different values
            return self.calc_payoffs_pd(agent_types)
        elif game == 'BS':
            return self.calc_payoffs_bs(agent_types)

    def calc_payoffs_pd(self, agent_types):
        payoffs = {}
        payoffs[('AC', 'AC')] = (self.R / (1-self.gamma), self.R / (1-self.gamma))
        payoffs[('AC', 'AD')] = (self.S / (1-self.gamma), self.T / (1-self.gamma))
        payoffs[('AC', 'TFT')] = (self.R / (1-self.gamma), self.R / (1-self.gamma))
        payoffs[('AC', 'nTFT')] = (self.S / (1-self.gamma), self.T / (1-self.gamma))

        payoffs[('AD', 'AC')] = (self.T / (1-self.gamma), self.S / (1-self.gamma))
        payoffs[('AD', 'AD')] = (self.P / (1-self.gamma), self.P / (1-self.gamma))
        payoffs[('AD', 'TFT')] = (self.T + self.gamma * (self.P / (1-self.gamma)), self.S + self.gamma * (self.P / (1-self.gamma)))
        payoffs[('AD', 'nTFT')] = (self.P + self.gamma * (self.T / (1-self.gamma)), self.P + self.gamma * (self.S / (1-self.gamma)))

        payoffs[('TFT', 'AC')] = (self.R / (1-self.gamma), self.R / (1-self.gamma))
        payoffs[('TFT', 'AD')] = (self.S + self.gamma * (self.P / (1-self.gamma)), self.T + self.gamma * (self.P / (1-self.gamma)))
        payoffs[('TFT', 'TFT')] = (self.R / (1-self.gamma), self.R / (1-self.gamma))
        payoffs[('TFT', 'nTFT')] = (self.S / (1 - self.gamma ** 4) + ((self.gamma * self.P) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.T) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.R) / (1 - self.gamma ** 4)),
                                   (self.T / (1 - self.gamma ** 4) + ((self.gamma * self.P) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.S) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.R) / (1 - self.gamma ** 4))))

        payoffs[('nTFT', 'AC')] = (self.T / (1-self.gamma), self.S / (1-self.gamma))
        payoffs[('nTFT', 'AD')] = (self.P + self.gamma * (self.S / (1-self.gamma)), self.P + self.gamma * (self.T / (1-self.gamma)))
        payoffs[('nTFT', 'TFT')] =  (self.T / (1 - self.gamma ** 4) + ((self.gamma * self.P) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.S) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.R) / (1 - self.gamma ** 4)),
                                     (self.S / (1 - self.gamma ** 4) + ((self.gamma * self.P) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.T) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.R) / (1 - self.gamma ** 4))))
        payoffs[('nTFT', 'nTFT')] = (self.P / (1 - self.gamma ** 2) + ((self.gamma * self.R) / (1 - self.gamma ** 2)),
                                     self.P / (1 - self.gamma ** 2) + ((self.gamma * self.R) / (1 - self.gamma ** 2)))
        return payoffs

    def calc_payoffs_bs(self, agent_types):
        payoffs = {}
        payoffs[('AC', 'AC')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))
        payoffs[('AC', 'AD')] = (self.TD / (1-self.gamma), self.TL / (1-self.gamma))
        payoffs[('AC', 'TFT')] = (self.A + self.gamma *  (self.TD / 1-self.gamma), self.A + self.gamma *  (self.TL / 1-self.gamma))
        payoffs[('AC', 'nTFT')] = (self.TD + self.gamma *  (self.A / 1-self.gamma), self.TL + self.gamma *  (self.A / 1-self.gamma))

        payoffs[('AD', 'AC')] = (self.TL / (1-self.gamma), self.TD / (1-self.gamma))
        payoffs[('AD', 'AD')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))
        payoffs[('AD', 'TFT')] = (self.TL / (1-self.gamma), self.TD / (1-self.gamma))
        payoffs[('AD', 'nTFT')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))

        payoffs[('TFT', 'AC')] = (self.A + self.gamma *  (self.TL / 1-self.gamma), self.A + self.gamma *  (self.TD / 1-self.gamma))
        payoffs[('TFT', 'AD')] = (self.TD / (1-self.gamma), self.TL / (1-self.gamma))
        payoffs[('TFT', 'TFT')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))
        payoffs[('TFT', 'nTFT')] = (self.TD / (1 - self.gamma ** 4) + ((self.gamma * self.A) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.TL) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.A) / (1 - self.gamma ** 4)),
                                   (self.TL / (1 - self.gamma ** 4) + ((self.gamma * self.A) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.TD) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.A) / (1 - self.gamma ** 4))))

        payoffs[('nTFT', 'AC')] = (self.TL + self.gamma *  (self.A / 1-self.gamma), self.TD + self.gamma *  (self.A / 1-self.gamma))
        payoffs[('nTFT', 'AD')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))
        payoffs[('nTFT', 'TFT')] = (self.TL / (1 - self.gamma ** 4) + ((self.gamma * self.A) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.TD) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.A) / (1 - self.gamma ** 4)),
                                   (self.TD / (1 - self.gamma ** 4) + ((self.gamma * self.A) / (1 - self.gamma ** 4)) + (((self.gamma ** 2) * self.TL) / (1 - self.gamma ** 4)) + (((self.gamma ** 3) * self.A) / (1 - self.gamma ** 4))))

        payoffs[('nTFT', 'nTFT')] = (self.A / (1-self.gamma), self.A / (1-self.gamma))
        return payoffs

    def n_lists_empty(self, lists):
        n = 0
        for lst in lists:
            if len(lst) == 0:
                n += 1
        return n

def safe_div(a, b):
    if b == 0:
        print("DIVISION BY ZERO")
        return 0
    return a / b


class InvalidActionError(BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    gr = GamesRunner()
    gr.run()

 




