import ga as ga
import tetris_base as game
# import analyser as analyser
import tetris_ai as ai
import argparse, copy
import pdb
import numpy as np
import matplotlib.pyplot as plt

def main(no_show_game):
    # GENERAL CONFIG
    GAME_SPEED     = 600
    NUM_GEN        = 10
    NUM_POP        = 15
    NUM_ITER        = 1000
    MUTATION_RATE  = 0.2
    CROSSOVER_RATE = 0.7
    MAX_SCORE      = 200000



    

    init_pop    = ga.GA(NUM_POP)        
    pop         = copy.deepcopy(init_pop)

    generations = []

    for g in range(NUM_GEN):
        print (' \n')
        print (' Generation: ', g)
        print (' \n')

        generations.append(copy.deepcopy(pop))

        selected_pop = pop.selection(pop.chromosomes)

        new_chromo = pop.crossover(selected_pop, cross_rate=CROSSOVER_RATE)
        new_chromo = pop.mutation(new_chromo,  mutation_rate=MUTATION_RATE)

        for i in range(NUM_POP):
            game_state = ai.run_game(new_chromo[i], GAME_SPEED, MAX_SCORE, no_show_game)
            new_chromo[i].calc_fitness(game_state)

        pop.replace(new_chromo)
        fitness = [chrom.score for chrom in pop.chromosomes]
        print(fitness)

        print(pop)



    best_score, best_weights = best(generations)
    plot(generations)
    return best_score,best_weights




def best(generations):
    experiment = []
    maxs = []
    best_weights = []

    for i, gen in enumerate(generations):
        max = 0
        for j in gen.chromosomes:
            if j.score > max:
                max = j.score
                max_gen = j
        maxs.append(max_gen)
            

    maxs = sorted(maxs, key=lambda x: x.score, reverse=True)

        

    max = maxs[0].score
    best_c = maxs[0].weights
        
    return max , best_c


def plot(generations):
    # print(generations)
    gens_names = []
    scores = [] 
        

    for i, gen in enumerate(generations):
        
        for j in gen.chromosomes:
            gens_names.append("Gen"+str(i))
            scores.append(j.score)
            
    # scores = [gen.score for gen in generations.chromosomes]
    
    plt.bar(gens_names , scores)
    plt.show() 
   

if __name__ == "__main__":

    # Train the model
    # best_score,best_chromos = main(True)
    # print(best_score)
    # print(best_chromos)
    # plot(best_chromos)
    # test the model
    chromo       = ga.Chromosome([-3.09157911 ,-2.62841855 ,-1.55125273 ,-8.82163329 ,-3.18884461  ,2.55447599, 9.56643249])
    game_state = ai.run_game(chromo, speed=500, max_score=10000, no_show=False)
    print(game_state)

# [ 0.97926142 -0.11750139  0.92433508 -0.88216333 -0.30884151  0.81990591
#   0.2013791 ]

# [-3.09157911 -2.62841855 -1.55125273 -8.82163329 -3.18884461  2.55447599
#   9.56643249]

# 23281

# [898, [246, 38, 3, 2], 18598, True]