import numpy as np
import pandas as pd

import strats.bassies_strats as bassies_strats
import strats.strat_k as strat_k
import strats.general_strats as general_strats
from pyics import Model


def state_to_dec(inp):
    """
    Convert a list of binary digits to their base 10 equivalent

    :param inp: list of binary digits
    """
    base_10 = 0

    for inp_i in range(0, len(inp)):
        base_10 += (int(inp[inp_i]) * 2**(len(inp) - 1 - inp_i))

    return base_10

class GTsim(Model):
    """
    Simulation of two strategies playing agains eachother
    """

    def __init__(self):
        Model.__init__(self)
        """
        p1_strat = the dictionary string value of the strat p1 should use
        p2_strat = the dictionary string value of the strat p1 should use
        height = the amount of games played in a matchup

        t = time in simulations, should not be tampered with outside of class
        width = the amount of choices per player per timepoint (for prisoners dilemma should always be 2)
        config = the moves per timepoint
        rewards = the rewards that awarded to the players at different dicisions
        live_scores = the cumulative scores per timepoint t for both players [score_p1, score_p2]
        """

        # Adjustable parameters
        self.make_param("p1_strat", "random")
        self.make_param("p2_strat", "random")
        self.make_param("height", 50)

        # config parameters
        self.t = 0
        self.width = 2
        self.config = None

        # silent = 0, testify = 1
        # punishment/reward [p1_rew, p2_rew]
        # for rewards the indexes correspond to:
        # i=0: both silent || i=1: p1-silent, p2-testify || i=2 p1-testify, p2-silent || i=3: both testify || 
        self.rewards = [[3, 3], [0, 5], [5, 0], [1, 1]]

        self.live_scores = None

        self.strat_library = {"tit_for_tat": general_strats.tit_for_tat,
                              "random": general_strats.random,
                              "traitor": bassies_strats.traitor,
                              "how_mean": strat_k.how_mean,
                              "weighted_decision": strat_k.weighted_decision,
                              "fitting": strat_k.fitting,
                              "tat_for_tit": strat_k.tat_for_tit,
                              "thrower": bassies_strats.thrower,
                              "copy_cat": bassies_strats.copy_cat,
                              "cry_baby": bassies_strats.easy_on_je_little_toes_gestept,
                              "eerlijk": bassies_strats.eerlijk,
                              "minder_eerlijk": bassies_strats.net_niet_helemaal_eerlijk}

    def execute_strat(self, strat):
        """
        For a list strategy (from the evolutionary strategy) execute the move from the moveset
        depending on the history

        :param self: Model
        :param strat: moveset list of the strategy
        """
        # Check the amount of steps we want to look back
        dim = int(np.emath.logn(4, len(strat)))
        if self.t < dim:
            return 0
        else:
            # Joined is a list of the history with [move1p1, move1p2, m2p1,
            # m2p2, ....]
            moves = self.config[self.t - dim: self.t]
            joined = [0, 0]
            for m in moves:
                joined += m

            # Gets the index of the history in the strat moveset and return
            # next move
            next_move_index = state_to_dec(joined)
            return strat[next_move_index]

    def reset(self):
        """
        Resets the model
        
        :param self: Model
        """
        self.t = 0
        self.config = np.zeros((self.height, self.width))
        self.live_scores = np.array([[0, 0]])

    def step(self, evostrat1=None, evostrat2=None):
        """
        Does a step in the simulation, also checks if we have an evolutionary strat by checking
        if there is another input given
        
        :param self: Model
        :param evostrat: moveset list of the evolutionary strategy
        """
        self.t += 1
        if self.t >= self.height:
            return True

        if evostrat1 is not None:
            move_1 = self.execute_strat(evostrat1)
        if evostrat2 is not None:
            move_2 = self.execute_strat(evostrat2)
        else:
            move_1 = self.strat_library[self.p1_strat](self, 0)
            move_2 = self.strat_library[self.p2_strat](self, 1)
        self.config[self.t - 1] = np.array([move_1, move_2])

        new_score = np.array([self.rewards[state_to_dec(self.config[self.t - 1])][0],
                              self.rewards[state_to_dec(self.config[self.t - 1])][1]])

        self.live_scores = np.vstack(
            [self.live_scores, (self.live_scores[-1, :] + np.array(new_score))])

    def draw(self):
        """
        Draws a plot of the simulation scoring of the two strategies against the time, also
        shows the moveset of both strategies in a bar below
        
        :param self: Model
        """
        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt

        if self.t >= self.height:
            return

        plt.clf()
        time = np.arange(self.t + 1)

        plt.subplot(2, 1, 1)
        plt.plot(time, self.live_scores[:, 0], c='blue', label="Player 1")
        plt.plot(time, self.live_scores[:, 1], c='red', label="Player 2")

        plt.title("Players scores over time and move history")
        plt.xlabel("timestep")
        plt.ylabel("Score")
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 1, 2)
        im = plt.imshow(self.config.T, cmap="RdYlGn")
        values = [0, 1]
        colors = [im.cmap(im.norm(value)) for value in values]
        patches = [
            mpatches.Patch(
                color=colors[0],
                label="Silent"),
            mpatches.Patch(
                color=colors[1],
                label="Talk")]
        plt.legend(
            handles=patches,
            bbox_to_anchor=(
                1.05,
                1),
            loc=2,
            borderaxespad=0.)

        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()


