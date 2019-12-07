import networkx as nx
import pruned_graph_gen as pg

from graph_utils import *


def prune_leaf_tsp_solver(original_graph, list_of_homes, starting_point, sp_mat, sp_length):
    """Remove all non_home locations:"""
    all_home_graph = graph_to_useful_nodes(original_graph, list_of_homes, sp_length)
    """Prune all homes that are leaves"""
    all_non_leaf_homes = prune_leaf_home(all_home_graph, list_of_homes)
    """Run tsp on the left homes"""




def prune_mst_solver(original_graph, list_of_homes, starting_point):
    # Get the pruned graph with no home leaves, get the drop_off locations for the leave pruned
    pruned_home_leaf_graph, leaf_mapping, new_list_of_homes = pg.prune_homes(original_graph, list_of_homes)
    # remove non_home locations, replace path between homes with the shortest path, return a 2_D array of shortest paths
    only_home_graph, short_paths_between = remove_non_home(pruned_home_leaf_graph, new_list_of_homes)
    # Find MST of the updated only homes graph
    mst_only_homes = graph_to_mst(only_home_graph)
    # Call traverse the mst using dfs, return a tour
    dfs_path = dfs_ordering(mst_only_homes, starting_point)
    # Using the shortest paths 2D array, convert tour back to original graph with other locations
    final_tour = dfs_to_tour(short_paths_between, dfs_path)
    # Drop all TAs as their own homes on the kept homes, drop leaf_home TAs at the closest homes
    drop_mapping = drop_off_list_all(leaf_mapping, final_tour)

    return final_tour, drop_mapping

# remove all non_home locations, connect homes by an edge of which length = shortest path
def remove_non_home(original_g, list_of_homes):
    """Remove non_home locations, replace with edges of shortest path length"""
    g_homes = nx.Graph()
    sp_paths = {}

    for i in range(len(list_of_homes)):
        source = list_of_homes[i]
        sp_paths[source] = {}
        for j in range(len(list_of_homes)):
            target = list_of_homes[j]
            if target != source:
                sp_ij_len = nx.shortest_path_length(original_g, source, target)
                g_homes.add_edge(source, target, weight=sp_ij_len)
                path = nx.shortest_path(original_g, source, target)
                sp_paths[source][target] = path

    return g_homes, sp_paths



def graph_to_mst(G):
    mst = nx.minimum_spanning_tree(G)
    return mst


def dfs_ordering(mst, starting_point):
    pre_ordering = list(nx.dfs_preorder_nodes(mst, source=starting_point))
    pre_ordering.append(starting_point)
    return pre_ordering


def dfs_to_tour(sp_between, dfs):
    final_tour = [dfs[0]]
    for i in range(len(dfs) - 1):
        start = dfs[i]
        end = dfs[i + 1]
        path = sp_between[start][end]
        final_tour.extend(path[1:])
    return final_tour


def drop_off_list_all(leaf_drop_off_dict, final_tour):
    all_locations = {}
    for i in range(len(final_tour)):
        drop_off = final_tour[i]
        all_locations[drop_off] = [drop_off]
    for key in leaf_drop_off_dict.keys():
        drop_off_loc = leaf_drop_off_dict[key]
        all_locations[drop_off_loc].append(key)
    return all_locations


