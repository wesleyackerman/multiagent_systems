import numpy as np
from evol_games import GamesRunner
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import utils
import pylab as pl

print(os.getcwd())


class lattice_gameboard:
    def __init__(self, game="PD", rows=30, columns=30, agents=("A1", "A2", "TFT", "nTFT"), weights=None, quadrants=False, variant=None, rounds=20, gamma=.95):
        if variant is None:
            variant = "{},{},rand={},{}".format(game, gamma, not quadrants, rows)
        self.path = os.path.join(r"./graphs/",variant)
        utils.make_dir(self.path)

        self.columns = columns
        self.rows = rows
        self.shape = [self.rows, self.columns]
        self.game = game

        self.mapping = {}
        for i, a in enumerate(agents):
            self.mapping[a] = i

        self.paired_payoff_matrix = GamesRunner(gamma=gamma).calc_payoffs(game=self.game)
        self.agents = agents
        self.colors = ['blue', 'red', 'violet', 'green']
        if weights is None:
            weights = [1 / len(self.agents)] * 4
        self.weights = weights
        self.populate_lattice(quadrants=quadrants)
        # print(self.agent_lattice)

        for i in range(0, rounds):
            old_lattice = self.agent_lattice
            self.run_generation(i)
            if (self.agent_lattice == old_lattice).all():
                break

    def run_generation(self,i=0):
        self.draw_lattice(self.agent_lattice, i)
        self.calculate_payoffs()
        self.update_lattice()

    def populate_lattice(self, quadrants=False):
        """ This populates a lattice with a mix of agents
        """
        # np.random.randint(0,4,[30,30])
        half_way_rows =    int(self.rows/2)
        half_way_columns = int(self.columns/2)
        if quadrants:
            self.agent_lattice = np.zeros([self.rows, self.columns], dtype=object)
            self.agent_lattice[0:half_way_rows,0:half_way_columns] = self.agents[3]
            self.agent_lattice[0:half_way_rows,half_way_columns:] = self.agents[2]
            self.agent_lattice[half_way_rows:,0:half_way_columns] = self.agents[1]
            self.agent_lattice[half_way_rows:,half_way_columns:] = self.agents[0]
        else:
            self.agent_lattice = np.random.choice(a=self.agents, size=[self.rows, self.columns], p=self.weights)

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
            r += self.paired_payoff_matrix[(central_agent, agent)][0]
        return r / 9

    def draw_lattice2(self, lattice):
        cmap = mpl.colors.ListedColormap(self.colors)
        # categories, integer_encoding = np.unique(lattice, return_inverse=True)
        # integer_encoding = integer_encoding.reshape([self.rows,self.columns])
        int_lattice = utils.replace_array_with_map(lattice, self.mapping, new_type=object).astype(int)
        print(int_lattice)
        plt.imshow(int_lattice, interpolation='nearest', cmap=cmap, origin='lower')
        plt.show()

    def draw_lattice(self, lattice, iteration=0):
        cmap = mpl.colors.ListedColormap(self.colors)
        bounds = range(0, len(self.agents) + 1)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        int_lattice = utils.replace_array_with_map(lattice, self.mapping, new_type=object).astype(int)

        img = plt.imshow(int_lattice, interpolation='nearest', origin='lower', cmap=cmap, norm=norm)
        #plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds)
        mycmap = pl.cm.jet  # for example
        for i,agent in enumerate(self.agents):
            pl.plot(0, 0, "-", c=self.colors[i], label=agent)
        pl.legend()
        plt.savefig(os.path.join(self.path, "lattice{}.png".format(iteration)))
        plt.clf()
        #print(int_lattice)
        #print(self.colors)
    def print_summary(self):
        pass


if __name__ == '__main__':
    size = 30
    games = ["BS", "SH", "PD"]
    for gamma in [.95,.99]:
        for game in games:
            for quadrants in [True, False]:
                lg = lattice_gameboard(rows=size, columns=size, quadrants=quadrants, game=game, gamma=gamma)

    gameboard = lg.agent_lattice