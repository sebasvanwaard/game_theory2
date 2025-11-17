import numpy as np

def test(game_history, player_id):
    other_player_id = 1 - player_id
    length = len(game_history)
    # First move nice
    if length == 0:
        return 0
    N = 30
    # tit for tat until N
    if length < N:
        return game_history[-1][other_player_id]
    else:
        meanie = np.sum(game_history, axis=0)[other_player_id]
        meanie /= length
        if meanie > 0.5:
            return 1
        else:
            return 0

        
