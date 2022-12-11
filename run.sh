#!/bin/bash

# bash command to create graphs
python3 graphs_creator.py -v 350 -m 355
# bash command to solve graphs problems with greedy heuristic
python3 greedy_heuristics.py -v 350
# bash command to solve graphs problems with exhaustive search
python3 exhaustive_search.py -v 13
# bash command to run randomized algorithm whith SW graphs
python3 randomized_algorithm.py -g SW
# bash command to run randomized algorithm with the graphs that come from the graphs_creator.py
python3 randomized_algorithm.py -v 188 -g graphs_creator