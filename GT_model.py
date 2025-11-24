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
    
def random(GTsim, player_id):
    return np.random.randint(0,2)

class GTsim(Model):

    def __init__(self):
        Model.__init__(self)

        self.make_param("p1_strat", "random")
        self.make_param("p2_strat", "random")
        self.make_param("height", 50)
        
        self.t = 0
        self.width = 2
        self.config = None
        self.live_scores = None

        self.strat_library = {"tit_for_tat": tit_for_tat, "random": random,
                              "traitor": bassies_strats.traitor, "how_mean": strat_k.how_mean,
                              "weighted_decision": strat_k.weighted_decision, "fitting": strat_k.fitting}
        

        # silent = 0, testify = 1
        # punishment/reward [p1_rew, p2_rew] i=0: both silent, i=1: p1-silent || p2-testify, i=2 p1-testify || p2-silent, i=3: both testify
        self.rewards = [[1, 1], [-3, 0], [0, -3], [-2, -2]]

    def setter_strat():
        included_strats = []
        pass

    def reset(self):
        self.t = 0
        self.config = np.zeros((self.height, self.width))
        self.live_scores = np.array([[0,0]])

    def step(self):
        self.t += 1
        if self.t >= self.height:
            return True
        
        move_1 = self.strat_library[self.p1_strat](self, 0)
        move_2 = self.strat_library[self.p2_strat](self, 1)
        self.config[self.t-1] = np.array([move_1, move_2])

        new_score = np.array([self.rewards[state_to_dec(self.config[self.t-1])][0],
                                  self.rewards[state_to_dec(self.config[self.t-1])][1]])

        self.live_scores = np.vstack([self.live_scores, (self.live_scores[-1,:] + np.array(new_score))])


    def draw(self):
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        if self.t >= self.height:
            return

        plt.clf()
        time = np.arange(self.t+1)

        plt.subplot(2, 1, 1)
        plt.plot(time, self.live_scores[:,0], c='blue', label = "Player 1")
        plt.plot(time, self.live_scores[:,1], c='red', label = "Player 2")

        plt.title("Players scores over time and move history")
        plt.xlabel("timestep")
        plt.ylabel("Score")
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 1, 2)
        im = plt.imshow(self.config.T, cmap="RdYlGn")
        values = [0,1]
        colors = [im.cmap(im.norm(value)) for value in values]
        patches = [mpatches.Patch(color=colors[0], label = "Silent"), mpatches.Patch(color=colors[1], label = "Talk")]
        plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )

        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()

sim = GTsim()

# for _ in range(500):
#     sim.step()

from pyics import GUI
cx = GUI(sim)
cx.start()