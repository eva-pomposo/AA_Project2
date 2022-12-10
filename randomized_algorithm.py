import getopt
import itertools
import json
import math
import os
import random
import sys
import time
import networkx as nx
import matplotlib.pyplot as plt

def create_graphic_image(vertices, edges_set, num_vertices, percentage):
    G = nx.Graph() # Create a graph
    for edge in edges_set: 
        G.add_node(edge[0], pos=vertices[edge[0]]) 
        G.add_node(edge[1], pos=vertices[edge[1]])
        G.add_edge(*edge) # Add the edge to the graph
    nx.draw(G, pos=nx.get_node_attributes(G,'pos'), with_labels = True, node_color='lightblue')
    plt.savefig("results/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".png")
    plt.clf()

def read_graph(num_vertices, percentage):
    # Read the graph from the file
    file = open("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", "r")
    vertices = file.readline()[:-1].replace("'", "\"").replace("(", "[").replace(")", "]")
    edges = file.readline().replace("'", "\"")
    file.close()
    vertices = {int(key):(value[0], value[1]) for key,value in json.loads(vertices).items()}
    edges = {int(key):value for key,value in json.loads(edges).items()}
    return vertices, edges

def min_edge_dominating_set(vertices, edges):
    result, basic_operations_num, configurations_tested = set(), 0, 0 
    
    print("Vertices: ", vertices)
    print("Edges: ", edges)
    # Iterating through the randomly generated candidate solutions
    for i in range( math.ceil(0.60 * (2**len(vertices) - 1) ) ): 
        configurations_tested += 1
        candidate_solution = set()
        edges_copy = {key:value[:] for key,value in edges.items()} # Copy the edges
        while edges_copy: # While the graph is not empty
            # Select a random edge
            vertice1 = random.choice(list(edges_copy.keys()))
            vertice2 = random.choice(edges_copy[vertice1])
            print("Vertice1: ", vertice1)
            print("Vertice2: ", vertice2)

            adjacent_vertices = set(edges_copy[vertice1] + edges_copy[vertice2]) # Get the adjacent vertices of the edge
            #remove the edge from adjacent vertices
            adjacent_vertices.remove(vertice1)  
            adjacent_vertices.remove(vertice2)

            # Remove the edge from the graph and the adjacent vertices 
            del edges_copy[vertice1] 
            del edges_copy[vertice2]

            # Remove the adjacent vertices from the graph
            for vertice in adjacent_vertices: # For each adjacent vertice
                adjacent_list = edges_copy[vertice] # Get the adjacent list of the vertice
                if vertice1 in adjacent_list: # If the vertice is adjacent to the vertice1
                    adjacent_list.remove(vertice1) # Remove the vertice from the adjacent list
                if vertice2 in adjacent_list: # If the vertice is adjacent to the vertice2
                    adjacent_list.remove(vertice2) # Remove the vertice from the adjacent list
                if not adjacent_list: del edges_copy[vertice] # If the adjacent list is empty, remove the vertice from the graph
                else: edges_copy[vertice] = adjacent_list # Save the adjacent list
                basic_operations_num += 5

            # Save the edge to the candidate solution
            candidate_solution.add((vertice1, vertice2))
            basic_operations_num += 7

        if len(candidate_solution) < len(result) or not result: # If the candidate solution is better than the current solution or the current solution is empty
            result = candidate_solution # Save the candidate solution as the current solution
    print("Dominating set found: ", result)
    return result, basic_operations_num, configurations_tested # If no dominating set is found, return the edge set

def read_arguments():
    # Remove 1st argument from the list of command line arguments
    argumentList = sys.argv[1:]
    
    # Options
    options = "v:"
    long_options = ["Vertices_Num_Last_Graph"]
    
    vertices_num_last_graph = 10
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # Checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-v", "--Vertices_Num_Last_Graph"):
                vertices_num_last_graph = int(currentValue)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
    return vertices_num_last_graph

def main():
    random.seed(98513)
    # Create the results folders if they don't exist already
    if not os.path.isdir("results"): 
        os.mkdir("results")
        
    file = open("results/analyze_randomized_algorithm.txt", 'w')
    file.write("vertices_num percentage_max_num_edges solution_size basic_operations_num configurations_tested execution_time\n")
    solutions = []

    #Read graphs and determine the min edge dominating set with 2, 3, 4, ... vertices
    for vertices_num in range(2, read_arguments() + 1):
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            vertices, edges = read_graph(vertices_num, percentage)

            execution_time = time.time() # Start the execution time counter
            solution_edges, basic_operations_num, configurations_tested = min_edge_dominating_set(vertices, edges)
            execution_time = time.time() - execution_time # Stop the execution time counter

            # Write the results to the file
            file.write("%s %f %s %s %s %f\n" % (vertices_num, percentage, len(solution_edges), basic_operations_num, configurations_tested, execution_time))
            solutions.append((vertices, solution_edges, vertices_num, percentage)) # Save the solution to plot it later
    
    file.close()
    
    print("Create and save image of solution graphs...")
    for solution in solutions:
        create_graphic_image(*solution)
        
if __name__ == "__main__":
    main()