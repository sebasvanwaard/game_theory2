import numpy as np
import GT_model as gtm

import sys

"""
evolution is based on the 5 best performing strats. In which the best strat has a 50% chance of transfering their move, second best 25%, third 12.5% etc.

strat format:
- The first 2^d (d=depth) elements of the strat list encode for the different situations in binary. E.g.
- An additional d elements of the list are added to encode the first t iterations in which t < depth 
(because you cannot make valid assumptions about the nature of any moves that haven't happened yet.)
The additional moves are essentially the first d initial moves.
"""

class EvoAlgorithm():
    def __init__(self):
        """
        Class to run an evolutionary algorithm. Every evolution a certain amount of new strats is evolved (n_evolved_strats). 
        This is done based on x amount of top performing strats (can be set with n_strats_in_evo).
        An additional x amount of strats is mutated per evolved strat (n_mutated_strats). So the amount of mutated strats is equal to
        n_evolved_strats * n_mutated_strats. Total amount of new strats that is generated each iteration is n_evolved_strats * (n_mutated_strats + 1).
        
        parameters:
        n_strats_in_evo: the amount of top performing strats used in evolution
        n_evolved_strats: the amount of new strats that is produced in evolution
        n_mutated_strats: the amount of new strats that is mutated, per evolved strat
        mutation_probability: the probability of a mutation happening for a certain game_state. 
                            For larger depths this value might have to be higher.
        
        depth: the amount of gamestates the evolution looks in the past to base its decisions on
        max_iter: the maximum amount of iterations of the entire evolution algorithm, mostly useful for testing
        convergence_iteration: the amount of iterations to keep looking for a better strat after not finding a better one.                    
        """

        self.n_strats_in_evo = 5
        self.n_evolved_strats = 5
        self.n_mutated_strats = 2
        self.mutation_probability = 0.05

        self.depth = 2
        self.max_iter = np.inf
        self.convergence_iteration = 40

    def gen_random_strat(self):
        strat = []
        for _ in range(4**self.depth + self.depth):
            strat.append(np.random.randint(0, 2))
        
        return strat

    def mutate_strat(self, strat):
        new_strat = strat

        for move_i in range(len(strat)):
            if np.random.random() < self.mutation_probability:
                new_strat[move_i] = 1 - new_strat[move_i]
        
        return new_strat

    def evolve_new_strat(self, strats):
        """
        Take a list of strats and evolve them.
        evolution is based on the 5 best performing strats. In which the best strat has a 50% chance of transfering their move, second best 25%, third 12.5% etc.
        """
        new_strat = []

        for move_i in range(len(strats[0])):
            new_move = -1
            for strat in reversed(strats):
                if np.random.random() < 0.5:
                    new_move = strat[move_i]
            
            # if all strats fail to transfer their move, use best strat move
            if new_move == -1:
                new_move = strats[0][move_i]

        return new_strat


    def evolve_new_strat_list(self, strats):
        """
        take a list of strats to be tested and evolved. Return an evevolved list of strats.

        n_strats_in_evo: how many strats are included as top-strats in the evolutionary production of a new strat
        n_evolved_strats: how many new strats are evolved in every iteration
        n_mutated_strats: how many times is each strat mutated in every iteration.

        returns 
        evolved_strats: the list of evolved strats, with the best strat as the final element
        top_scores[0]: the score of the best strat
        """

        if self.n_strats_in_evo > len(strats):
            self.n_strats_in_evo = len(strats)

        strats_scores = []

        # run a tournament for every strat in strats, save the final scores in strats_scores
        for strat in strats:
            tourney_final_score = gtm.tournament(strat)
            strats_scores.append(tourney_final_score)
        
        # get the top 5 scores and their corresponding strats, save in top_scores and top_strats
        # strats are ordered best-worst
        top_scores = sorted(strats_scores)[:self.n_strats_in_evo]
        top_strats_indexes = [strats_scores.index(score) for score in top_scores]
        top_strats = [strats[i] for i in top_strats_indexes]

        # generate n_evolved_strats new strats by evolution
        evolved_strats = []
        for _ in range(self.n_evolved_strats):
            evolved_strats.append(self.evolve_new_strat(top_strats))
        
        # generate n_mutated_strats new strats by mutation
        for strat in strats:
            for _ in range(self.n_mutated_strats):
                evolved_strats.append(self.mutate_strat(strat))
        
        # include the best performing strat in evolved_strats as is
        evolved_strats.append(top_strats[0])

        return evolved_strats, top_scores[0]

    def execute(self):
        """
        Function to run an evolutionary algorithm that finds the best strat for a prisoners dillemma. The strat will look "depth" moves in the past
        to base its next move on.

        convergence_iterations: the amount of times to keep iterating after the top_strats score does not improve.

        generate a random list of strats, this list should be longer than n_strats_in_evo
        keep track of the best strat, and its score
        
        evolve the list of strats

        as long as the best strat is still improving keep evolving

        after convergence, return the best strat
        """

        tot_iterations = 0

        best_strat = None
        best_score = -1
        strats = []

        # generate a list of random strats. Will generate the amount of strats that the evolution function evolves
        for _ in range(self.n_evolved_strats * (self.n_mutated_strats + 1)):
            strats.append(self.gen_random_strat())
        
        conv_iter = 0
        while conv_iter < self.convergence_iteration:
            # evolve the strats
            new_strats, top_score = self.evolve_new_strat_list(strats)
            if top_score > best_score:
                best_strat = new_strats[-1]
                best_score = top_score
                conv_iter = 0
            else:
                conv_iter += 1

            if tot_iterations == self.max_iter:
                break
            
            sys.stdout.write(f"\rCurrent iteration: {tot_iterations} || top score: {best_score}")
            sys.stdout.flush()
            tot_iterations += 1
        
        return best_strat, best_score


def print_results(strats, scores):
    """
    Print the leaderboards of found strats, best strat takes the win
    """
    strats = np.array(strats)
    scores  = np.array(scores)
    strats_and_scores = np.column_stack((strats, scores))
    sorted_sas = strats_and_scores[strats_and_scores[:, 1].astype(int).argsort()[::-1]]
    
    print("\n\nFinal strat leaderboard\npos | strat | total points")
    for i in range(sorted_sas.shape[0]):
        print(f"#{i + 1} | {sorted_sas[i][0]} | {sorted_sas[i][1]}")



if __name__ == '__main__':
    n_strats = 5
    best_strats = []
    best_scores = []
    
    evo = EvoAlgorithm()
    evo.convergence_iteration = 5
    evo.depth = 1
    evo.max_iter = 10

    for _ in range(n_strats):
        best_strat, best_score = evo.execute()
        best_strats.append(str(best_strat))
        best_scores.append(best_score)
    
    # print(best_strats, best_scores)
    
    print_results(best_strats, best_scores)




