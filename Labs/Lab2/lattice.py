import numpy as np
from evol_games import GamesRunner
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import utils
import pylab as pl
from random import shuffle

print(os.getcwd())

color_dict = {"AC":"blue", "AD":"red", "TFT":"violet", "nTFT":"green"}
class lattice_gameboard:
    def __init__(self, game="PD", rows=30, columns=30, agents=("AC", "AD", "TFT", "nTFT"), weights=None, variant=None, rounds=30, gamma=.95, pattern="quadrants", plot=False, shuffle=True):
        """
        Args:
              pattern (str): random, quadrants, diagonal, vertical, or horizontal - method of initializing lattice

        """
        self.shuffle=shuffle
        self.agents = agents
        self.gamma = gamma
        self.pattern = pattern
        if weights is None:
            weights = [1 / len(self.agents)] * 4
            self.pretty_weights = weights

        if variant is None:
            self.pretty_weights = [round(w,2) for w in weights]
            variant = "{},{},{},wt={},{},{}".format(game, gamma, rows, self.pretty_weights, pattern,agents)
        self.weights = weights

        self.path = os.path.join(r"./graphs/",variant)
        utils.make_dir(self.path,delete=False)
        self.plot = plot
        self.columns = columns
        self.rows = rows
        self.shape = [self.rows, self.columns]
        self.game = game

        self.mapping = {}
        for i, a in enumerate(agents):
            self.mapping[a] = i

        self.paired_payoff_matrix = GamesRunner(game=self.game, gamma=gamma).calc_payoffs()

        self.colors = [color_dict[a] for a in agents]

        self.weights = weights
        self.populate_lattice(pattern=pattern, weights=self.weights)
        # print(self.agent_lattice)

        for i in range(0, rounds):
            old_lattice = self.agent_lattice
            self.run_generation(i)

            if (self.agent_lattice == old_lattice).all():
                break

        winning_agents = np.unique(self.agent_lattice)
        self.winners = winning_agents.tolist()

        self.final_round = i

    def get_results(self):
        return [self.game, self.gamma, self.rows, self.pretty_weights.tolist(), self.pattern, self.agents, self.winners, self.final_round]


    def run_generation(self,i=0):
        if self.plot:
            self.draw_lattice(self.agent_lattice, i)
        self.calculate_payoffs()
        self.update_lattice()

    def populate_lattice(self, weights=None, pattern = "diagonal"):
        """ This populates a lattice with a mix of agents
        """
        # np.random.randint(0,4,[30,30])
        half_way_rows =    int(self.rows/2)
        half_way_columns = int(self.columns/2)
        self.agent_lattice = np.zeros([self.rows, self.columns], dtype=object)
        shuffled_agents = shuffle(self.agents[:]) if self.shuffle else self.agents[:]

        if pattern=="random":
            self.agent_lattice = np.random.choice(a=self.agents, size=[self.rows, self.columns], p=weights)
        elif pattern == "quadrants":
            self.agent_lattice[0:half_way_rows,0:half_way_columns] = shuffled_agents[3]
            self.agent_lattice[0:half_way_rows,half_way_columns:] = shuffled_agents[2]
            self.agent_lattice[half_way_rows:,0:half_way_columns] = shuffled_agents[1]
            self.agent_lattice[half_way_rows:,half_way_columns:] = shuffled_agents[0]
        else:
            cum_wt = 0
            previous_item = 0
            size = self.rows*self.columns
            for agent_idx,w in enumerate(weights):
                cum_wt+=w
                next_item = int(size*cum_wt+1e-5)
                ## Populate lattice with that agent
                for idx in range(previous_item, next_item):
                    i,j = utils.integer_to_coordinates(idx,self.rows,self.columns, method=pattern)
                    self.agent_lattice[i,j] = shuffled_agents[agent_idx]
                previous_item = next_item

    def update_lattice(self, use_random_argmax=True):
        """ This updates the lattice where each cell adopts the strategy of the most successful neighbor
        """
        # print(np.indices(self.shape))
        # neighbors = self.neighbor_indices(np.indices(self.shape))
        # neighbor_agents = self.agent_lattice[neighbors[:,0], neighbors[:,1]]
        new_lattice = self.agent_lattice.copy()
        argmax = utils.random_argmax if use_random_argmax else np.argmax
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                neighbors = self.neighbor_indices([i, j])
                neighbor_idx = (neighbors[:, 0], neighbors[:, 1])
                neighbor_agents = self.agent_lattice[neighbor_idx]
                best_index = argmax(self.payoffs[neighbor_idx])

                # Don't change if other strategy is equivalent
                if self.payoffs[neighbor_idx][best_index] == self.payoffs[i,j]:
                    pass
                else:
                    new_lattice[i, j] = neighbor_agents[best_index]
        self.agent_lattice = new_lattice

    def neighbor_indices(self, index):
        """ Return indices of neighbors. This includes the original cell as a "neighbor".
        Assumes a square lattice
        Args:
            index (x,y tuple)
        Returns:
            list of x,y tuples for all neighbors
        """
        return (np.add(utils.cartesian_product([-1, 0, 1], [-1, 0, 1]), index)) % self.rows

    def calculate_payoffs(self):
        """ This calculates the payoffs of the lattice
        """
        payoffs = np.zeros([self.rows, self.columns])
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                payoffs[i, j] = self.calculate_cell_payoff(i, j)
        self.payoffs = payoffs

    def calculate_cell_payoff(self, i, j):
        """ Calculate the payoff of a cell
        """
        central_agent = self.agent_lattice[i, j]
        # print(central_agent)
        neighbors = self.neighbor_indices([i, j])
        neighbor_agents = self.agent_lattice[neighbors[:, 0], neighbors[:, 1]]

        # Remove central agent
        neighbor_agents = np.delete(arr=neighbor_agents, obj=4, axis=0)

        r = 0
        for agent in neighbor_agents:
            # print(agent)
            payoff = self.paired_payoff_matrix[(central_agent, agent)][0]
            r += payoff
        return r / 8

    def draw_lattice(self, lattice, iteration=0):
        cmap = mpl.colors.ListedColormap(self.colors)
        bounds = range(0, len(self.agents) + 1)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        int_lattice = utils.replace_array_with_map(lattice, self.mapping, new_type=object).astype(int)

        img = plt.imshow(int_lattice, interpolation='nearest', origin='lower', cmap=cmap, norm=norm)
        #plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds)
        mycmap = pl.cm.jet  # for example
        for i,agent in enumerate(np.unique(self.agents)):
            pl.plot(0, 0, "-", c=self.colors[i], label=agent)
        pl.legend()
        plt.savefig(os.path.join(self.path, "lattice{:02d}.png".format(iteration)))
        plt.clf()
        #print(int_lattice)
        #print(self.colors)
    def print_summary(self):
        pass

