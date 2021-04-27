"""
METAHEURISTIC ALGORITHMS

This code implements Random Search, Random Sub-tour Reversal, 
and Genetic Algorithm.

Based on Chapter Chapter 14 of Introduction to Operations Research (10th Edition)
by Hilier and Lieberman.
"""

import numpy as np
import random as rd

def _random_search(start_node, end_node, num_nodes, node_graph, num_trials):
    """
    Implementation of a random search. 

    Input:
    start_node: int
        starting node of travelling salesman problem
    end_node: int
        end node of travelling salesman problem; round travelling 
    num_nodes: int
        number of nodes of a input graph
    node_graph: dict
        input graph generated by proprietary generate_graph() function
    num_trails:

    Output:
    path_out:
    dist_out: 
    """

    i = 0
    path_out = []
    dist_out = []
    while i < num_trials:
        j = 0
        path = []
        dist = 0
        current_node = start_node
        path.append(current_node)
        while j <= num_nodes:
            destination_list = list(node_graph[current_node].keys())
            rd.shuffle(destination_list)
            k = 0
            max_dest = len(destination_list)
            for destination in destination_list:  
                if (destination not in path) or ((destination == end_node) and (j == (num_nodes - 1))):
                    path.append(destination)
                    dist += node_graph[current_node][destination]
                    current_node = destination
                    j += 1
                    break
                else: 
                    k += 1
            if max_dest == k:
                i += 1
                break
        if path not in path_out and (len(path) == (num_nodes + 1)):       
            path_out.append(path)
            dist_out.append(dist)
    return path_out, dist_out

def random_search(start_node, end_node, num_nodes, node_graph, num_trials, goal = 'max'):
    
    i = 0
    path_out = []
    dist_out = []
    best_path = None
    best_dist = None
    data_out = {}
    while i < num_trials:
        j = 0
        path = []
        dist = 0
        current_node = start_node
        path.append(current_node)
        while j <= num_nodes:
            destination_list = list(node_graph[current_node].keys())
            rd.shuffle(destination_list)
            k = 0
            max_dest = len(destination_list)
            for destination in destination_list:
                if (destination not in path) or ((destination == end_node) and (j == (num_nodes - 1))):
                    path.append(destination)
                    dist += node_graph[current_node][destination]
                    current_node = destination
                    j += 1
                    break
                else: 
                    k += 1
            if max_dest == k:
                i += 1
                break
        if path not in path_out and (len(path) == (num_nodes + 1)):       
            path_out.append(path)
            dist_out.append(dist)
            if goal == 'max':
                if best_dist == None:
                    best_dist = dist
                    best_path = path
                elif best_dist < dist:
                    best_dist = dist
                    best_path = path
            if goal == 'min':
                if best_dist == None:
                    best_dist = dist
                    best_path = path
                elif best_dist > dist:
                    best_dist = dist
                    best_path = path
        data_out['Paths'] = path_out
        data_out['Distances'] = dist_out
    return best_path, best_dist, data_out
       
def _random_search_solution(start_node, end_node, num_nodes, node_graph): 
    
    path_out = None
    dist_out = None
    while path_out is None: 
        j = 0
        path = []
        dist = 0
        current_node = start_node
        path.append(current_node)
        while j <= num_nodes:
            destination_list = list(node_graph[current_node].keys())
            rd.shuffle(destination_list)
            k = 0
            max_dest = len(destination_list) 
            for destination in destination_list: 
                if (destination not in path) or ((destination == end_node) and (j == (num_nodes - 1))):
                    path.append(destination)
                    dist += node_graph[current_node][destination]
                    current_node = destination
                    j += 1
                    break
                else: 
                    k += 1
            if max_dest == k:
                break
        if (len(path) == (num_nodes + 1)):       
            path_out = path
            dist_out = dist 
    return path_out, dist_out

def sub_tours(graph, current_node):
    
    destinations = list(graph[current_node].keys())
    node_subtours = [] 
    for destination in destinations:
        destinations2 = list(graph[destination].keys())
        for destination2 in destinations2: 
            if destination2 in destinations:
                node_subtours.append((destination,destination2))
    return node_subtours

def subtour_map(graph):
    
    subtourmap = {}
    for node in list(graph.keys()):
        subtourmap[node] = sub_tours(graph, node)
    return subtourmap

def _local_sub_tours(graph, current_node, subtour_map = {}):
    
    if current_node not in subtour_map.keys():
        subtour_map[current_node] = sub_tours(graph, current_node)
    return subtour_map

