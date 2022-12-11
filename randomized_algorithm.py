import getopt
import json
import math
import os
import random
import sys
import time
import networkx as nx
import matplotlib.pyplot as plt
import copy

def create_graphic_image(vertices, edges_set, num_vertices, percentage, graphs_from):
    G = nx.Graph() # Create a graph
    for edge in edges_set: 
        G.add_node(edge[0], pos=vertices[edge[0]]) 
        G.add_node(edge[1], pos=vertices[edge[1]])
        G.add_edge(*edge) # Add the edge to the graph
    nx.draw(G, pos=nx.get_node_attributes(G,'pos'), with_labels = True, node_color='lightblue')
    plt.savefig("results/" + graphs_from + "/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".png")
    plt.clf()

def read_from_graphs_creator(num_vertices, percentage):
    # Read the graph from the file
    file = open("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", "r")
    vertices = file.readline()[:-1].replace("'", "\"").replace("(", "[").replace(")", "]")
    edges = file.readline().replace("'", "\"")
    file.close()
    vertices = {int(key):(value[0], value[1]) for key,value in json.loads(vertices).items()}
    edges_dict = {}
    num_edges = 0
    for key,value in json.loads(edges).items():
        edges_dict[int(key)] = value
        num_edges += len(value)
    num_edges /= 2
    return vertices, edges_dict, int(num_edges)

def read_from_SW(file_name):
    # Read the graph from the file
    file = open("SW_ALGUNS_GRAFOS/" + file_name, "r") # Open the file

    # Ignore the first two properties, which are not needed for algorithm development
    file.readline()
    file.readline()

    num_vertices = int(file.readline()) # Read the number of vertices
    num_edges = int(file.readline()) # Read the number of edges
    edges = {} # Dictionary of edges
    
    # Read the edges
    for i in range(num_edges): # For each edge
        vertice1, vertice2 = file.readline().split() # Read the edge
        vertice1, vertice2 = int(vertice1), int(vertice2) # Convert the edge to int
        # Add the edge to the dictionary
        if vertice1 in edges: edges[vertice1].append(vertice2) 
        else: edges[vertice1] = [vertice2] 
        if vertice2 in edges: edges[vertice2].append(vertice1) 
        else: edges[vertice2] = [vertice1]
    file.close() # Close the file
    return num_vertices, num_edges, edges # Return the number of vertices, the number of edges and the edges

def randomized_algorithm(edges, num_edges):
    execution_time = time.time() # Start the execution time counter
    result, basic_operations_num, configurations_tested = set(), 0, 0 
    
    # Iterating through the randomly generated candidate solutions
    for i in range( max(2,math.ceil(0.23 * math.log(2**(num_edges) - 1) ) ) ): 
        configurations_tested += 1
        candidate_solution = set()
        edges_copy = copy.deepcopy(edges) # Copy the edges
        basic_operations_num += 2
        while edges_copy: # While the graph is not empty
            # Select a random edge
            vertice1 = random.choice(list(edges_copy.keys()))
            vertice2 = random.choice(edges_copy[vertice1])

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
            basic_operations_num += 8

        if len(candidate_solution) < len(result) or not result: # If the candidate solution is better than the current solution or the current solution is empty
            result = candidate_solution # Save the candidate solution as the current solution
    execution_time = time.time() - execution_time # Stop the execution time counter
    return result, execution_time, basic_operations_num, configurations_tested # Return the min edge dominating set

def algorithm_for_graphs_creator(vertices_num_last_graph, graphs_from):
    file = open("results/" + graphs_from + "/analyze_randomized_algorithm.txt", 'w')
    file.write("vertices_num percentage_max_num_edges solution_size basic_operations_num configurations_tested execution_time\n")
    solutions = []

    #Read graphs and determine the min edge dominating set with 2, 3, 4, ... vertices
    for vertices_num in range(2, vertices_num_last_graph + 1):
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            vertices, edges, edges_num = read_from_graphs_creator(vertices_num, percentage)

            solution_edges, execution_time, basic_operations_num, configurations_tested = randomized_algorithm(edges, edges_num)

            # Write the results to the file
            file.write("%s %f %s %s %s %f\n" % (vertices_num, percentage, len(solution_edges), basic_operations_num, configurations_tested, execution_time))
            solutions.append((vertices, solution_edges, vertices_num, percentage)) # Save the solution to plot it later
    
    file.close()
    
    print("Create and save image of solution graphs...")
    for solution in solutions:
        create_graphic_image(*solution, graphs_from)

def algorithm_for_SW(graphs_from):
    file = open("results/" + graphs_from + "/analyze_randomized_algorithm.txt", 'w')
    file.write("vertices_num edges_num solution_size basic_operations_num configurations_tested execution_time\n")

    #Read graphs that are in folder SW_ALGUNS_GRAFOS and determine the min edge dominating set
    for file_name in os.listdir("SW_ALGUNS_GRAFOS"):
        vertices_num, edges_num, edges = read_from_SW(file_name)

        solution_edges, execution_time, basic_operations_num, configurations_tested = randomized_algorithm(edges, edges_num)

        # Write the results to the file
        file.write("%s %s %s %s %s %f\n" % (vertices_num, edges_num, len(solution_edges), basic_operations_num, configurations_tested, execution_time))

    file.close()

def read_arguments():
    # Remove 1st argument from the list of command line arguments
    argumentList = sys.argv[1:]
    
    # Options
    options = "v:g:"
    long_options = ["Vertices_Num_Last_Graph", "Graphs_From"]
    
    vertices_num_last_graph = 10
    graphs_from = "graphs_creator"
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # Checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-v", "--Vertices_Num_Last_Graph"):
                vertices_num_last_graph = int(currentValue)
            elif currentArgument in ("-g", "--Graphs_From"):
                graphs_from = currentValue
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
    return vertices_num_last_graph, graphs_from

def main():
    random.seed(98513)
    vertices_num_last_graph, graphs_from = read_arguments()

    if graphs_from == "graphs_creator":
        algorithm_for_graphs_creator(vertices_num_last_graph, graphs_from)
    elif graphs_from == "SW":
        algorithm_for_SW(graphs_from)
        
if __name__ == "__main__":
    main()