def main_loop(size = 30):
    patterns = ["random", "quadrants", "horizontal", "vertical", "diagonal"]
    #patterns = ["diagonal"]

    games = ["BS", "SH", "PD"]
    for pattern in patterns:
        for gamma in [.95,.99]:
            for game in games:
                #variant = "{},{},{},{},{}".format(game, gamma, size, weights, pattern)
                lg = lattice_gameboard(rows=size, columns=size, game=game, gamma=gamma, pattern=pattern)


def main_loop_data(size = 30):

    # repititions
    # random starts

    patterns = ["random", "quadrants", "horizontal", "vertical", "diagonal"]
    #patterns = ["diagonal"]

    # report all variation parameters, report who won, report how many reps
    results = []
    agents = ["AC", "AD", "TFT", "nTFT"]
    games = ["BS", "SH", "PD"]
    for pattern in patterns:
        max_loops = 10 if pattern == "quadrants" else 100
        for i in range(0,max_loops):
            for gamma in [.95,.99]:
                for game in games:
                        weights = utils.normalize(np.random.rand(len(agents)), as_list=True)
                        #variant = "{},{},{},{},{}".format(game, gamma, size, weights, pattern)
                        lg = lattice_gameboard(rows=size, columns=size, game=game, gamma=gamma, pattern=pattern, weights=weights, plot=False)
                        results.append(lg.get_results())

if __name__ == '__main__':
    size = 30
    gamma = .95
    weights = [.8,.2,0,0]
    games = ["BS", "SH", "PD"]
    #main_loop(size)

    main_loop_data(30)

    if False:
        games = ["PD"]
        pattern = "quadrants"
        for game in games:
            lg = lattice_gameboard(rows=size, columns=size, game=game, gamma=gamma,weights=weights, pattern=pattern)

        gameboard = lg.agent_lattice

    if False:
        ## AD can dominate
        weights = utils.normalize([.8,.01,.05,.05], as_list=True)
        agents = ["AC","AD","TFT","nTFT"]
        lg = lattice_gameboard(rows=size, columns=size, game="PD", gamma=.95, weights=weights, pattern="random", agents=agents, variant=None)

        ## TFT can win
        weights = utils.normalize([.6,.05,.3,.05], as_list=True)
        agents = ["AC","AD","TFT","nTFT"]
        lg = lattice_gameboard(rows=size, columns=size, game="PD", gamma=.95, weights=weights, pattern="random", agents=agents, variant=None)

        # Anti-nephi-lehis
        weights = utils.normalize([.05,.5,.4,.3,.2])
        agents = ["TFT","AC","TFT","AD","nTFT"]
        lg = lattice_gameboard(rows=size, columns=size, game="PD", gamma=.95, weights=weights, pattern="diagonal", agents=agents, variant="antinephi")
