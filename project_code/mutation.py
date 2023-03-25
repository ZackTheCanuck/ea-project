# mutation methods
from ea_helpers import *
from population_individual import *     # may want to remove this later
import numpy as np
import shortest_path_algorithms


# select a route to mutate inversely proportional to how often the route appears in the individual
# this makes sense because it assumes there is some reason we have evolved to generate a route multiple times,
# therefore it is more likely beneficial that we keep it
def new_route(individual, all_routes, graph, start, end):
    probabilities    = get_inverse_traffic_flow_probabilities(individual, all_routes)
    all_routes_index = np.random.choice(range(len(all_routes)), p=probabilities)
    route_to_replace = all_routes[all_routes_index]
    
    route_index = individual.routes.index(route_to_replace)
    
    new_route = shortest_path_algorithms.dijkstra(graph, start, end)
    individual.routes[route_index] = new_route
    if new_route not in all_routes:
        all_routes.append(new_route)
    
    return individual

def random_p(individual, all_routes, graph, start, end):
    return individual

def link_wp(individual, all_routes, graph, start, end):
    return individual

def ex_segment(individual):
    # NOT TESTED
    route1, route2 = np.random.choice(individual.get_routes(), 2)   # select two copied routes uniformly at random
    rte_idx1 = np.where(individual = route1)                        # store indices of route for reinsertion
    rte_idx2 = np.where(individual = route2)
    
    route1 = remove_cycles(route1); route2 = remove_cycles(route2)
    shared_p = np.array(list(set(route1) & set(route2)))            # find nodes occurring in both routes
    diverge_p = np.empty(shared_p.shape)                            # divergence p are shared p w diff successor
    goto_p = np.empty(shared_p.shape)                               # goto p are shared p w diff predecessor after diverge_p
    for idx, p in enumerate(shared_p):
        i1 = np.where(route1 == p); i2 = np.where(route2 == p)      # locate indices of shared point
        if not i1+1 == len(route1) and not i2+1 == len(route2):     # check indices are not last in route
            if route1(i1+1) != route2(i2+1):                        # add p to divergence p if diff
                diverge_p[idx] = p
    v_s = np.random.choice(diverge_p)                               # choose a divergence point at random
    dp_idx1 = np.where(route1 == v_s)                               # find index of divergence point in route1
    dp_idx2 = np.where(route2 == v_s)                               # find index of divergence point in route2

    for idx, p in enumerate(shared_p):
        if not p != v_s:
            i1 = np.where(route1 == p); i2 = np.where(route2 == p)  # locate indices of shared point
            if (i1 > dp_idx1 and i2 > dp_idx2                       # if p occurs after divergence point in both routes
                and route1(i1-1) != route2(i2-1)):                  # and p is a goto p
                goto_p[idx] = p                                     # add p to goto p 
    v_t = np.random.choice(goto_p)                                  # choose a goto point occurring after v_s at random
    gt_idx1 = np.where(route1 == v_t)                               # find index of divergence point in route1
    gt_idx2 = np.where(route2 == v_t)                               # find index of divergence point in route2
    sub_rs1 = np.split(route1, [dp_idx1, gt_idx1])                  # split route1 into 3 subarrays 
    sub_rs2 = np.split(route2, [dp_idx2, gt_idx2])                  # split route2 into 3 subarrays
    route1 = np.concatenate(sub_rs1[0], sub_rs2[1], sub_rs1[2])     # swap subroutes between selected diverge_p & goto_p
    route2 = np.concatenate(sub_rs2[0], sub_rs1[1], sub_rs2[2])
    individual.routes[rte_idx1] = route1                            # replace routes in individual
    individual.routes[rte_idx2] = route2

    return individual