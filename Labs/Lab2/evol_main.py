from agents import *
from evol_games import *


def run_tournament(game, n_ac, n_ad, n_tft, n_ntft, gamma):
    gr = GamesRunner(game=game, n_ac=n_ac, n_ad=n_ad, n_tft=n_tft, n_ntft=n_ntft, gamma=gamma)
    results = gr.run()
    return results

if __name__ == '__main__':

    for game in ['PD', 'SH', 'BS']:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(game)
        for gamma in [.95, .99]:
            print("_______________________________________")
            print(gamma)
            run_tournament(game, 0, 0, .1, .9, gamma)
            run_tournament(game, 0, 0, .25, .75, gamma)
            run_tournament(game, 0, 0, .5, .5, gamma)
            run_tournament(game, 0, 0, .75, .25, gamma)
            run_tournament(game, 0, 0, .9, .1, gamma)

            run_tournament(game, .1, .9, 0, 0, gamma)
            run_tournament(game, .25, .75, 0, 0, gamma)
            run_tournament(game, .5, .5, 0, 0, gamma)
            run_tournament(game, .75, .25, 0, 0, gamma)
            run_tournament(game, .9, .1, 0, 0, gamma)

            run_tournament(game, .1, 0, .9, 0, gamma)
            run_tournament(game, .25, 0, .75, 0, gamma)
            run_tournament(game, .5, 0, .5, 0, gamma)
            run_tournament(game, .75, 0, .25, 0, gamma)
            run_tournament(game, .9, 0, .1, 0, gamma)

            run_tournament(game, .1, 0, 0, .9, gamma)
            run_tournament(game, .25, 0, 0, .75, gamma)
            run_tournament(game, .5, 0, 0, .5, gamma)
            run_tournament(game, .75, 0, 0, .25, gamma)
            run_tournament(game, .9, 0, 0, .1, gamma)

            run_tournament(game, 0, .1, .9, 0, gamma)
            run_tournament(game, 0, .25, .75, 0, gamma)
            run_tournament(game, 0, .5, .5, 0, gamma)
            run_tournament(game, 0, .75, .25, 0, gamma)
            run_tournament(game, 0, .9, .1, 0, gamma)

            run_tournament(game, .25, .25, .25, .25, gamma)
            run_tournament(game, .25, .5, .25, 0, gamma)
            run_tournament(game, .25, .25, .5, 0, gamma)
            run_tournament(game, .33, .33, .34, 0, gamma)
            run_tournament(game, .2, .4, .4, 0, gamma)
            run_tournament(game, .1, .45, .45, 0, gamma)

            run_tournament(game, 0, .33, .34, .33, gamma)
            run_tournament(game, 0, .4, .4, .2, gamma)
            run_tournament(game, 0, .45, .45, .1, gamma)




#            run_tournament(game, 0, .1, 0, .9, gamma)
#            run_tournament(game, 0, .25, 0, .75, gamma)
#            run_tournament(game, 0, .5, 0, .5, gamma)
#            run_tournament(game, 0, .75, 0, .25, gamma)
#            run_tournament(game, 0, .9, 0, .1, gamma)

#  game="PD", verbose=False, n_ac=0, n_ad=.75, n_tft=.25, n_ntft=.0, n_generations=18, games_per_generation=2500, interaction='REP', gamma = .95
