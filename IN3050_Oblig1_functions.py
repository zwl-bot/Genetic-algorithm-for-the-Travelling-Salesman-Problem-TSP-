import numpy as np
from itertools import permutations
import time
import csv
import random
import matplotlib.pyplot as plt
import copy


## Helper function from assignment 1
# Simplier way to read the .csv-file
def createTableCitiesCSV(filename):
    with open(filename, "r") as f:
        citiesTable = list(csv.reader(f, delimiter=';'))
        citiesName = citiesTable[0]
    
    for row in range(1, len(citiesTable)):
        for col in range(len(citiesName)):
            citiesTable[row][col] = float(citiesTable[row][col])
    
    return citiesTable, citiesName



## Helper function from assignment 1
# A method you can use to plot your plan on the map
def plot_plan(city_order, city_coords, europe_map, titles = None):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(europe_map, extent=[-14.56, 38.43, 37.697 + 0.3, 64.344 + 2.0], aspect="auto")
    
    n = len(city_order)
    # Map (long, lat) to (x, y) for plotting
    for index in range(n - 1):
        current_city_coords = city_coords[city_order[index]]
        next_city_coords = city_coords[city_order[index+1]]
        x, y = current_city_coords[0], current_city_coords[1]
        
        #Plotting a line to the next city
        next_x, next_y = next_city_coords[0], next_city_coords[1]
        plt.plot([x, next_x], [y, next_y])

        plt.plot(x, y, 'ok', markersize=5)
        plt.text(x, y, index, fontsize=12)
    #Finally, plotting from last to first city
    first_city_coords = city_coords[city_order[0]]
    first_x, first_y = first_city_coords[0], first_city_coords[1]
    plt.plot([next_x, first_x], [next_y, first_y])
    #Plotting a marker and index for the final city
    plt.plot(next_x, next_y, 'ok', markersize=5)
    plt.text(next_x, next_y, index+1, fontsize=12)
    if titles is None: 
        plt.title(f"TSP for {n} cities")
    else:
        plt.title(f"TSP for {n} cities - {titles}")
    plt.show()



## Helper function for printing out the corresponding cities
""" Input: path - order number of the cities, citiesName - the name of corresponding cities
Output: returns order list of cities
"""
def TSPPrintPath(path, citiesName):
    path_cities = [""]*len(path)
    for i in range(len(path)):
        path_cities[i] = citiesName[path[i]]
        
    return path_cities



## Helper function for calculating total distances for our given table of cities
""" Input: a - order number of the cities
Output: the distance of the tour
"""
def TSPDist(a, citiesTable):
    d = citiesTable[a[0]+1][a[-1]]
    for i in range(len(a)-1):
        d += citiesTable[a[i]+1][a[i+1]]
    return d



## Method, with time checks
def timeTSPMethod(n, citiesTable, TSP_method):
    # making sure TSP_method is a function
    if not callable(TSP_method):
        raise TypeError("Input method is not a function")
    
    # time calculated in ns
    t = time.time_ns() # time START
    shortestDist, shortestPathCities = TSP_method(n, citiesTable)
    timeus = time.time_ns() - t # time END
    return shortestDist, shortestPathCities, timeus




########## Exhaustive search ##########

### Exhaustive search main function
def TSPExhaustive(n, citiesTable):
    if type(n) != int or n < 1: # Assure n is a valid integer
        raise AssertionError(f"Input n is not a valid integer, value n is {n}")
    
    if n > len(citiesTable[0]): # Assure n is within range
        raise ValueError("Input n too large")
    
    lst = citiesTable[0][:n]
    paths = list(permutations(range(len(lst))))
    
    # current shortest distance and shortest path
    shortestDist, shortestPath = TSPDist(paths[0], citiesTable), paths[0]
    
    for p in paths: 
        currDist = TSPDist(p, citiesTable)
        if currDist < shortestDist:
            shortestDist, shortestPath = currDist, p
    
    shortestPathCities = TSPPrintPath(shortestPath, citiesTable[0])
    
    return round(shortestDist, 2), shortestPathCities



########## Hill climbing ##########

## Helper function for Hill climbing
""" Input: path - list of order number of cities
Output: List of its neighbors
"""
def generateNeighbors(path):
    n = len(path)
    
    """Mathematical explaination on page 4 of Assignment 1"""
    neighbors = [[]]*int(n*(n-1)/2) # avoids using append each time
    
    count = 0
    for i in range(n, 1, -1):
        for j in range(i-1, 0, -1):
            path[i-1], path[j-1] = path[j-1], path[i-1]
            # since we want to reuse path with its original input, need to copy current results
            neighbors[count] = path[:] 
            path[i-1], path[j-1] = path[j-1], path[i-1] 
            count += 1
    
    return neighbors



## Helper function for finding best neighbor solution
""" Input: neighbors - a list of different solutions
Output: the solution with shortest distance and its path
"""
def findMinTSP(neighbors, citiesTable):
    n = len(neighbors)
    shortestDist, shortestPath = TSPDist(neighbors[0], citiesTable), neighbors[0]
    
    for i in range(1, n):
        currShortestDist = TSPDist(neighbors[i], citiesTable)
        if currShortestDist < shortestDist:
            shortestDist, shortestPath = currShortestDist, neighbors[i]
    
    return shortestDist, shortestPath




