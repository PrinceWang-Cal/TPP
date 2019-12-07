from student_utils import *


def has_leaf_home(G, list_of_homes):
    """Check if there's a leaf home"""
    for home in list_of_homes:
        if G.degree(home) == 1:
            return True
    return False


def prune_homes(G, list_of_homes):
    """Prune all home that is a leaf"""
    leaf_drop_off_dict = {}
    left_home = []
    while has_leaf_home(G, list_of_homes):
        for home in list_of_homes:
            if G.degree(home) == 1:
                leaf_drop_off_dict[home] = G.neighbors(home)  # map the leaf to the node above it
                if home in leaf_drop_off_dict.values():
                    for key in leaf_drop_off_dict.keys():
                        if leaf_drop_off_dict[key] == home:
                            leaf_drop_off_dict[key] = leaf_drop_off_dict[home]
                G.remove_node(home)
            elif home not in left_home:
                left_home.append(home)
            #list_of_homes.remove(home)

    map_leaf_to_drop_off(leaf_drop_off_dict, G, left_home) #list_of_homes)
    return G, leaf_drop_off_dict, left_home


def map_leaf_to_drop_off(leaf_drop_off_dict, G, list_of_homes):
    """Map the pruned leaves(homes) to the closest home that is not pruned"""
    for leaf in leaf_drop_off_dict.keys():
        source_node = leaf_drop_off_dict[leaf]
        parent_list = nx.edge_bfs(G, source_node)
        for parent in parent_list:
            if parent[1] in list_of_homes:
                leaf_drop_off_dict[leaf] = parent[1]
                # remember the edge case when there's no home on the path to the leaf home
                break
