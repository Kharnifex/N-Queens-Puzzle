import random
from scipy import special
import itertools

def generate_population(nqueens, popsize):
    #function that initializes a list with possible positions for the queens
    population=[]
    for individual in range(popsize):
        new=[random.randrange(nqueens) for index in range(nqueens)]
        population.append(new)
    return population

def print_check_goal(population, nqueens):
    #function that prints each generation's score and checks whether the problem has been solved
    for ind in population:
        score = fitness_score(ind, nqueens)
        print(str(ind) +  "Fitness score: " + str(score))
        if score==special.comb(nqueens, 2):
            print('Solution found')
            return True
    print("Solution not Found")
    return False

def fitness_score(seq, nqueens):
    #simple function that calculates fitness score
    score=0
    for row in range(nqueens):
        col=seq[row]
        for other_row in range(nqueens):
            if other_row == row:
                continue
            if seq[other_row] == col:
                continue
            if other_row + seq[other_row] == row + col:
                continue
            if other_row - seq[other_row] == row - col:
                continue
            #score+=1 if two queens dont threaten one another
            score+=1
    #score/2 because each pair of queens appears twice
    return score/2

def selection(population, nqueens):
    #function that selects parents using probabilities
    parents = []
    for ind in population:
        if random.randrange(special.comb(nqueens, 2)*2) < fitness_score(ind, nqueens):
            parents.append(ind)
    return parents

def crossover(parents, nqueens, mixingnum):
    #random index is chosen
    crosspoints = random.sample(range(nqueens), mixingnum - 1)
    offsprings = []
    #we use permutations with 2 as its 2nd argument so we get random combinations of 2 of parents' elements
    permutationslist = list(itertools.permutations(parents, mixingnum))
    for perm in permutationslist:
        offspring = []
        start_pt = 0 #initialize index "pointer"
        for parent_idx, cross_point in enumerate(crosspoints): #does not run for last parent
            parent_part = perm[parent_idx][start_pt:cross_point]
            #for each parent, their offspring is added to the offspring list
            offspring.append(parent_part)
            start_pt = cross_point
        #we basically do the same that's in the for loop but for the last parent
        last_parent = perm[-1]
        parent_part = last_parent[cross_point:]
        offspring.append(parent_part)
        #we add all offsprings to the offspring list for each perm
        offsprings.append(list(itertools.chain(*offspring)))
    return offsprings

def mutate(seq, nqueens, mutaterate):
    #mutation function, random.random() returns value from 0 to 1 so if mutaterate>1 then mutations always happen and if mutaterate<0 they never happeb
    for row in range(len(seq)):
        if random.random() < mutaterate:
            seq[row] = random.randrange(nqueens)
    return seq

def evolution(population, nqueens, popsize):
    #we use selection() to choose parents
    parents = selection(population, nqueens)
    #we use crossover() to find children
    offsprings = crossover(parents, nqueens, 2)
    #we use mutate() with mutaterate=0.1 (can change) to give this generation a chance of mutating
    offsprings = [mutate(x, nqueens, 0.1) for x in offsprings]
    #we put the previous and next generation to new_gen so we can keep the individiuals with the highest fitness_score
    new_gen = offsprings
    for ind in population:
        new_gen.append(ind)
    #a sorted, n=popsize sized list that uses descending order of fitness score is returned
    new_gen = sorted(new_gen, key=lambda ind: fitness_score(ind, nqueens), reverse=True)[:popsize]
    return new_gen
