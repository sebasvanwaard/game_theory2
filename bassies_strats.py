import numpy as np

def traitor(game_history, player_id):
    """
    Traitor strat. This strat tries to win trust by playing silent. 
    If the opponent returns the favor 3 times in a row it starts talking until the opponent stops playing silent. 
    Then it starts over again.
    if the opponent talks for more than 5 times in a row the traitor starts talking as well.
    """
    opponent_id = 0
    if player_id == 0:
        opponent_id = 1

    # initial moves
    if len(game_history) < 3:
        return 0
    elif np.sum(game_history[-3:], axis = 0)[opponent_id] == 0:
        return 1
    elif np.sum(game_history[-3:], axis = 0)[opponent_id] == 5:
        return 1


