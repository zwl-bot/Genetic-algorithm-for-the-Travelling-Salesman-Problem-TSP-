import numpy as np
import IN3050_Oblig1_functions as iof
import csv
import matplotlib.pyplot as plt
import time

## Initial values
np.random.seed(57)

#Map of Europe
europe_map = plt.imread('map.png')

#Lists of city coordinates
city_coords = {
    "Barcelona": [2.154007, 41.390205], "Belgrade": [20.46, 44.79], "Berlin": [13.40, 52.52], 
    "Brussels": [4.35, 50.85], "Bucharest": [26.10, 44.44], "Budapest": [19.04, 47.50],
    "Copenhagen": [12.57, 55.68], "Dublin": [-6.27, 53.35], "Hamburg": [9.99, 53.55], 
    "Istanbul": [28.98, 41.02], "Kyiv": [30.52, 50.45], "London": [-0.12, 51.51], 
    "Madrid": [-3.70, 40.42], "Milan": [9.19, 45.46], "Moscow": [37.62, 55.75],
    "Munich": [11.58, 48.14], "Paris": [2.35, 48.86], "Prague": [14.42, 50.07],
    "Rome": [12.50, 41.90], "Saint Petersburg": [30.31, 59.94], "Sofia": [23.32, 42.70],
    "Stockholm": [18.06, 60.33], "Vienna": [16.36, 48.21], "Warsaw": [21.02, 52.24]}


## Read the file, create the tables for cities and their corresponding name
fileName = "european_cities.csv"
citiesTable, citiesName = iof.createTableCitiesCSV(fileName)



#################### EXHAUSTIVE SEARCH ####################

## Plot the average times for several n cities

## Average time for finding the shortest path for n=6 to n=10
n_start = 6; n_end = 10; 
n_list = list(range(n_start, n_end+1))
mu_times = [0]*(len(n_list)) # list of average times
"""
for n in n_list:
    curr_total_time = 0
    
    for i in range(10):
        currDist, currPath, currTime = iof.timeTSPMethod(n, citiesTable, iof.TSPExhaustive)
        curr_total_time += currTime
    curr_mu_time = curr_total_time/10 # current average time for n cities
    mu_times[n - n_start] = curr_mu_time


# plot average times for each n cities 
plt.plot(n_list, mu_times)
plt.title(f"Average runtime for {n_start} to {n_end} cities")
plt.show()
"""


## Test for n=6 and n=10
"""
shortestDist1, shortestPath1, timeus1 = iof.timeTSPMethod(n_start, citiesTable, iof.TSPExhaustive)
shortestDist2, shortestPath2, timeus2 = iof.timeTSPMethod(n_end, citiesTable, iof.TSPExhaustive)
print("Exhaustive search")
print("---- Number of cities: ", n_start, " ----")
#print("Runtime (ns): ", timeus1)
print("Shortest distance: ", shortestDist1, " km")
print(shortestPath1)
print("\n")
#iof.plot_plan(shortestPath1, city_coords, europe_map)

print("---- Number of cities: ", n_end, " ----")
#print("Runtime (ns): ", timeus2)
print("Shortest distance: ", shortestDist2, " km")
print(shortestPath2)
print("\n")
#iof.plot_plan(shortestPath2, city_coords, europe_map) 
"""



#################### HILL CLIMBING ####################
## Find best, worst, mean solution and it's standard deviation
"""
runs = 20
n_cities = [10, 24]
count = 0

print("Hill climbing")
for n in n_cities:
    curr_best_dist = 0; curr_best_path = []
    curr_worst_dist = 0; curr_worst_path = []
    curr_total_dist = 0
    
    distances = [0.0]*runs
    
    for i in range(runs):
        curr_dist, curr_path = iof.TSPHillClimbing(n, citiesTable)
        curr_total_dist += curr_dist
        
        distances[i] = curr_dist
        
        if curr_best_dist == 0:
            curr_best_dist = curr_dist; curr_best_path = curr_path
        
        if curr_dist < curr_best_dist: # finding the best solution
            curr_best_dist = curr_dist; curr_best_path = curr_path
        
        elif curr_dist > curr_worst_dist: # finding the worst solution
            curr_worst_dist = curr_dist; curr_worst_path = curr_path
            
        else: # curr_dist == curr_best_dist or curr_worst_dist
            continue
    
    curr_mean_dist = round(curr_total_dist/runs, 2)
    
    curr_variance = 0 # variance
    for d in distances:
        curr_variance += (curr_mean_dist - d)**2
    curr_variance = curr_variance/runs
    curr_standard_deviation = round(np.sqrt(curr_variance), 2) # standard deviation
    
    print("---- Number of cities: ", n, " ----")
    print("Best solution: ", curr_best_dist, " km")
    print(curr_best_path)
    print()
    print("Worst solution: ", curr_worst_dist, " km")
    print(curr_worst_path)
    print()
    print("Mean solution: ", curr_mean_dist, " km")
    print("Standard deviation: ", curr_standard_deviation, " km")
    print("\n\n")
    iof.plot_plan(curr_best_path, city_coords, europe_map, "Best") # plotting the best result
    iof.plot_plan(curr_worst_path, city_coords, europe_map, "Worst") # plotting the worst result
"""





