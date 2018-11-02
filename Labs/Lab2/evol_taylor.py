from agents import *
from evol_games import *


def run_tournament(game, n_ac, n_ad, n_tft, n_ntft, gamma):
    gr = GamesRunner(game=game, n_ac=n_ac, n_ad=n_ad, n_tft=n_tft, n_ntft=n_ntft, gamma=gamma)
    results = gr.run()
    return results

if __name__ == '__main__':
    #run_tournament('SH', .5, 0, .5, 0, 0.99)


    for game in ['SH']:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(game)
        for gamma in [.95, .99]:
            print("_______________________________________")
            print(gamma)

            run_tournament(game, .25, 0, .75, 0, gamma)
