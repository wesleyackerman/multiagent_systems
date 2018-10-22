from agents import *
from evol_games import *


def run_tournament(agents=None, verbose=False, n_rounds=5, play_self=False):
    gr = GamesRunner()
    results = gr.run()
    return results

if __name__ == '__main__':
    run_tournament()
