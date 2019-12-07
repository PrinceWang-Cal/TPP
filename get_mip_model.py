from __future__ import print_function
from ortools.linear_solver import pywraplp


def get_mip_model(list_homes, list_locations, source_index, list_edges):
    solver = pywraplp.Solver('drop-tas',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    infinity = solver.infinity()
    """Add "drop TA k at i" variables with constraints"""
    drop_k_at_i_array = []
    for i in range(len(list_locations)):
        for k in range(len(list_homes)):
            drop_k_at_i_array[i][k] = solver.IntVar(0, 1, str(i) + '_' + str(k))

    """Add vertices variables with constraints"""
    loc_visited_array = []
    loc_visited_array[source_index] = 1
    for i in range(len(list_locations)):
        if i == source_index:
            break
        loc_visited_array[i] = solver.IntVar(0, infinity, 'y' + str(i))

    """Add edges variables with constraints"""
    edge_visited_array = []
    for i in range(len(list_edges)):
        edge_visited_array[i] = solver.IntVar(0, infinity, 'x' + str(i))

    """Add 'sum to one constrains' variables with constraints"""
    sum_of_ta_drop = []
    for k in range(len(list_homes)):
        sum_of_ta_drop[k] = 0
        for i in range(len(list_locations)):
            sum_of_ta_drop[k] += drop_k_at_i_array[i][k]
        solver.Add(sum_of_ta_drop[k] == 1)
