from pyics import Model
import numpy as np

import bassies_strats
import strat_k

def state_to_dec(inp):
    """
    Convert a 
    """
    base_10 = 0

    for inp_i in range(0, len(inp)):
        base_10 += (int(inp[inp_i]) * 2**(len(inp) - 1 - inp_i))
    
    return base_10

def tit_for_tat(GTsim, player_id):
    if len(GTsim.game_history) == 0:
        return 0
    if player_id == 0:
        return GTsim.game_history[-1][1]
    else:
        return GTsim.game_history[-1][0]

class GTsim(Model):

    def __init__(self):
        Model.__init__(self)

        self.make_param("p1_strat", "traitor")
        self.make_param("p2_strat", "traitor")

        self.strat_library = {"tit_for_tat": tit_for_tat,
                              "traitor": bassies_strats.traitor, "test": strat_k.test}
        
        # live score feed i=0: p1 score, i=1: p2 score
        self.live_scores = np.array([0,0])

        # history is saved in list of list, every sublist is a gamestate [p1, p2] 0=silent 1=testify. Gamestates are chronologically saved
        # intial state
        self.game_history = []
        self.score_history = []

        # silent = 0, testify = 1
        # punishment/reward [p1_rew, p2_rew] i=0: both silent, i=1: p1-silent || p2-testify, i=2 p1-testify || p2-silent, i=3: both testify
        self.rewards = [[-1, -1], [-3, 0], [0, -3], [-2, -2]]

    def setter_strat():
        included_strats = []
        pass

    def step(self):
        self.game_history.append([self.strat_library[self.p1_strat](self, 0), 
                                  self.strat_library[self.p2_strat](self, 1)])

        new_score = [self.rewards[state_to_dec(self.game_history[-1])][0],
                                  self.rewards[state_to_dec(self.game_history[-1])][1]]

        self.score_history.append(new_score)
        self.live_scores += np.array(new_score)

    def reset(self):
        self.game_history = []

    def draw(self):
        pass

sim = GTsim()

for _ in range(500):
    sim.step()

final_scores = np.sum(sim.score_history, axis = 0)

# print(sim.game_history)
# print(sim.score_history)
print(sim.live_scores)
print(final_scores)