#################### GENETIC ALGORITHM ####################
"""
k = 5
runs = 20
n_cities = [10, 24]

# for each population size, plot fitness convergence, best and worst path out of 20 runs
max_pops = [100, 200, 400]
max_generations = 400

print("Genetic Algorithm"); print(f"{max_generations} generations"); print()

generations_list = np.arange(1, max_generations+1) # x-axis, fitness plot

for n in n_cities: 
    print("---- Number of cities: ", n, " ----"); print()
    best_fit_each_gen_pops = [[]]*len(max_pops); count = 0
    
    for pop_size in max_pops:
        print("--- Population: ", pop_size, " ---")
        best_fit_each_gen = np.zeros(max_generations) # y-axis, fitness plot
        
        curr_best_dist = 0; curr_best_path = []
        curr_worst_dist = 0; curr_worst_path = []
        curr_total_dist = 0
        
        distances = np.zeros(runs)
        curr_total_time = 0 # calculate average runtime
        for i in range(runs):
            t = time.time_ns() # time START
            curr_path, curr_dist, curr_best_fit_each_gen = iof.geneticAlgorithm(n, citiesTable, pop_size, k, max_generations)
            timeus = time.time_ns() - t # time END
            curr_total_time += timeus # add time to total time
            
            best_fit_each_gen += curr_best_fit_each_gen
            
            curr_total_dist += curr_dist
            
            distances[i] = curr_dist
            
            if curr_best_dist == 0:
                curr_best_dist = curr_dist; curr_best_path = curr_path
            
            if curr_dist < curr_best_dist: # finding the best solution
                curr_best_dist = curr_dist; curr_best_path = curr_path
            
            elif curr_dist > curr_worst_dist: # finding the worst solution
                curr_worst_dist = curr_dist; curr_worst_path = curr_path
                
            else: # curr_dist == curr_best_dist or curr_worst_dist
                continue
            
        # average time
        avg_time = curr_total_time/runs
        
        # Average fitness in each generation of n cities for different populations
        best_fit_each_gen = best_fit_each_gen/runs
        best_fit_each_gen_pops[count] = best_fit_each_gen
        count += 1
        
        curr_mean_dist = round(curr_total_dist/runs, 2)
        
        curr_variance = 0 # variance
        for d in distances:
            curr_variance += (curr_mean_dist - d)**2
        curr_variance = curr_variance/runs
        curr_standard_deviation = round(np.sqrt(curr_variance), 2) # standard deviation
        
        print("Runtime (ns): ", avg_time)
        print("Best solution: ", curr_best_dist, " km"); print(curr_best_path); print()
        print("Worst solution: ", curr_worst_dist, " km"); print(curr_worst_path); print()
        print("Mean solution: ", curr_mean_dist, " km")
        print("Standard deviation: ", curr_standard_deviation, " km"); print("\n\n")
        title_best = f"GA Best, Population = {pop_size},  Generations = {max_generations}"
        iof.plot_plan(curr_best_path, city_coords, europe_map, title_best) # plotting the best result
    
    pop_index = 0
    for best_fits in best_fit_each_gen_pops:
        plt.plot(generations_list, best_fits, label=f"Population = {max_pops[pop_index]}")
        pop_index += 1
    plt.title(f"GA Average fit of best in each gen, {n} cities")
    plt.xlabel("Generations"); plt.ylabel("Fitness/Distance"); plt.legend(); plt.show()
    print()
"""






# Single test for 24 cities
"""
k = 5
n = 24

# for each population size, plot fitness convergence, best and worst path out of 20 runs
pop_size = 200
max_generations = 400

bestPathGA, bestDistGA, best_fit_each_gen = iof.geneticAlgorithm(n, citiesTable, pop_size, k, max_generations)
print("Best solution: ", bestDistGA, " km"); print(bestPathGA); print()
title_best = f"GA Best, Population = {pop_size},  Generations = {max_generations}"
iof.plot_plan(bestPathGA, city_coords, europe_map, title_best) # plotting the best result
"""