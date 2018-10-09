from agents import *
from repeated_pd import *


def run_tournmanet(agents=None, verbose=False, n_rounds=5):
    gr = GamesRunner(agents, verbose, n_rounds)
    results = gr.run()
    return results

if __name__ == '__main__':
    actions = ["C", "D"]
    all_agents = [AlwaysDefect(actions),
                  RandomAgent(actions),
                  AlwaysCooperate(actions),
                   TitForTat(actions),
                   TitFor2Tat(actions),
                   Pavlov(actions),
                   WinStayLoseShift(actions),
                   NeverForgive(actions),
                  SuperAgent(actions)]

    all_agents = [SuperAgent(actions), WinStayLoseShift(actions)]
    # run_tournmanet(all_agents, n_rounds=.75)
    # run_tournmanet(all_agents, n_rounds=.95)
    # run_tournmanet(all_agents, n_rounds=.99)
    #
    # run_tournmanet(all_agents, n_rounds=5)
    # run_tournmanet(all_agents, n_rounds=100)
    run_tournmanet(all_agents, n_rounds=200)
