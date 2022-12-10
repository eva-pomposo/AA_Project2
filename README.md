# Algoritmos Avançados 2nd Project — Randomized Algorithms for Combinatorial Problems

## Introduction

Problem 20 – Find a minimum edge dominating set for a given undirected graph G(V, E), with n vertices and m edges. An edge dominating set of G is a subset D of edges, such that every edge not in D is adjacent to, at least, one edge in D. A minimum edge dominating set is an edge dominating set of smallest possible size.

## How to run

### Start by installing the requeriments, creating a virtual environment for that:
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requeriments.txt
```

### CLI optional arguments 

First generate graphs and then test them in the developed algorithm.

We can pass as an argument the number of vertices of the last graph to be generated (this program starts generating graphs from 2 vertices). This argument is passed by "-v".

We can also pass as an argument the maximum number of coordinates that a vertex can have (the minimum is 1), this through the "-m"
```
python3 graphs_creator.py -v 350 -m 355
```

To run the algorithm:
```
```

## Author
Eva Bartolomeu, Nmec 98513