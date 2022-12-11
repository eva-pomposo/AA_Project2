import getopt
import json
import os
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
    plt.savefig("results/greedy_heuristics/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".png")
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
    sorted_edges = dict(sorted(edges.items(), key = lambda entry: len(entry[1]), reverse=True)) # Sort the edges by the number of vertices they connect
    sorted_edges = { key:sorted(value, key = lambda vertice: list(sorted_edges.keys()).index(vertice)) for key,value in sorted_edges.items() } # Sort the vertices of each value by the number of edges they connect
    result, basic_operations_num = set(), 5 # Initialize the result and the number of basic operations

    # Iterate over the edges
    while sorted_edges:
        vertice1_max_adjacency = list(sorted_edges.keys())[0] # Get the vertice with the maximum number of edges
        adjacent_vertices = sorted_edges[vertice1_max_adjacency] # Get the adjacent vertices of the vertice1 
        vertice2_max_adjacency = adjacent_vertices[0] # Get the adjacent vertice with the maximum number of edges
        
        result.add((vertice1_max_adjacency, vertice2_max_adjacency)) # Add the edge to the result
        del sorted_edges[vertice1_max_adjacency] # Delete the edge from the edges
    
        if vertice2_max_adjacency in sorted_edges.keys(): # If the vertice2 is in the edges
            adjacent_vertices = adjacent_vertices + sorted_edges[vertice2_max_adjacency] # Add the adjacent vertices of the vertice2 to the adjacent_vertices
            del sorted_edges[vertice2_max_adjacency] # Delete the edge from the edges
            basic_operations_num += 5 

        basic_operations_num += 10
        for vertice in set(adjacent_vertices): # Iterate over the adjacent vertices
            if vertice in sorted_edges.keys(): # If the vertice is in the edges
                adjacency_list = sorted_edges[vertice] # Get the adjacency list of the vertice
                if vertice1_max_adjacency in adjacency_list: # If the vertice1 is in the adjacency list
                    adjacency_list.remove(vertice1_max_adjacency) # Remove the vertice1 from the adjacency list
                    basic_operations_num += 1
                if vertice2_max_adjacency in adjacency_list: # If the vertice2 is in the adjacency list
                    adjacency_list.remove(vertice2_max_adjacency) # Remove the vertice2 from the adjacency list
                    basic_operations_num += 1
                if len(adjacency_list) != 0: # If the adjacency list is not empty
                    sorted_edges[vertice] = adjacency_list # Update the adjacency list of the vertice
                    basic_operations_num += 6
                else: # If the adjacency list is empty
                    del sorted_edges[vertice] # Delete the vertice from the edges
                    basic_operations_num += 8
            basic_operations_num +=1
                
    return result, basic_operations_num 
    
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
    # Create the results folders if they don't exist already
    if not os.path.isdir("results"): 
        os.mkdir("results")
        os.mkdir("results/greedy_heuristics")
    elif not os.path.isdir("results/greedy_heuristics"):
        os.mkdir("results/greedy_heuristics")

    file = open("results/analyze_greedy.txt", 'w')
    file.write("vertices_num percentage_max_num_edges solution_size basic_operations_num execution_time\n")
    solutions = []
    
    #Read graphs and determine the min edge dominating set with 2, 3, 4, ... vertices
    for vertices_num in range(2, read_arguments() + 1):
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            vertices, edges = read_graph(vertices_num, percentage)

            execution_time = time.time() # Start the execution time counter
            solution_edges, basic_operations_num = min_edge_dominating_set(vertices, edges)
            execution_time = time.time() - execution_time # Stop the execution time counter

            # Write the results to the file
            file.write("%s %f %s %s %f\n" % (vertices_num, percentage, len(solution_edges), basic_operations_num, execution_time))
            solutions.append((vertices, solution_edges, vertices_num, percentage)) # Save the solution to plot it later
    
    file.close()
    
    print("Create and save image of solution graphs...")
    for solution in solutions:
        create_graphic_image(*solution)

if __name__ == "__main__":
    main()