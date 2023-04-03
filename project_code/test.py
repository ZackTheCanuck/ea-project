from population_individual import *
from diversity import *
from mutation import *
from graph_helpers import *
import random

def test_mut():
    toronto_graph, geodata = build_graph()
    start_node, end_node = random.sample(list(toronto_graph.nodes), 2)
    print(f'Starting run from {start_node} -> {end_node}')
    indiv = individual(toronto_graph, start_node, end_node)
    print(ex_segment(indiv, None, None, None, None))

def test_div():
    toronto_graph, geodata = build_graph()
    start_node, end_node = random.sample(list(toronto_graph.nodes), 2)
    print(f'Starting run from {start_node} -> {end_node}')
    indiv = individual(toronto_graph, start_node, end_node)
    print(diversity_func(indiv))

test_div()