def battle(sim, strat1, strat2):
    """
    Does a battle between two strategies and gives the final score afther n moves
    
    :param sim: Model
    :param strat1: first strategy
    :param strat2: second strategy
    :param n: duration of the battle between the strategies
    """
    # Reset config for battle
    sim.reset()

    # Check if strat1 is a type list
    if isinstance(strat1, list):
        if isinstance(strat2, list):
            for _ in range(sim.height):
                sim.step(strat1, strat2)
            return sim.live_scores[-1]
        else:
            sim.p2_strat = strat2
            for _ in range(sim.height):
                sim.step(strat1)
            return sim.live_scores[-1]
    
    # Check if strat2 is a type list
    if isinstance(strat2, list):
        sim.p2_strat = strat1
        for _ in range(sim.height):
            sim.step(strat2)
        return sim.live_scores[-1]

    # Runs battle for two string strategies
    else:
        # Set strats
        sim.p1_strat = strat1
        sim.p2_strat = strat2

        # Run the battle for n steps and return score
        for _ in range(sim.height):
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

def result_matrix(sim, evostrat=False):
    """
    Create a result matrix of battles between strategies.
    
    :param sim: Model
    :param evostrat: Moveset list of the evolutionary strategy
    :return: Matrix with results of every battle
    :rtype: DataFrame
    """
    # Strategy labels
    strat_labels = list(sim.strat_library.keys())
    # Strategy objects used in battle
    strat_objects = list(sim.strat_library.keys())
    
    # Add the evolutionary strategy if there
    if evostrat:
        strat_labels.append("evostrat")   # DataFrame label
        strat_objects.append(evostrat)    # actual object used in battle

    n = len(strat_labels)
    result = np.zeros((n, n))

    # Fill matrix with battle results
    for i, s1 in enumerate(strat_objects):
        for j, s2 in enumerate(strat_objects):
            result[i, j] = battle(sim, s1, s2)[0]

    # Create DataFrame with labels
    df = pd.DataFrame(result, index=strat_labels, columns=strat_labels)
    df["Total"] = df.sum(axis=1)

    # Sort rows by Total, get this order and reorder columns adding total as last
    df = df.sort_values("Total", ascending=False)
    new_order = df.index.tolist()
    df = df[new_order + ["Total"]]

    return df

evostrat1 = [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1,
            0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0,
            1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

evostrat2 = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
             1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1,
             0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0]

evostrat3 = [0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1,
             1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0,
             1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0,
             0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1,
             1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1,
             0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1,
             1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1,
             0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0,
             0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0,
             0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1,
             1, 1, 1, 0, 0, 0, 1, 0, 1, 0]

# sim = GTsim()
# sim.height = 200

# df = result_matrix(sim, evostrat1)
# # df.to_csv('test.csv')
# print(df)
