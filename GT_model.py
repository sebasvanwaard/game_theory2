from pyics import Model

class GTsim(Model):

    def __init__(self):
        self.make_param("p1_strat", setter=self.setter_strat)
        p1_strat = []
        self.p2_strat = []

        # history is saved in list of list, every sublist is a gamestate [p1, p2] 0=silent 1=testify
        # intial state
        self.game_history = []

        # punishment/reward [p1_rew, p2_rew] i=0: both silent, i=1: p1-silent || p2-testify, i=2 p1-testify || p2-silent, i=3: both testify
        self.rewards = [[-1, -1], [-3, 0], [0, -3], [-2, -2]]
        self.t = 0

    def setter_strat():
        pass
    

    def make_strat(self):
        pass

    def step(self):
        pass

    def reset(self):
        pass

    def draw(self):
        pass
