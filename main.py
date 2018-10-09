from agents import *
from repeated_pd import *


def run_tournmanet(agents=None, verbose=False, n_rounds=5, play_self=False):
    gr = GamesRunner(agents, verbose, n_rounds, play_self=play_self)
    results = gr.run()
    return results

if __name__ == '__main__':
    actions = ["C", "D"]
    no_random_agents = [AlwaysDefect(actions),
                  AlwaysCooperate(actions),
                   TitForTat(actions),
                   TitFor2Tat(actions),
                   Pavlov(actions),
                   WinStayLoseShift(actions),
                   NeverForgive(actions),
                  SuperAgent(actions)]

    tft_agents = [ TitForTat(actions),
                   TitFor2Tat(actions),
                   SuperAgent(actions)]


    #all_agents = [SuperAgent(actions), WinStayLoseShift(actions)]
    if True:
        for n_rounds in [5,100,200,.75,.95,.99]:

            ## Recreate all agents
            all_agents = [AlwaysDefect(actions),
                          RandomAgent(actions),
                          AlwaysCooperate(actions),
                          TitForTat(actions),
                          TitFor2Tat(actions),
                          Pavlov(actions),
                          WinStayLoseShift(actions),
                          NeverForgive(actions),
                          SuperAgent(actions)]
            
            print("******  Number of rounds: {} ***********".format(n_rounds))
            run_tournmanet(all_agents, n_rounds=n_rounds, play_self=True)
    else:
        #run_tournmanet(no_random_agents, n_rounds=200, play_self=True)
        #run_tournmanet([SuperAgent(actions)], n_rounds=200, play_self=True)

        run_tournmanet(no_random_agents, n_rounds=100, play_self=True)
        #run_tournmanet([AlwaysDefect(actions), SuperAgent(actions)], n_rounds=100, play_self=False)
        #run_tournmanet([SuperAgent(actions)], n_rounds=100, play_self=True)
