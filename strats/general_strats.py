import numpy as np

def tit_for_tat(GTsim, player_id):
    """
    tit_for_tat strategy

    :param GTsim: Model
    :param player_id: player id in the match
    """
    length = GTsim.t
    if length == 0:
        return 0
    if player_id == 0:
        return GTsim.config[length - 1][1]
    else:
        return GTsim.config[length - 1][0]


def random(GTsim, player_id):
    """
    random strategy

    :param GTsim: Model
    :param player_id: player id in the match
    """
    return np.random.randint(0, 2)
