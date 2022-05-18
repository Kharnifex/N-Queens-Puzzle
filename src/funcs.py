import random
from scipy import special
import itertools

def generate_population(nqueens, popsize):
    #sunarthsh pou kanei initialize mia lista me pithanes theseis twn queens
    population=[]
    for individual in range(popsize):
        new=[random.randrange(nqueens) for index in range(nqueens)]
        population.append(new)
    return population

def print_check_goal(population, nqueens):
    #sunarthsh pou typwnei to score gia kathe genia kai tsekarei an exei vrethei lush sto problhma
    for ind in population:
        score = fitness_score(ind, nqueens)
        print(str(ind) +  "Fitness score: " + str(score))
        if score==special.comb(nqueens, 2):
            print('Solution found')
            return True
    print("Solution not Found")
    return False

def fitness_score(seq, nqueens):
    #aplh sunarthsh upologismou fitness score
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
            #score+=1 an ena zeugari queens den apeilei h mia thn allh
            score+=1
    #score/2 dioti to kathe zeugari elegxetai 2 fores apo thn sunarthsh
    return score/2

def selection(population, nqueens):
    #sunarthsh epiloghs gonewn gia evolution mesw xrhshs pithanothtwn
    parents = []
    for ind in population:
        if random.randrange(special.comb(nqueens, 2)*2) < fitness_score(ind, nqueens):
            parents.append(ind)
    return parents

def crossover(parents, nqueens, mixingnum):
    #dialegoume random index
    crosspoints = random.sample(range(nqueens), mixingnum - 1)
    offsprings = []
    #xrhsimopoioume thn permutations me deutero orisma mixingnum=2 gia na paroume tous random sunduasmous 2 stoixiwn tou parents
    permutationslist = list(itertools.permutations(parents, mixingnum))
    for perm in permutationslist:
        offspring = []
        start_pt = 0 #kanoume initialize ton index "pointer"
        for parent_idx, cross_point in enumerate(crosspoints): #den trexei gia ton teleutaio gonea
            parent_part = perm[parent_idx][start_pt:cross_point]
            #gia kathe parent vazoume ola ta offspring tou sth lista offspring
            offspring.append(parent_part)
            start_pt = cross_point
        #kanoume sthn ousia to idio pou ginetai sto for loop gia ton teleutaio gonea
        last_parent = perm[-1]
        parent_part = last_parent[cross_point:]
        offspring.append(parent_part)
        #gia kathe perm vazoume ola ta offspring sth lista offsprings
        offsprings.append(list(itertools.chain(*offspring)))
    return offsprings

def mutate(seq, nqueens, mutaterate):
    #sunarthsh gia metallakseis, to random.random() epistrefei timh apo 0 mexri 1 ara an to mutaterate einai panw apo 1 tha ginontai panta metallakseis kai katw apo 0 den tha ginontai pote
    for row in range(len(seq)):
        if random.random() < mutaterate:
            seq[row] = random.randrange(nqueens)
    return seq

def evolution(population, nqueens, popsize):
    #xrhsimopoioume thn selection gia na epileksoume goneis
    parents = selection(population, nqueens)
    #xrhsimopoioume thn crossover anamesa stous 2 goneis gia na vroume ta paidia tous
    offsprings = crossover(parents, nqueens, 2)
    #xrhsimopoioume thn mutate me mutate rate to 0.1 (mporoume na to allaksoume) gia na dwsoume thn pithanotita na ginoun metallakseis
    offsprings = [mutate(x, nqueens, 0.1) for x in offsprings]
    #vazoume thn prohgoumenh kai epomenh genia sto new_gen gia na krathsoume ta atoma me to megalutero fitness_score
    new_gen = offsprings
    for ind in population:
        new_gen.append(ind)
    #vriskoume kai gurname sorted lista twn n=popsize stoixiwn tou new_gen me descending order (reverse) tou fitness score, dhladh auta pou exoun pio megalo fitness score tha einai prwta
    new_gen = sorted(new_gen, key=lambda ind: fitness_score(ind, nqueens), reverse=True)[:popsize]
    return new_gen