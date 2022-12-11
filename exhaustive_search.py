import getopt
import itertools
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
    plt.savefig("results/exhaustive_search/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".png")
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
    max_num_edges, edges_set, basic_operations_num, configurations_tested = [], set(), 2, 0 
    
    #Create list of edges, where each edge is a tuple of two vertices
    for vertice1 in edges: 
        max_num_edges.append(len(edges[vertice1])) #Add the number of edges of the vertice to the list
        basic_operations_num += 3  
        #For each vertice in the list of edges of the vertice1
        for vertice2 in edges[vertice1]: 
            basic_operations_num += 1
            # If the edge is not already in the set
            if (vertice2, vertice1) not in edges_set:
                edges_set.add((vertice1, vertice2)) #Add the edge to the set
                basic_operations_num += 1

    max_num_edges = int(sum(max_num_edges) / 2) # The number of edges is the sum of the number of edges of each vertice divided by 2
    basic_operations_num += 1

    # Create all possible combinations of edges
    for num_edges in range(1,max_num_edges):
        #Generate all num_edges size subsets of the edge set
        subsets = list(itertools.combinations(edges_set, num_edges))

        # For each subset, check if it is a dominating set
        for subset in subsets:
            configurations_tested += 1
            subset, is_solution = set(subset), True # Convert the subset to a set to use the intersection method
            edges_not_in_subset = edges_set - subset # Get the edges that are not in the subset
            basic_operations_num += 4
            # For each edge not in the subset, check if it has at least one vertice in the subset
            for edge in edges_not_in_subset: 
                basic_operations_num += (2 * num_edges) + 1
                #Check if the edge has a vertex in common with some edge of the subset
                if all(edge[0] not in i and edge[1] not in i for i in subset):
                    is_solution = False # If not, the subset is not a dominating set
                    basic_operations_num += 1
                    break
            basic_operations_num += 1
            if is_solution: # If the subset is a dominating set, return it
                return subset, basic_operations_num, configurations_tested
    return edges_set, basic_operations_num, configurations_tested # If no dominating set is found, return the edge set

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
        os.mkdir("results/exhaustive_search")
    elif not os.path.isdir("results/exhaustive_search"):
        os.mkdir("results/exhaustive_search")
        
    file = open("results/analyze_exhaustive_search.txt", 'w')
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