## Hill climbing main function
def TSPHillClimbing(n, citiesTable):
    if type(n) != int or n < 1: # Assure n is a valid integer
        raise AssertionError("Input n is not a valid integer")
    
    if n > len(citiesTable[0]): # Assure n is within range
        raise ValueError("Input n too large")
    
    initialPath = list(range(n))
    random.shuffle(initialPath) # start with random initial path
    initialDist = TSPDist(initialPath, citiesTable)
    
    neighbors = generateNeighbors(initialPath) # returns a list of neighbors of initial path
    
    currDist, currPath = initialDist, initialPath
    currNeighbors = neighbors
    
    limitCount = 1e+16  # Avoiding "infinitely" search when n is large
    counter = 0
    
    while True: 
        currBestDist, currBestPath = findMinTSP(currNeighbors, citiesTable)
        
        if counter >= limitCount: # seached for too long
            break
        
        if currBestDist < currDist: # if better solution is found
            currDist, currPath = currBestDist, currBestPath
            currNeighbors = generateNeighbors(currPath)
            counter += 1
        else: # if no more better solution is found
            break
    
    currPath = TSPPrintPath(currPath, citiesTable[0])
    return round(currDist, 2), currPath




########## Genetic algorithm ##########

## Helper function for (inversion) mutation of candidate
def inverseMutation(citiesOrder):
    new_citiesOrder = citiesOrder[:] # copy path
    n = len(citiesOrder)
    start_end = [0,0] # start and end positions in citiesOrder
    
    a = random.randint(1, n); start_end[0] = a
    curr_b = random.randint(1, n)
    while curr_b == a: # prevents duplicates
        curr_b = random.randint(1, n)
    
    start_end[1] = curr_b
    start_end.sort() # sort a and b (curr_b) in increased order
    
    # reverse segment of new_citiesOrder from start position to end position
    p1 = new_citiesOrder[start_end[0]-1:start_end[1]]
    p1.reverse()
    new_citiesOrder[start_end[0]-1:start_end[1]] = p1
    
    return new_citiesOrder



## Helper function for PMX (Partially Mapped Crossover)
""" Input: p1, p2 - parent 1, parent 2 | a, b - two different positions in p1
Output: a child
"""
def PMX_child(p1, p2, a, b):
    n = len(p1)
    child = [None]*n

    # step 1 - segmenting
    segment = p1[a-1:b]
    child[a-1:b] = segment

    # step 2 - placement of remaning segment elements
    for i in range(a-1, b):
        if p2[i] in segment:
            continue
        else:
            pos_first = i
            pos_next = p2.index(p1[pos_first])
            
            for j in range(len(segment)):
                if pos_next >= a-1 and pos_next <= b-1:
                    pos_first = pos_next
                    pos_next = p2.index(p1[pos_first])
                else: 
                    child[pos_next] = p2[i]
                    break
    
    # step 3 - copy remaining elements from p2 into child
    for i in range(n):
        if child[i] == None:
            child[i] = p2[i]
    
    return child



## PMX (crossover) main function
""" Input: p1, p2 - parent 1, parent 2
Output: two children
"""
def PMX(p1, p2):
    n = len(p1)
    start, end = 0, 0
    
    a = random.randint(1, n); b = random.randint(1, n) 
    while b == a: # prevents duplicates
        b = random.randint(1, n)
    if a < b:
        start, end = a, b 
    else: 
        start, end = b, a
    
    child1 = PMX_child(p1, p2, a, b) # child 1
    child2 = PMX_child(p2, p1, a, b) # child 2
    
    return child1, child2



## Helper function - generate an initial population with evenly spread candidates (diversity)
# what happens when a random candidate is a duplicate? 
""" Input: n - number of cities | pop_size - size of population
Output: A random initial population with different spread solutions as candidates
"""
def createInitialPopulation(n, pop_size):
    population_path = [[]]*pop_size
    
    population_fitness = [0]*pop_size # initial population fitness
    
    init_sol = list(range(n)); random.shuffle(init_sol) # initial candidate
    for i in range(pop_size):
        population_path[i] = init_sol[:]
        random.shuffle(init_sol)
    
    population = list(zip(population_path, population_fitness))
    for j in range(pop_size):
        population[j] = list(population[j])
    
    return population
    
    

## Helper function for evaluation of a population
def populationFitness(population, citiesTable):
    for i in range(len(population)): # Assign evaluated fitness too 
        population[i][1] = TSPDist(population[i][0], citiesTable)
    return population



## find the best fitness of a population
def findMin(population):
    curr_min = population[0]
    for i in range(1, len(population)):
        if population[i][1] < curr_min[1]:
            curr_min = population[i]
    return curr_min


