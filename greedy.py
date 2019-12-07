import networkx as nx
import os
import sys
import graph_utils
import tsp

from networkx.algorithms.shortest_paths.weighted import dijkstra_path_length
from networkx.algorithms.shortest_paths.weighted import dijkstra_path

sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import prune_mst as pm



from student_utils import *

"""
Algorithm is as follows:

    Start from soda
    
    if no edge to any unvisited home in current location：
        then run Dijkstra to find the next home
    else:
        Choose the shortest path to the next home
    (due to triangular inequality, going to a home that is your neighbor is always closer than going through some other route)
    
    repeat until no home is not visited.
    
    Go back to Soda
"""

"""
graph: a nx graph
"""
def greedy_solver(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix):
    G = adjacency_matrix_to_graph(adjacency_matrix)[0]

    name_to_ind = name_to_index(list_of_locations)

    home_in_ind = [name_to_ind[home] for home in list_of_homes]

    start_ind = name_to_ind[starting_car_location]

    path = greedy_algorithm(G, home_in_ind, start_ind)

    drop_off_dict = {}

    for home in home_in_ind:
        drop_off_dict[home] = [home]

    return path, drop_off_dict

def greedy_prune_solver(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix):
    G = adjacency_matrix_to_graph(adjacency_matrix)[0]

    name_to_ind = name_to_index(list_of_locations)

    home_in_ind = [name_to_ind[home] for home in list_of_homes]

    start_ind = name_to_ind[starting_car_location]

    G_pruned, to_drop, pruned_homes = graph_utils.prune_leaf_home(G, home_in_ind, start_ind)

    original_homes = home_in_ind
    homes_left = [x for x in original_homes if x not in pruned_homes]
    drop_off_loc = list(to_drop.keys())

    to_add = [x for x in drop_off_loc if x not in homes_left]
    home_in_new_G = homes_left + to_add

    path = greedy_algorithm(G_pruned, home_in_new_G, start_ind)

    # make dropoff dictionary
    drop_off_dict = {}

    for home in homes_left:
        drop_off_dict[home] = [home]

    for loc in drop_off_loc:
        if loc not in drop_off_dict.keys():
            drop_off_dict[loc] = to_drop[loc]
        else:
            drop_off_dict[loc].extend(to_drop[loc])

    return path, drop_off_dict




def greedy_algorithm(graph, list_of_homes, starting_location):
    # all homes not visited yet, at the beginning that's just all home
    unvisited_home = [_ for _ in list_of_homes]

    # this variable tracks your current location
    currently_at = starting_location

    # what we want to return, a path that goes through all home, initialized as only having start point
    path = [starting_location]

    # while there are home remained unvisited
    while (len(unvisited_home) != 0):

        # extract all neighbors of the node we are currently at
        current_location_neighbors = list(graph.neighbors(currently_at))

        # all neighboring homes that unvisited
        neighboring_unvisited_homes = [neighbor for neighbor in current_location_neighbors if
                                       neighbor in unvisited_home]

        # If none of our neighbors are unvisited home, we have to run dijkstra to find the closest node
        if len(neighboring_unvisited_homes) == 0:

            # keep track of the shortest home so far
            nearest_node = unvisited_home[0]
            shortest_path_length = dijkstra_path_length(graph, currently_at, nearest_node)
            shortest_path = dijkstra_path(graph, currently_at, nearest_node)  # a list of path

            # loop through all unvisited nodes
            for home in unvisited_home:
                path_length = dijkstra_path_length(graph, currently_at, home)
                if (path_length < shortest_path_length):
                    shortest_path_length = path_length
                    shortest_path = dijkstra_path(graph, currently_at, home)
                    nearest_node = home
            # update path
            path.extend(shortest_path[1:])

            # update current location
            currently_at = nearest_node

            # remove the visited home from our list of unvisited home
            unvisited_home.remove(nearest_node)

        # Find the nearest unvisited home among all neighbors
        else:
            closest_neighboring_home = neighboring_unvisited_homes[0]
            closest_distance = graph.edges[currently_at, closest_neighboring_home]['weight']
            for node in neighboring_unvisited_homes:
                weight = graph.edges[currently_at, node]['weight']
                if (weight < closest_distance):
                    closest_distance = weight
                    closest_neighboring_home = node
            unvisited_home.remove(closest_neighboring_home)
            path.append(closest_neighboring_home)
            currently_at = closest_neighboring_home

    # from the home that is lastly visited we find a shortest path back to start point
    path_to_home = dijkstra_path(graph, path[-1], starting_location)
    path.extend(path_to_home[1:])

    return path


def name_to_index(list_of_locations):
    name_to_index_mapping = {}
    for i in range(len(list_of_locations)):
        name = list_of_locations[i]
        name_to_index_mapping[name] = i
    return name_to_index_mapping






