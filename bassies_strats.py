import numpy as np

def traitor(GTsim, player_id):
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
    if GTsim.t < 3:
        return 0
    elif np.sum(GTsim.config[GTsim.t - 3:GTsim.t], axis = 0)[opponent_id] == 0:
        return 1
    elif GTsim.t > 5:
        if np.sum(GTsim.config[GTsim.t-5:GTsim.t], axis = 0)[opponent_id] == 5:
            return 1
        else:
            return 0
    else:
        return 0

def thrower(GTsim, player_id):
    """
    This strategy will play to win (tit for tat). As long as its winning. Otherwise it will throw the game with random moves.
    """
    
    opponent_id = 0
    if player_id == 0:
        opponent_id = 1
    
    if GTsim.live_scores[-1][player_id] < GTsim.live_scores[-1][opponent_id]:
        return np.random.randint(0,2)
    else:
        length = GTsim.t
        if length == 0:
            return 0
        if player_id == 0:
            return GTsim.config[-1][1]
        else:
            return GTsim.config[-1][0]
    
def indecisive(GTsim, player_id):
    """
    Changes to a random stategy from the library every 10 steps
    """
    

