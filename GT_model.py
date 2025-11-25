from pyics import Model
import numpy as np
import matplotlib.pyplot as plt

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
    length = GTsim.t
    if length == 0:
        return 0
    if player_id == 0:
        return GTsim.config[length-1][1]
    else:
        return GTsim.config[length-1][0]
    
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
                              "weighted_decision": strat_k.weighted_decision, "fitting": strat_k.fitting,
                              "tat_for_tit": strat_k.tat_for_tit, "thrower": bassies_strats.thrower,
                              "copy_cat": bassies_strats.copy_cat, "cry_baby": bassies_strats.easy_on_je_little_toes_gestept,
                              "eerlijk": bassies_strats.eerlijk, "minder_eerlijk": bassies_strats.net_niet_helemaal_eerlijk}
        

        # silent = 0, testify = 1
        # punishment/reward [p1_rew, p2_rew] i=0: both silent, i=1: p1-silent || p2-testify, i=2 p1-testify || p2-silent, i=3: both testify
        self.rewards = [[3, 3], [0, 5], [5, 0], [1, 1]]

    def setter_strat():
        included_strats = []
        pass

    def execute_strat(self, strat):
        # Check the amount of steps we want to look back
        dim = int(np.emath.logn(4, len(strat)))
        if self.t < dim:
            return 0
        else:
            # Joined is a list of the history with [move1p1, move1p2, m2p1, m2p2, ....]
            moves = self.config[self.t-dim : self.t]
            joined = [0,0]
            for m in moves:
                joined += m
            
            # Gets the index of the history in the strat moveset and return next move
            next_move_index = state_to_dec(joined[:2])
            return strat[next_move_index]


    def reset(self):
        self.t = 0
        self.config = np.zeros((self.height, self.width))
        self.live_scores = np.array([[0,0]])

    def step(self, evostrat = None):
        self.t += 1
        if self.t >= self.height:
            return True
        
        if evostrat != None:
            move_1 = self.execute_strat(evostrat)
        else:
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


# for _ in range(500):
#     sim.step()

# from pyics import GUI
# cx = GUI(sim)
# cx.start()

#print(sim.list_to_strat([0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1]))


def list_to_strat(self, list):
        length = len(list)
        steps_back = np.emath.logn(4, length)
        hisitory = self.config()


def battle(sim, strat1, strat2, n=50):
    # Reset config for battle
    sim.reset()

    # Check if strat1 is a type list
    if isinstance(strat1, list):
        sim.p2_strat = strat2
        for _ in range(n):
            sim.step(strat1)
        return sim.live_scores[-1]

    # Runs battle for two string strategies
    else:
        # Set strats
        sim.p1_strat = strat1
        sim.p2_strat = strat2

        # Run the battle for n steps and return score
        for _ in range(n):
            sim.step()
        return sim.live_scores[-1]


def tournament(strat):
    sim = GTsim()
    sim.reset()
    scores = []
    bib = sim.strat_library
    for key in bib.keys():
        points = battle(sim, strat, key)
        scores.append(points[0])
    return sum(scores)


sim = GTsim()
# print(battle(sim, [0,0,0,0], "tit_for_tat"))

lijstje = []
strats = sim.strat_library.keys()
for s in strats:
    lijstje.append(tournament(s))

plt.figure(figsize=(12,8))

plt.plot(strats, lijstje)
plt.show()

# print(tournament([0,0,0,0]))