def _subtour_dist(start_node, subtour, end_node, node_graph):
    
    old_dist = node_graph[start_node][subtour[0]] + node_graph[subtour[0]][subtour[1]] + node_graph[subtour[1]][end_node]
    new_dist = node_graph[start_node][subtour[1]] + node_graph[subtour[1]][subtour[0]] + node_graph[subtour[0]][end_node]
    return new_dist - old_dist

def _test_subtour(start_node, subtour, end_node, node_graph):
    
    if (subtour[1] in list(node_graph[start_node].keys())) and (subtour[0] in list(node_graph[subtour[1]].keys())) and (end_node in list(node_graph[subtour[0]].keys())):
        feasible = True
    else:
        feasible = False
    return feasible

def _evaluate_path(path, node_graph):
    
    dist = 0
    num_nodes = len(path) - 1
    for i in np.arange(num_nodes):
        dist += node_graph[path[i]][path[i + 1]]
    return dist

def sub_tour_reversal(start_node, end_node, num_nodes, node_graph, num_trials, goal = 'max'):
    
    # Generate a random solution.
    best_path, best_dist = _random_search_solution(start_node, end_node, num_nodes, node_graph)
    # Start performing random sub-tour reversals.
    i = 0
    while i < num_trials:
        i += 1
        random_position = np.random.randint(1, num_nodes - 1)
        start_node = best_path[random_position - 1]
        subtour = (best_path[random_position], best_path[random_position + 1])
        end_node = best_path[random_position + 2]
        if _test_subtour(start_node, subtour, end_node, node_graph):
            sub_dist = _subtour_dist(start_node, subtour, end_node, node_graph)
            if goal == 'max':
                if sub_dist >= 0:
                    best_path[random_position] = subtour[1]
                    best_path[random_position + 1] = subtour[0]
                    best_dist += sub_dist
            if goal == 'min':
                if sub_dist <= 0:
                    best_path[random_position] = subtour[1]
                    best_path[random_position + 1] = subtour[0]
                    best_dist += sub_dist
            if goal == 'search':
                best_path[random_position] = subtour[1]
                best_path[random_position + 1] = subtour[0]
                best_dist += sub_dist
    return best_path, best_dist

def simulated_annealing(start_node, end_node, num_nodes, node_graph, num_trials, goal = 'max'):
    
    # Generate a random solution.
    best_path, best_dist = _random_search_solution(start_node, end_node, num_nodes, node_graph)
    # Start performing random sub-tour reversals.
    i = 0
    T = best_dist * 0.2
    while i < num_trials:
        i += 1
        random_position = np.random.randint(1, num_nodes - 1)
        start_node = best_path[random_position - 1]
        subtour = (best_path[random_position], best_path[random_position + 1])
        end_node = best_path[random_position + 2]
        if _test_subtour(start_node, subtour, end_node, node_graph):
            sub_dist = _subtour_dist(start_node, subtour, end_node, node_graph)
            if goal == 'max': 
                if np.random.random() < np.exp(sub_dist/T) :
                    best_path[random_position] = subtour[1]
                    best_path[random_position + 1] = subtour[0]
                    best_dist += sub_dist
                    T = T * 0.8 
            if goal == 'min':
                if np.random.random() < np.exp(-sub_dist/T) :
                    best_path[random_position] = subtour[1]
                    best_path[random_position + 1] = subtour[0]
                    best_dist += sub_dist
                    T = T * 0.8 
    return best_path, best_dist


def _random_search_population(start_node, end_node, num_nodes, node_graph, num_trials):
    
    i = 0
    path_out = []
    dist_out = []
    while i < num_trials:
        j = 0
        path = []
        dist = 0
        current_node = start_node
        path.append(current_node)
        while j <= num_nodes:
            destination_list = list(node_graph[current_node].keys())
            rd.shuffle(destination_list) 
            k = 0
            max_dest = len(destination_list)
            for destination in destination_list:            
                if (destination not in path) or ((destination == end_node) and (j == (num_nodes - 1))):
                    path.append(destination)
                    dist += node_graph[current_node][destination]
                    current_node = destination
                    j += 1
                    break
                else: 
                    k += 1
            if max_dest == k:
                break
        if path not in path_out and (len(path) == (num_nodes + 1)): 
            i += 1
            path_out.append(path)
            dist_out.append(dist)
    return path_out, dist_out
    
