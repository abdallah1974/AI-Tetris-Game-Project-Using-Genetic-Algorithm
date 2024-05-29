import pygame
import random
import numpy as np
import copy
import tetris_base as game
import tetris_ai as ai

SEED = 49
random.seed(SEED)
np.random.seed(SEED)
class Chromosome():
    def __init__(self, weights):
        self.weights = weights
        self.score = 0

    def calc_fitness(self, game_state):
        self.score = game_state[2]

    def calc_best_move(self, board, piece, show_game=False):

        best_X = 0
        best_R = 0
        best_Y = 0
        best_score = -100000

        num_holes_bef, num_blocking_blocks_bef = game.calc_initial_move_info(board)
        for r in range(len(game.PIECES[piece['shape']])):
            for x in range(-2, game.BOARDWIDTH - 2):
                movement_info = game.calc_move_info(board, piece, x, r, num_holes_bef, num_blocking_blocks_bef)
                if movement_info[0]:
                    movement_score = sum(w * movement_info[i] for i, w in enumerate(self.weights))
                    if movement_score > best_score:
                        best_score = movement_score
                        best_X = x
                        best_R = r
                        best_Y = piece['y']

        if show_game:
            piece['y'] = best_Y
        else:
            piece['y'] = -2

        piece['x'] = best_X
        piece['rotation'] = best_R

        return best_X, best_R

class GA:
    def __init__(self, num_pop, num_weights=7, lb=-10, ub=10):
        self.chromosomes = []

        for i in range(num_pop):
            weights = np.random.uniform(lb, ub, size=(num_weights))
            chrom = Chromosome(weights)
            self.chromosomes.append(chrom)

            # Evaluate fitness
            game_state = ai.run_game(self.chromosomes[i], 1000, 200000, True)
            self.chromosomes[i].calc_fitness(game_state)

    def __str__(self):
        for i, chromo in enumerate(self.chromosomes):
            print(f"   chromosome  {i+1}")
            print(f"   Weights: {chromo.weights}")
            print(f"   Score: {chromo.score}")

        return ''

    def selection(self, chromosomes):
        fitness = np.array([chrom.score for chrom in chromosomes])
        norm_fitness = fitness / fitness.sum()
        roulette_prob = np.cumsum(norm_fitness)

        pop_selected = []
        while len(pop_selected) < len(self.chromosomes):
            pick = random.random()
            for index, individual in enumerate(self.chromosomes):
                if pick < roulette_prob[index]:
                    pop_selected.append(individual)
                    break
        return pop_selected





    def crossover(self, selected_pop, cross_rate=0.4):
    
        new_pop = []
        pop_size = len(selected_pop)
        for i in range(0, pop_size - 1, 2):
            p1 = selected_pop[i]
            p2 = selected_pop[i + 1]
            R = random.random()
            if R < cross_rate:
                point = random.randint(1, len(p1.weights) - 1)
                c1_genes = np.concatenate([p1.weights[:point], p2.weights[point:]])
                c2_genes = np.concatenate([p2.weights[:point], p1.weights[point:]])
                new_pop.append(Chromosome(c1_genes))
                new_pop.append(Chromosome(c2_genes))
            else:
                
                new_pop.append(copy.deepcopy(p1))
                new_pop.append(copy.deepcopy(p2))

        if pop_size % 2 != 0:
            last_chromosome = selected_pop[-1]
            new_pop.append(copy.deepcopy(last_chromosome))

        return new_pop


    def mutation(self, chromosomes, mutation_rate):
        num_genes = len(chromosomes[0].weights)
        pop_size = len(chromosomes)
        total_genes = num_genes * pop_size
        num_mutations = int(mutation_rate * total_genes)
        for i in range(num_mutations):
            random_pos = random.randint(0, total_genes - 1)
            chr_index = random_pos // num_genes
            gene_index = random_pos % num_genes
            chromosomes[chr_index].weights[gene_index] = random.uniform(-10, 10)
        return chromosomes

    def replace(self, new_chromo):
        new_pop = sorted(self.chromosomes, key=lambda x: x.score, reverse=True)
        new_pop[-(len(new_chromo)):] = new_chromo

        random.shuffle(new_pop)
        self.chromosomes = new_pop


