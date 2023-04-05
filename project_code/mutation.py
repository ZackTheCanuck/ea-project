# mutation methods
import random

import numpy as np
import shortest_path_algorithms
from ea_helpers import *
from population_individual import *  # may want to remove this later


# select a route to mutate inversely proportional to how often the route appears in the individual
# this makes sense because it assumes there is some reason we have evolved to generate a route multiple times,
# therefore it is more likely beneficial that we keep it
def new_route(individual, all_routes, graph, spa_v, start, end):
    probabilities    = get_inverse_traffic_flow_probabilities(individual, all_routes)
    all_routes_index = np.random.choice(range(len(all_routes)), p=probabilities)
    route_to_replace = all_routes[all_routes_index]
    route_index      = individual.get_route_index(route_to_replace)
    new_route        = spa_v(graph, start, end)
    individual.update_route_at_index(index=route_index, new_route=new_route)
    if new_route not in all_routes:
        all_routes.append(new_route)
    
    return individual


def random_p(individual, all_unique_routes, graph, spa_v, start_node, end_node):

    # Choose a random subset of routes proportional to their inverse traffic flow
    probabilities = get_inverse_traffic_flow_probabilities(individual, all_unique_routes)
    # Select a random subset of route indices from all_unique_routes based on probabilities
    selected_routes_indices = np.random.choice(len(all_unique_routes), size=individual.get_num_routes() // 2, replace=False, p=probabilities)
    # Get the routes corresponding to the selected indices
    selected_routes = []
    for i in selected_routes_indices:
        selected_routes.append(all_unique_routes[i])
    for route in selected_routes:
        # Choose a start node and destination node
        route_length = len(route)
        start_index = random.randint(0, route_length - 2)
        max_subroute_length = route_length - start_index
        subroute_length = max(min(abs(int(np.random.normal(0.25 * route_length, 0.5 * route_length))), max_subroute_length), 2)
        end_index = start_index + subroute_length - 1
        # Replace subsegment with a new random route
        new_subroute = spa_v(graph, route[start_index], route[end_index])
        new_route    = route[:start_index] + new_subroute[:-1] + route[end_index:]
        new_route    = remove_cycles(new_route)
        #print(route, new_subroute, new_route)
        index        = individual.get_route_index(route)
        individual.update_route_at_index(index, new_route)

    # Update all_unique_routes with new routes
    for route in individual.get_routes():
        if route not in all_unique_routes:
            all_unique_routes.append(route)

    return individual

# instead of using capacity (which our data doesn't have), we take the sum of our fitnesses along each edge going out of each node,
# except the one we are currently using, and choose proportional to the fastest (lowest fitness) node
def link_wp(individual, all_unique_routes, graph, spa_v, start, end):
    # Choose a random subset of routes proportional to their inverse traffic flow
    probabilities = get_inverse_traffic_flow_probabilities(individual, all_unique_routes)
    # Select a random subset of route indices from all_unique_routes based on probabilities
    selected_routes_indices = np.random.choice(len(all_unique_routes), size=individual.get_num_routes() // 2, replace=False, p=probabilities)
    # Get the routes corresponding to the selected indices
    selected_routes = []
    for i in selected_routes_indices:
        selected_routes.append(all_unique_routes[i])
    for route in selected_routes:
        route_edges = list(zip(route, route[1:]))
        node_probs = []
        for i in range(len(route)):
            node_out_edges = individual.graph.out_edges(route[i])
            outbound_travel_times = [individual.get_edge_travel_time(edge[0], edge[1]) for edge in node_out_edges if edge not in route_edges]
            node_probs.append(sum(outbound_travel_times))
        percentages = [prob/sum(node_probs) for prob in node_probs]

        # Choose a start node and destination node
        num_nodes = len(node_probs)
        # select start and end indexes with shorter times more likely to be picked
        non_selected_indexes = np.random.choice(num_nodes, num_nodes - 2, replace=False, p=percentages)
        selected_indexes     = [i for i in range(num_nodes) if i not in non_selected_indexes]
        start_index  = min(selected_indexes)
        end_index    = max(selected_indexes)
        # Replace subsegment with a new random route
        new_subroute = spa_v(graph, route[start_index], route[end_index])
        new_route    = route[:start_index] + new_subroute[:-1] + route[end_index:]
        new_route    = remove_cycles(new_route)
        index        = individual.get_route_index(route)
        individual.update_route_at_index(index, new_route)

    # Update all_unique_routes with new routes
    for route in individual.get_routes():
        if route not in all_unique_routes:
            all_unique_routes.append(route)

    return individual

def ex_segment(individual, all_unique_routes, graph, spa_v, start, end):         
    """Outdated, works when get_routes() returns ndarray"""  
    # routes = individual.get_routes()      
    # r1, r2 = np.random.choice(len(routes), 2, replace=False)        # select two copied routes uniformly at random
    # route1 = routes[r1]; route2 = routes[r2]
    # route1 = remove_cycles(route1); route2 = remove_cycles(route2)
    # shared_p = np.array(list(set(route1) & set(route2)))            # find nodes occurring in both routes
    # diverge_p = np.full(shared_p.shape, -1, dtype=int)              # divergence p are shared p w diff successor                        
    # goto_p = np.full(shared_p.shape, -1, dtype=int)                 # goto p are shared p w diff predecessor after diverge_p
    # for idx, p in enumerate(shared_p):
    #     i1 = np.where(route1 == p)[0][0]                            # locate indices of shared point
    #     i2 = np.where(route2 == p)[0][0]    
    #     if not i1+1 == len(route1) and not i2+1 == len(route2):     # check indices are not last in route
    #         if route1[i1+1] != route2[i2+1]:                        # add p to divergence p if diff
    #             diverge_p[idx] = p
    # delete_i = np.where(diverge_p == -1)[0]
    # diverge_p = np.delete(diverge_p, delete_i)
    # v_s = np.random.choice(diverge_p)                               # choose a divergence point at random
    # dp1 = np.where(route1 == v_s)[0][0]                             # find index of divergence point in route1
    # dp2 = np.where(route2 == v_s)[0][0]                             # find index of divergence point in route2

    # for idx, p in enumerate(shared_p):
    #     if not p != v_s:
    #         i1 = np.where(route1 == p); i2 = np.where(route2 == p)  # locate indices of shared point
    #         if (i1 > dp1 and i2 > dp2                               # if p occurs after divergence point in both routes
    #             and route1[i1-1] != route2[i2-1]):                  # and p is a goto p
    #             goto_p[idx] = p                                     # add p to goto p 
    # delete_i = np.where(goto_p == -1)[0]
    # goto_p = np.delete(goto_p, delete_i)
    # v_t = np.random.choice(goto_p)                                  # choose a goto point occurring after v_s at random
    # gt1 = np.where(route1 == v_t)[0][0]                             # find index of divergence point in route1
    # gt2 = np.where(route2 == v_t)[0][0]                             # find index of divergence point in route2
    # sub_rs1 = np.split(route1, [dp1, gt1])                          # split route1 into 3 subarrays 
    # sub_rs2 = np.split(route2, [dp2, gt2])                          # split route2 into 3 subarrays
    # route1 = np.concatenate(sub_rs1[0], sub_rs2[1], sub_rs1[2])     # swap subroutes between selected diverge_p & goto_p
    # route2 = np.concatenate(sub_rs2[0], sub_rs1[1], sub_rs2[2])
    # individual.update_route_at_index(r1, route1)                    # replace routes in individual
    # individual.update_route_at_index(r2, route2) 

    return individual