def _child_solution(start_node, end_node, num_nodes, node_graph, parent1, parent2, mutation_rate):
    
    path_out = None
    dist_out = None
    while path_out is None:
        j = 0
        path = []
        dist = 0
        current_node = start_node
        path.append(current_node)
        while j <= num_nodes:
            # Identify what destination have the parents at a current node.
            dest1_index = np.where(np.array(parent1) == current_node)[0][0] + 1
            dest1 = parent1[dest1_index]
            dest2_index = np.where(np.array(parent2) == current_node)[0][0] + 1
            dest2 = parent2[dest2_index]
            # Check whether mutation happens. Only mutate when it is possible to mutate. 
            destination_list = list(node_graph[current_node].keys())
            destination_list = list(np.array(destination_list)[[d not in (dest1,dest2) for d in destination_list]])   
            if (np.random.random() < mutation_rate) and len(destination_list) > 0:
                # Pick random non-parent destination to mutate.
                rd.shuffle(destination_list)
            else: 
                # Or use one of one of the parent.
                if np.random.random()  < 0.5:
                    destination_list = [dest1]
                else:
                    destination_list = [dest2]
            k = 0 
            max_dest = len(destination_list)
            for destination in destination_list:
                if (destination not in path) or ((destination == end_node) and (j == (num_nodes - 1))):
                    path.append(destination)
                    dist += node_graph[current_node][destination]
                    current_node = destination
                    j += 1
                    break
                else: 
                    k += 1
            if max_dest == k:
                break
        if (len(path) == (num_nodes + 1)):       
            path_out = path
            dist_out = dist
    return path_out, dist_out

def _produce_offspring(start_node, end_node, num_nodes, node_graph, pop_path, pop_dist, goal, mutation_rate):
    
    off_pop_path = []  
    off_pop_dist = []
    # Select number of parents. Ensure there are at least 2.
    if np.maximum(np.floor(len(pop_dist)/2), 1) == 1:
        num_parents = 2
    else:
        num_parents = np.random.randint(1, np.maximum(np.floor(len(pop_dist)/2), 1)) * 2
    if goal == 'max':
        probs = np.array(pop_dist)/np.max(pop_dist)
    if goal == 'min':
        probs = 1/(np.array(pop_dist)/np.min(pop_dist)) 
    i = 0
    parent_index = []
    # Selects indices that will become parents.
    while i < num_parents:
        j = 0
        for prob in probs:
            if (np.random.random() < prob) and j not in parent_index:
                parent_index.append(j)
                i += 1
            if len(parent_index) == num_parents:
                break
            j += 1
    # Produce offspring.
    for k in np.arange(0, num_parents - 1):
        parent1 = pop_path[parent_index[k]]
        parent2 = pop_path[parent_index[k + 1]]
        m = 0
        while m < 2:                
            child_path, child_dist = _child_solution(start_node, end_node, num_nodes, node_graph, parent1, parent2, mutation_rate)
            if child_dist is not None:
                off_pop_path.append(child_path)
                off_pop_dist.append(child_dist)
                m += 1
    # Fill the rest with parent generation.
    rest_index = []
    while len(off_pop_dist) < len(pop_dist):
        n = 0
        for prob in probs:
            if (np.random.random() < prob) and n not in rest_index:
                rest_index.append(j)
                off_pop_path.append(pop_path[m])
                off_pop_dist.append(pop_dist[m])     
                n += 1
            if len(rest_index) == len(pop_dist):
                break
    return off_pop_path, off_pop_dist

def genetic_algorithm(start_node, end_node, num_nodes, node_graph, num_trials, goal = 'max',
                      population_size = 0.20, mutation_rate = 0.01):
    
    # Generate starting population size.
    pop_size = np.maximum(round(population_size * num_trials), 2)    
    pop_path, pop_dist = _random_search_population(start_node, end_node, num_nodes, node_graph, pop_size)
    # Create offspring populations.
    i = 0
    while i < num_trials:
        i += 1
        pop_path, pop_dist = _produce_offspring(start_node, end_node, num_nodes, node_graph, pop_path, pop_dist, goal, mutation_rate)
        best_path = None
        best_dist = None
        for j in np.arange(len(pop_dist)):
            dist = pop_dist[j]
            path = pop_path[j]
            if goal == 'max':
                if best_dist == None:
                    best_dist = dist
                    best_path = path
                elif best_dist < dist:
                    best_dist = dist
                    best_path = path
            if goal == 'min':
                if best_dist == None:
                    best_dist = dist
                    best_path = path
                elif best_dist > dist:
                    best_dist = dist
                    best_path = path
    return best_path, best_dist