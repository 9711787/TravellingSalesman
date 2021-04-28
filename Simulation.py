"""
SIMULATE PROBLEMS

This code is to simulate large number of travelling salesman problems 
to be solved by the implemented algorithms. 
"""

import numpy as np
import pandas as pd
import seaborn as sns
from itertools import chain
from Metaheuristics import random_search
from Graphs import generate_graph

def _flatten_list(outer_list):
    """
    Function to flatten a list of lists into a list
    Input
    outer_list: a list of lists
    """
    flat_list = []
    for inner_list in outer_list:
        for element in inner_list:
            flat_list.append(element)
    return flat_list

def simulate_graph_paths(random_seed, num_simulations, num_nodes, num_trials = 10000):
    
    np.random.seed(random_seed)
    data_out = []
    i = 0
    while i < num_simulations:
        i += 1
        random_graph = generate_graph(num_nodes, symmetric=True)
        _, _, data_d  = random_search(1, 1, num_nodes, random_graph, num_trials)
        data_out.append(data_d['Distances'])
    return data_out

def process_data(data_out):

    dataset_out = {'Id': [],'Feasible':[], 'Num_Solutions': [], 'Max_Dist': [], 'Min_Dist': [], 'Median_Dist': []}
    dist_out = []
    i = 0
    for record in data_out:
        # print(record)
        i += 1
        # Check whether any solution was find
        if len(record) == 0:
            dataset_out['Id'].append(i)
            dataset_out['Feasible'].append(0)
            dataset_out['Num_Solutions'].append(np.nan)
            dataset_out['Max_Dist'].append(np.nan)
            dataset_out['Min_Dist'].append(np.nan)
            dataset_out['Median_Dist'].append(np.nan)
        else:
            dataset_out['Id'].append(i)
            dataset_out['Feasible'].append(1)
            dataset_out['Num_Solutions'].append(len(record))
            dataset_out['Max_Dist'].append(np.amax(record))
            dataset_out['Min_Dist'].append(np.amin(record))
            dataset_out['Median_Dist'].append(np.median(record))
            # This removes the empty lists 
            dist_out.append(record)   
    return pd.DataFrame.from_dict(dataset_out), np.array(_flatten_list(dist_out), dtype=object)

def plot_distances(dist_data):

    sns.histplot(dist_data)
    return None


def paths_by_nodes(random_seed, num_simulations, num_nodes_list, num_trials = 10000):
    
    np.random.seed(random_seed)
    data_out = {}
    for num_nodes in num_nodes_list:
        i = 0
        path_data = []
        while i < num_simulations:
            i += 1
            random_graph = generate_graph(num_nodes, symmetric=True)
            _, _, data_d  = random_search(1, 1, num_nodes, random_graph, num_trials)
            path_data.append(data_d['Distances'])  
        data_out[num_nodes] = path_data
    return data_out

def paths_by_nodes_data(data_out):

    dataset_out = {'Id': [], 'Num_Of_Nodes': [], 'Feasible':[], 'Num_Solutions': [], 'Max_Dist': [], 'Min_Dist': [], 'Median_Dist': []}
    dist_out = {'Id':[],  'Num_Of_Nodes': [], 'Distance': []}
    
    i = 0
    for num_nodes in list(data_out.keys()):
        for record in data_out[num_nodes]:
            # print(record)
            i += 1
            # Check whether any solution was find
            if len(record) == 0:
                dataset_out['Id'].append(i)
                dataset_out['Num_Of_Nodes'].append(num_nodes)
                dataset_out['Feasible'].append(0)
                dataset_out['Num_Solutions'].append(np.nan)
                dataset_out['Max_Dist'].append(np.nan)
                dataset_out['Min_Dist'].append(np.nan)
                dataset_out['Median_Dist'].append(np.nan)
            else:
                dataset_out['Id'].append(i)
                dataset_out['Num_Of_Nodes'].append(num_nodes)
                dataset_out['Feasible'].append(1)
                dataset_out['Num_Solutions'].append(len(record))
                dataset_out['Max_Dist'].append(np.amax(record))
                dataset_out['Min_Dist'].append(np.amin(record))
                dataset_out['Median_Dist'].append(np.median(record))
                # This removes the empty lists 
                dist_out['Id'].append(np.repeat(i, len(record)).tolist())
                dist_out['Num_Of_Nodes'].append(np.repeat(num_nodes, len(record)).tolist())
                dist_out['Distance'].append(record)
    dist_out['Id'] = _flatten_list(dist_out['Id'])             
    dist_out['Num_Of_Nodes'] = _flatten_list(dist_out['Num_Of_Nodes'])
    dist_out['Distance'] = _flatten_list(dist_out['Distance'])
     
    return pd.DataFrame.from_dict(dataset_out), pd.DataFrame.from_dict(dist_out)