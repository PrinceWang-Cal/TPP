from student_utils import *


def graph_to_useful_nodes(original_graph, wanted_nodes, short_path_length_between):
    """
    Input: original graph, nodes to be included in result graph, shortest_path_length matrix
    Output: a graph only with nodes needed, connected by sp between nodes

    """
    new_graph = nx.Graph()
    for i in range(len(wanted_nodes)):
        source = wanted_nodes[i]
        for j in range(len(wanted_nodes)):
            target = wanted_nodes[j]
            if source != target:
                new_graph.add_edge(source, target, weight=short_path_length_between[source][target])

    return new_graph


def sp_matrix(graph, list_of_nodes):
    """
    Return two dictionaries the shortest paths matrix of the graph, all pairs of shortest path from i -> j
    shortest_paths = all the actual paths
    shortest_paths_lengths = length of all the actual path
    """

    shortest_paths = {}
    shortest_paths_lengths = {}
    for i in range(len(list_of_nodes)):
        source = list_of_nodes[i]
        shortest_paths[source] = {}
        shortest_paths_lengths[source] = {}
        for j in range(len(list_of_nodes)):
            target = list_of_nodes[j]
            if source != target:
                shortest_paths[source][target] = nx.shortest_path(graph, source=source, target=target)
                shortest_paths_lengths[source][target] = nx.shortest_path_length(graph, source=source, target=target)
    return shortest_paths, shortest_paths


def prune_leaf_home(original_graph, list_of_homes, starting):
    """

    :param original_graph: the original graph with all homes
    :param list_of_homes: all homes in the original graphs
    :return: a graph with only non_leaf homes, a dictionary of where to drop these homes
    """
    homes_to_prune = []
    home_to_dropoff = {}
    for home in list_of_homes:
        if original_graph.degree[home] == 1 and home != starting:
            homes_to_prune.append(home)
            key = list(original_graph.neighbors(home))[0]
            if key in home_to_dropoff.keys():
                home_to_dropoff[key].append(home)
            else:
                home_to_dropoff[key] = [home]

    for home in homes_to_prune:
        original_graph.remove_node(home)

    return original_graph, home_to_dropoff, homes_to_prune
