from pyics import Model
import bassies_strats

def state_to_dec(inp):
    """
    Convert a 
    """
    base_10 = 0

    for inp_i in range(0, len(inp)):
        base_10 += (int(inp[inp_i]) * 2**(len(inp) - 1 - inp_i))
    
    return base_10

def tit_for_tat(game_history, player_id):
    if len(game_history) == 0:
        return 0
    if player_id == 0:
        return game_history[-1][1]
    else:
        return game_history[-1][0]

class GTsim(Model):

    def __init__(self):
        Model.__init__(self)

        self.make_param("p1_strat", "traitor")
        self.make_param("p2_strat", "tit_for_tat")

        self.strat_library = {"tit_for_tat": tit_for_tat,
                              "traitor": bassies_strats.traitor}
        self.p1_score = 0
        self.p2_score = 0

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
        self.game_history.append([self.strat_library[self.p1_strat](self.game_history, 0), 
                                  self.strat_library[self.p1_strat](self.game_history, 1)])
        self.score_history.append([self.rewards[state_to_dec(self.game_history[-1])][0],
                                  self.rewards[state_to_dec(self.game_history[-1])][1]])

    def reset(self):
        self.game_history = []

    def draw(self):
        pass

sim = GTsim()

for _ in range(10):
    sim.step()
print(sim.game_history)
print(sim.score_history)