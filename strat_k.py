import numpy as np
import matplotlib.pyplot as plt


def how_mean(GTsim, player_id):
    """
    Checks how mean the other player is by looking how many time the other player has talked,
    then dividing by the length of the game and when the mean is over 0.5 we also talk, otherwise stay silent
    """
    other_player_id = 1 - player_id
    length = GTsim.t
    # First moves nice
    if length < 3:
        return 0
    meanie = np.sum(GTsim.config, axis=0)[other_player_id]
    meanie /= length
    if meanie > 0.5:
        return 1
    else:
        return 0


def weighted_decision(GTsim, player_id):
    """
    Based on the simulation scoring, we decide the weights of how many times we should talk and how many times we should stay silent,
    Then picks random based on these weights
    """
    scoring = GTsim.rewards

    #Calculate the weights for staying silent
    weights = [w[0] for w in scoring]
    print(weights)
    silent = weights[0] + weights[1]
    total = sum(weights)
    w = silent/total

    # Random choice
    choice = np.random.choice([0,1], 1, p=[w, 1-w])[0]
    return choice


def fitting(GTsim, player_id):
    """
    Fit polynomial to sum of other player's previous moves, depending on the coefficient of second order term we decide next move
    """
    other_player_id = 1 - player_id
    length = GTsim.t
    # First moves nice
    if length < 4:
        return 0
    
    # Make time axis and sum axis
    time = np.arange(length)
    data = [np.sum(GTsim.config[:i], axis=0)[other_player_id] for i in range(length)]

    # Fit polynomial degree 2
    coeff = np.polyfit(time, data, 2)
    lead = coeff[0]

    # If lead > 0 we see an increase in how mean the other player is getting otherwise it is getting nicer
    if lead > 0:
        return 1
    else:
        return 0


def tat_for_tit(GTsim, player_id):
    """
    Inverse of tit for tat 2 moves back, so starts mean, when other player was nice 2 moves ago be mean, when other player was mean be nice
    """
    other_player_id = 1 - player_id
    length = GTsim.t
    if length < 2:
        return 1
    else:
        other_move = GTsim.config[length - 2][other_player_id]
        return 1 - other_move


