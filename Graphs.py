"""
GENERATE GRAPH

This code can be used to generate a graph to
be used for a travelling salesman problem.
"""

import numpy as np

def generate_graph(num_nodes, max_distance = 15, symmetric = True):
    """
    Function to generate a graph to be used for a travelling salesman problem.

    Input:
    num_nodes: int or float
        number of nodes in a graph
    max_distance: int or float
        largest distance possible between nodes
    symmetric: boolean
        whether distance between two of nodes is same in both directions 

    Output:
    graph: dictionary of dictionaries
        outer keys represent starting nodes; outer values are dictionaries of destination nodes and distances
        inner keys are destination nodes; inner values are distances
    """
    graph = {}
    # Initialize the graph.
    for i in np.arange(1, num_nodes + 1):
        graph[i] = {}
    # Symmetric graph has a same distance between two nodes in both directions. 
    if symmetric == True:
        for i in np.arange(1, num_nodes + 1):
            num_routes = np.random.randint(1, num_nodes - 1)
            destinations = np.random.randint(1, num_nodes, size=num_routes)
            for destination in destinations:
                distance = np.random.randint(1, max_distance)
                graph[i][destination] = distance
                graph[destination][i] = distance
    # This assumes that path works both ways, but the distance does not have to be same.
    elif symmetric == False:
        for i in np.arange(1, num_nodes + 1):
            num_routes = np.random.randint(1, num_nodes - 1)
            destinations = np.random.randint(1, num_nodes, size=num_routes)
            for destination in destinations:
                distance = np.random.randint(1, max_distance)
                graph[i][destination] = distance
                distance = np.random.randint(1, max_distance)
                graph[destination][i] = distance
    return graph




    


