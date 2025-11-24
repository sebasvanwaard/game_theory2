import numpy as np
import matplotlib.pyplot as plt


def how_mean(GTsim, player_id):
    """
    Checks how mean the other player is by looking how many time the other player has talked,
    then dividing by the length of the game and when the mean is over 0.5 we also talk, otherwise stay silent
    """
    other_player_id = 1 - player_id
    length = len(GTsim.game_history)
    # First move nice
    if length == 0:
        return 0
    N = 10
    # tit for tat until N
    if length < N:
        return GTsim.game_history[-1][other_player_id]
    else:
        meanie = np.sum(GTsim.game_history, axis=0)[other_player_id]
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
    other_player_id = 1 - player_id
    scoring = GTsim.rewards

    #Calculate the weights for staying silent
    weights = [w[0] for w in scoring]
    silent = sum(weights[:2])
    total = sum(weights)
    w = silent/total

    # Random choice
    choice = np.random.choice([0,1], [w, 1-2])
    return choice


    



# def fitting(game_history, player_id):
#     other_player_id = 1 - player_id
#     length = len(game_history)
#     # First move nice
#     if length == 0:
#         return 0
#     N = 50
#     # tit for tat until N
#     if length < N:
#         return game_history[-1][other_player_id]
#     else:
#         time = np.arange(length)
#         data = [np.sum(game_history[i:], axis=0)[other_player_id] for i in length]
#         coeff = np.fit(time, data, 2)

# sample = [1,1,1,1,0,1,0,0,1,1,0,0,1,1,0,0,1,1]

# length = len(sample)
# time = np.arange(length)

# data = []
# for i in range(length):
#     data.append(np.sum(sample[:i]))

# polyfit = np.polyfit(time, data, 2)

# new_time = time+len(time)

# plt.plot(time, data)
# plt.plot(time, polyfit[2] + polyfit[1]* time + polyfit[0] * time**2)
# plt.plot(new_time, polyfit[2] + polyfit[1]* new_time + polyfit[0] * new_time**2)
# plt.show()