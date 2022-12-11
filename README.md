# Algoritmos Avançados 2nd Project — Randomized Algorithms for Combinatorial Problems

## Introduction

Problem 20 – Find a minimum edge dominating set for a given undirected graph G(V, E), with n vertices and m edges. An edge dominating set of G is a subset D of edges, such that every edge not in D is adjacent to, at least, one edge in D. A minimum edge dominating set is an edge dominating set of smallest possible size.

Design and test a randomized algorithm to solve the Minimum edge dominating set.

## How to run

### Start by installing the requeriments, creating a virtual environment for that:
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requeriments.txt
```

### CLI optional arguments 

First generate graphs and then test them in the developed algorithms.

We can pass as an argument the number of vertices of the last graph to be generated (this program starts generating graphs from 2 vertices). This argument is passed by "-v".

We can also pass as an argument the maximum number of coordinates that a vertex can have (the minimum is 1), this through the "-m"
```
python3 graphs_creator.py -v 350 -m 355
```

To run the algorithms:
```
python3 greedy_heuristics.py -v 350
python3 exhaustive_search.py -v 13
python3 randomized_algorithm.py -g SW
python3 randomized_algorithm.py -v 188 -g graphs_creator
```

To run the Randomized Algorithm we can use the graphs we want to analyze as an argument.
In the "-g" argument if we pass:
* "SW" : the algorithm runs with the SW graphs that the teacher provided
* "graphs_creator" : the algorithm is executed with the graphs created by graph creator

## Author
Eva Bartolomeu, Nmec 98513