## Choose candidates as parents - tournament style
def createParents(population, pop_size, k):
    if pop_size % k == 0: 
        parents = [[]] * int(pop_size/k)
    else: 
        parents = [[]] * int(pop_size/k + 1)
    
    this_population = population[:] # make a copy of current population
    count = 0 
    while count < len(parents):
        # generate k random indices
        if k > len(this_population):
            k = len(this_population)
        
        tournament_index = random.sample(range(len(this_population)), k)
        tournament_parent = []
        
        for index in tournament_index: # adding parents into tournament
            tournament_parent.append(this_population[index])
        
        tournament_parent_best = findMin(tournament_parent) # find best parent
        parents[count] = tournament_parent_best
        
        # update current population by removing the chosen parents from tournament
        this_population_new = [] 
        for i in range((len(this_population))):
            if i not in tournament_index:
                this_population_new.append(this_population[i])
        this_population = this_population_new  # new population has k fewer elements
        
        count += 1
    
    return parents



## Create initial offsprings (fitness = 0)
def createOffsprings(parents):
    if len(parents) % 2 == 0:
        offsprings = [ [] ] * len(parents)
    else: 
        offsprings = [ [] ] * int(len(parents)-1)
    
    # Recombination part (PMX)
    for i in range(int(len(parents)/2)):
        if len(parents) < 2: # if less than 2 parents
            break
        p1 = parents.pop(0); p2 = parents.pop(0) # parent 1 and parent 2
        c1, c2 = PMX(p1[0], p2[0]) # child 1 and child 2
        offsprings[2*i] = c1; offsprings[2*i+1] = c2
    
    # Mutation part (inverse mutation)
    offsprings_fitness = [0]*len(offsprings)
    offsprings_mutated = [[]]*len(offsprings)
    for j in range(len(offsprings)):
        offsprings_mutated[j] = inverseMutation(offsprings[j])
    
    
    offsprings_final = list(zip(offsprings_mutated, offsprings_fitness))
    for j in range(len(offsprings)):
        offsprings_final[j] = list(offsprings_final[j])
        
    return offsprings_final



## Survivor selection (elitist strategy)
def populationSelect(prev_pop, offsprings, pop_size):
    new_pool = prev_pop + offsprings
    new_pool = sortPop(new_pool)  # use sorting algorithms from IN2010
    new_population = new_pool[:pop_size] # choose the first pop_size candidates as survivors
    random.shuffle(new_population) # reshuffle candidates in population
    return new_population



## Quick sort algorithm
def choosePivot(A, low, high):
    d = int(low + (high - low)/2)
    return d


def partition(A, low, high):
    p = choosePivot(A, low, high)
    A[p], A[high] = A[high], A[p]
    
    pivot = A[high][1]
    left = low
    right = high - 1 
    
    while left <= right:
        while left <= right and A[left][1] <= pivot:
            left += 1
        while right >= left and A[right][1] >= pivot:
            right -= 1
        if left < right:
            A[left], A[right] = A[right], A[left]
    A[left], A[high] = A[high], A[left]
    return left


def quicksort(A, low, high):
    if low >= high:
        return A
    p = partition(A, low, high)
    quicksort(A, low, p-1)
    quicksort(A, p+1, high)
    return A



## Sort population in ascending order by their fitness (Quicksort)
def sortPop(new_population):
    n = len(new_population)
    
    # This sorting algorithm is demonstrated in IN2010 Algoritmer og Datastrukturer
    new_population = quicksort(new_population, 0, n-1)
    return new_population



### Genetic algorithm main function
def geneticAlgorithm(n, citiesTable, pop_size, k, max_generations=50):
    """max_generations=50 default value"""
    if type(n) != int or n < 1: # Assure n is a valid integer
        raise AssertionError("Input n is not a valid integer")
    
    if n > len(citiesTable[0]): # Assure n is within range
        raise ValueError("Input n too large")
    
    # Initialize population with pop_size and "evenly" distributed random candidates
    initial_population = createInitialPopulation(n, pop_size)
    
    # Evaluate population with some fitness function (TSPDist)
    initial_population_eval = populationFitness(initial_population, citiesTable)
    
    curr_pop = initial_population_eval
    
    # store best fitness canndidate for each generation
    best_fit_each_gen = np.zeros(max_generations)
        
    # repeating until termination condition is met
    generations = 0
    while generations < max_generations: 
        # create current parents
        curr_parents = createParents(curr_pop, pop_size, k)
        
        # create current offsprings (mutated as well) and evaluate
        curr_offsprings = createOffsprings(curr_parents)
        curr_offsprings = populationFitness(curr_offsprings, citiesTable) 
        
        # survivor selection (Elitist strategy)
        curr_pop = populationSelect(curr_pop, curr_offsprings, pop_size)
        
        best_fit_each_gen[generations] = findMin(curr_pop)[1]
        generations += 1
    
    # Termination condition reached
    optimal_candidate = findMin(curr_pop) # best candidate in this generation of population
    shortestPath, shortestDist = optimal_candidate[0], optimal_candidate[1]
    shortestPath = TSPPrintPath(shortestPath, citiesTable[0])
    return shortestPath, shortestDist, best_fit_each_gen

