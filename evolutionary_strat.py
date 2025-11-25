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

def gen_random_strat(depth):
    strat = []
    for _ in range(4^depth + depth):
        strat.append(np.random.randint(0, 2))
    
    return strat

def mutate_strat(strat, mutation_probability = 0.05):
    new_strat = strat

    for move_i in range(len(strat)):
        if np.random.random() < mutation_probability:
            new_strat[move_i] = 1 - new_strat[move_i]
    
    return new_strat

def evolve_new_strat(strats):
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


def evolve_new_strat_list(strats, n_strats_in_evo = 5, n_evolved_strats = 5, n_mutated_strats = 2):
    """
    take a list of strats to be tested and evolved. Return an evevolved list of strats.

    n_strats_in_evo: how many strats are included as top-strats in the evolutionary production of a new strat
    n_evolved_strats: how many new strats are evolved in every iteration
    n_mutated_strats: how many times is each strat mutated in every iteration.

    returns 
    evolved_strats: the list of evolved strats, with the best strat as the final element
    top_scores[0]: the score of the best strat
    """

    if n_strats_in_evo > len(strats):
        n_strats_in_evo = len(strats)

    strats_scores = []

    # run a tournament for every strat in strats, save the final scores in strats_scores
    for strat in strats:
        tourney_final_score = gtm.tournament(strat)
        strats_scores.append(tourney_final_score)
    
    # get the top 5 scores and their corresponding strats, save in top_scores and top_strats
    # strats are ordered best-worst
    top_scores = sorted(strats_scores)[:n_strats_in_evo]
    top_strats_indexes = [strats_scores.index(score) for score in top_scores]
    top_strats = [strats[i] for i in top_strats_indexes]

    # generate n_evolved_strats new strats by evolution
    evolved_strats = []
    for _ in range(n_evolved_strats):
        evolved_strats.append(evolve_new_strat(top_strats))
    
    # generate n_mutated_strats new strats by mutation
    for strat in strats:
        for _ in range(n_mutated_strats):
            evolved_strats.append(mutate_strat(strat))
    
    # include the best performing strat in evolved_strats as is
    evolved_strats.append(top_strats[0])

    return evolved_strats, top_scores[0]

def evolutionary_algorithm(depth, max_iter = np.inf, convergence_iteration = 40, n_strats_in_evo = 5, n_evolved_strats = 5, n_mutated_strats = 2):
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
    for _ in range(n_evolved_strats * (n_mutated_strats + 1)):
        strats.append(gen_random_strat(depth))
    
    conv_iter = 0
    while conv_iter < convergence_iteration:
        # evolve the strats
        new_strats, top_score = evolve_new_strat_list(strats, n_strats_in_evo, n_evolved_strats, n_mutated_strats)
        if top_score > best_score:
            best_strat = new_strats[-1]
            best_score = top_score
            conv_iter = 0
        else:
            conv_iter += 1

        if tot_iterations == max_iter:
            break
        
        sys.stdout.write(f"\rCurrent iteration: {tot_iterations} || top score: {best_score}")
        sys.stdout.flush()
        tot_iterations += 1
    
    return best_strat

print(evolutionary_algorithm(2))
