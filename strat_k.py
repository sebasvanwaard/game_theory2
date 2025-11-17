import numpy as np
import matplotlib.pyplot as plt

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


def fitting(game_history, player_id):
    other_player_id = 1 - player_id
    length = len(game_history)
    # First move nice
    if length == 0:
        return 0
    N = 50
    # tit for tat until N
    if length < N:
        return game_history[-1][other_player_id]
    else:
        time = np.arange(length)
        data = [np.sum(game_history[i:], axis=0)[other_player_id] for i in length]
        coeff = np.fit(time, data, 2)

sample = [1,1,1,1,0,1,0,0,1,1,0,0,1,1,0,0,1,1]

length = len(sample)
time = np.arange(length)

data = []
for i in range(length):
    data.append(np.sum(sample[:i]))

polyfit = np.polyfit(time, data, 2)

new_time = time+len(time)

plt.plot(time, data)
plt.plot(time, polyfit[2] + polyfit[1]* time + polyfit[0] * time**2)
plt.plot(new_time, polyfit[2] + polyfit[1]* new_time + polyfit[0] * new_time**2)
plt.show()