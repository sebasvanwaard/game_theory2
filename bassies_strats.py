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
    
def copy_cat(GTsim, player_id):
    opponent_id = 1 - player_id
    if GTsim.t == 0:
        return 0
    return GTsim.config[GTsim.t][opponent_id]

def easy_on_je_little_toes_gestept(GTsim, player_id):
    opponent_id = 1 - player_id
    if GTsim.t == 0:
        return 0
    if np.sum(GTsim.config, axis = 0)[opponent_id] > 0:
        return 1
    else:
        return 0

def eerlijk(GTsim, player_id):
    opponent_id = 1 - player_id
    if GTsim.t == 0:
        return 0
    
    if GTsim.t < 10:
        opponent_sum = np.sum(GTsim.config[:GTsim.t], axis=0)[opponent_id]
        defect_prob = opponent_sum/GTsim.t
        if np.random.random() <= defect_prob:
            return 1
        else:
            return 0
    else:
        opponent_sum = np.sum(GTsim.config[GTsim.t - 10:GTsim.t],axis=0)[opponent_id]
        defect_prob = opponent_sum/10
        if np.random.random() <= defect_prob:
            return 1
        else:
            return 0

def net_niet_helemaal_eerlijk(GTsim, player_id):
    opponent_id = 1 - player_id
    if GTsim.t == 0:
        return 0
    
    if GTsim.t < 10:
        opponent_sum = np.sum(GTsim.config[:GTsim.t], axis=0)[opponent_id]
        defect_prob = opponent_sum/GTsim.t
        if np.random.random() <= defect_prob:
            return 1
        else:
            return 0
    else:
        opponent_sum = np.sum(GTsim.config[GTsim.t - 10:GTsim.t],axis=0)[opponent_id]
        defect_prob = (opponent_sum/10)*1.25
        if np.random.random() <= defect_prob:
            return 1
        else:
            return 0
