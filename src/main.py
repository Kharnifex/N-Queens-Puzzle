#p3190044, IOANNIS GKIONIS || p310104, PANAGIOTIS LAMPROPOULOS, TEXNHTH NOHMOSUNH 2021-22
#h askhsh ulopoieitai me genetiko algorithmo

from funcs import *
import time

def main():
    popsize=10
    nq=input("Give number of queens\n")
    start_time = time.time()
    try:
        val = int(nq)
    except ValueError:
        print("Number of queens has to be an integer")
        return
    #an queens<4 tote den uparxei lush kai trexei infinitely, exw valei san panw orio to 20
    if (int(nq)<4 or int(nq)>20):
        print("Number of queens has to be an integer ranging from 4 to 19")
        return
    nqueens=int(nq)
    #kyrio programma
    print("Generation:0")
    population = generate_population(nqueens, popsize)
    generation = 1
    while not print_check_goal(population, nqueens):
        print('Generation:'+ str(generation))
        population = evolution(population, nqueens, popsize)
        generation += 1
    print("--- %s seconds ---" % (time.time() - start_time))


main()