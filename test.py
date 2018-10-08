from agents import *
from repeated_pd import *


def run_test(agents=None, verbose=False, n_rounds=5):
    gr = GamesRunner(agents, verbose, n_rounds)
    results = gr.run()
    print(results)
    return results

def test_cases():
    actions = ["C", "D"]

    ## Basic
    result = run_test([AlwaysDefect(actions), AlwaysCooperate(actions)])
    assert result == {'0:0': ['DC', 'DC', 'DC', 'DC', 'DC']}

    result = run_test([AlwaysDefect(actions), TitForTat(actions)])
    assert result == {'0:0': ['DC', 'DD', 'DD', 'DD', 'DD']}

    result = run_test([AlwaysCooperate(actions), TitForTat(actions)])
    assert result == {'0:0': ['CC', 'CC', 'CC', 'CC', 'CC']}

    result = run_test([TitForTat(actions), NeverForgive(actions)])
    assert result == {'0:0': ['CC', 'CC', 'CC', 'CC', 'CC']}

    result = run_test([AlwaysDefect(actions), NeverForgive(actions)])
    assert result == {'0:0': ['DC', 'DD', 'DD', 'DD', 'DD']}

    result = run_test([NeverForgive(actions), NeverForgive(actions)])
    assert result == {'0:0': ['CC', 'CC', 'CC', 'CC', 'CC']}

    result = run_test([Alternater(actions), TitForTat(actions)])  # should be tied for odd # of rounds, else tft +2
    assert result == {'0:0': ['CC', 'DC', 'CD', 'DC', 'CD']}

    ## TitFor2Tat
    result = run_test([NeverForgive(actions), TitFor2Tat(actions)])
    assert result == {'0:0': ['CC', 'CC', 'CC', 'CC', 'CC']}

    result = run_test([AlwaysDefect(actions), TitFor2Tat(actions)])
    assert result == {'0:0': ['DC', 'DC', 'DD', 'DD', 'DD']}

    result = run_test([Alternater(actions, freq=2), TitFor2Tat(actions)])
    assert result == {'0:0': ['CC', 'CC', 'DC', 'DC', 'CD']}
    result = run_test([Alternater(actions, freq=1), TitFor2Tat(actions)])
    assert result == {'0:0': ['CC', 'DC', 'CC', 'DC', 'CC']}

    ## Pavlov - DEFECT if you played different moves, else C
    result = run_test([Alternater(actions), Pavlov(actions)])
    assert result == {'0:0': ['CC', 'DC', 'CD', 'DD', 'CC']}

    result = run_test([NeverForgive(actions), Pavlov(actions)])
    assert result == {'0:0': ['CC', 'CC', 'CC', 'CC', 'CC']}

    result = run_test([Pavlov(actions), Alternater(actions, freq=2)], n_rounds=10)
    assert result == {'0:0': ['CC', 'CC', 'CD', 'DD', 'CC', 'CC', 'CD', 'DD', 'CC', 'CC']}


    ## Win Stay - change if you didn't "win" (e.g. one of best 2 outcomes)
    result = run_test([WinStayLoseShift(actions), NeverForgive(actions)]) # should be CC
    assert result == {'0:0': ['CC', 'CC', 'CC', 'CC', 'CC']}

    result = run_test([WinStayLoseShift(actions), Alternater(actions)])
    assert result == {'0:0': ['CC', 'CD', 'DC', 'DD', 'CC']}

    result = run_test([WinStayLoseShift(actions), Alternater(actions, freq=2)], n_rounds=10)
    assert result == {'0:0': ['CC', 'CC', 'CD', 'DD', 'CC', 'CC', 'CD', 'DD', 'CC', 'CC']}


    ## All agents
    all_agents = [AlwaysDefect(actions),
                  RandomAgent(actions),
                  AlwaysCooperate(actions),
                   TitForTat(actions),
                   TitFor2Tat(actions),
                   Pavlov(actions),
                   WinStayLoseShift(actions),
                   NeverForgive(actions)]

    selected_agents = [AlwaysDefect(actions),
                  RandomAgent(actions),
                   TitForTat(actions),
                   TitFor2Tat(actions),
                   Pavlov(actions),
                   WinStayLoseShift(actions),
                   NeverForgive(actions)]

    result = run_test(n_rounds=200, agents=selected_agents)

    ## All Agents
    result = run_test(n_rounds=200)

if __name__ == '__main__':
    test_cases()
