import pandas as pd
import matplotlib.pyplot as plt

def compare_all_solutions(exhaustive_search, greedy, randomized_graphs_creator):
    exhaustive_search_vertices_num = exhaustive_search['vertices_num']
    exhaustive_search_percentage_max_num_edges = exhaustive_search['percentage_max_num_edges']
    exhaustive_search_solution_size = exhaustive_search['solution_size']
    rows_num = exhaustive_search_vertices_num.size
    greedy_vertices_num = greedy['vertices_num'][:rows_num]
    greedy_percentage_max_num_edges = greedy['percentage_max_num_edges'][:rows_num]
    greedy_solution_size = greedy['solution_size'][:rows_num]
    randomized_graphs_creator_vertices_num = randomized_graphs_creator['vertices_num'][:rows_num]
    randomized_graphs_creator_percentage_max_num_edges = randomized_graphs_creator['percentage_max_num_edges'][:rows_num]
    randomized_graphs_creator_solution_size = randomized_graphs_creator['solution_size'][:rows_num]

    for percentage in [0.125, 0.25, 0.50, 0.75]:
        plt.scatter(exhaustive_search_vertices_num[exhaustive_search_percentage_max_num_edges == percentage],exhaustive_search_solution_size[exhaustive_search_percentage_max_num_edges == percentage],c="r",marker="+", label="Exhaustive Search")
        plt.scatter(greedy_vertices_num[greedy_percentage_max_num_edges == percentage],greedy_solution_size[greedy_percentage_max_num_edges == percentage],c="b",marker="x", label="Greedy")
        plt.scatter(randomized_graphs_creator_vertices_num[randomized_graphs_creator_percentage_max_num_edges == percentage],randomized_graphs_creator_solution_size[randomized_graphs_creator_percentage_max_num_edges == percentage],c="g",marker="v", label="Randomized Graphs Creator")
        plt.legend()
        plt.title('Solution Size for each Experiment with Percentage max num edges ' + str(percentage))
        plt.xlabel('Vertices Number')
        plt.ylabel('Solution Size')
        plt.savefig("graphics/solutions_sizes_percentage_" + str(percentage) + ".png")
        plt.clf()

def compare_greedy_randomized_solutions(greedy, randomized_graphs_creator):
    randomized_graphs_creator_vertices_num = randomized_graphs_creator['vertices_num']
    randomized_graphs_creator_percentage_max_num_edges = randomized_graphs_creator['percentage_max_num_edges']
    randomized_graphs_creator_solution_size = randomized_graphs_creator['solution_size']
    rows_num = randomized_graphs_creator_vertices_num.size
    greedy_vertices_num = greedy['vertices_num'][:rows_num]
    greedy_percentage_max_num_edges = greedy['percentage_max_num_edges'][:rows_num]
    greedy_solution_size = greedy['solution_size'][:rows_num]

    for percentage in [0.125, 0.25, 0.50, 0.75]:
        plt.scatter(greedy_vertices_num[greedy_percentage_max_num_edges == percentage],greedy_solution_size[greedy_percentage_max_num_edges == percentage],c="b",marker="x", label="Greedy")
        plt.scatter(randomized_graphs_creator_vertices_num[randomized_graphs_creator_percentage_max_num_edges == percentage],randomized_graphs_creator_solution_size[randomized_graphs_creator_percentage_max_num_edges == percentage],c="g",marker="v", label="Randomized Graphs Creator")
        plt.legend()
        plt.title('Solution Sizes for Greedy and Randomized with Percentage max num edges ' + str(percentage))
        plt.xlabel('Vertices Number')
        plt.ylabel('Solution Size')
        plt.savefig("graphics/greedy_randomized_solutions_sizes_percentage_" + str(percentage) + ".png")
        plt.clf()

    
def configurations_tested(data, algorithm_name):
    vertices_num = data['vertices_num']
    percentage_max_num_edges = data['percentage_max_num_edges']
    configurations_tested = data['configurations_tested']

    if algorithm_name == "Exhaustive Search":
        plt.plot(vertices_num[percentage_max_num_edges == 0.125],configurations_tested[percentage_max_num_edges == 0.125],c="r",marker="+", label="Percentage max num edges 0.125")
        plt.plot(vertices_num[percentage_max_num_edges == 0.25],configurations_tested[percentage_max_num_edges == 0.25],c="b",marker="o", label="Percentage max num edges 0.25")
        plt.plot(vertices_num[percentage_max_num_edges == 0.5],configurations_tested[percentage_max_num_edges == 0.5],c="g",marker="x", label="Percentage max num edges 0.5")
        plt.plot(vertices_num[percentage_max_num_edges == 0.75],configurations_tested[percentage_max_num_edges == 0.75],c="y",marker="v", label="Percentage max num edges 0.75")
    else:
        plt.scatter(vertices_num[percentage_max_num_edges == 0.125],configurations_tested[percentage_max_num_edges == 0.125],c="r",marker="+", label="Percentage max num edges 0.125")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.25],configurations_tested[percentage_max_num_edges == 0.25],c="b",marker="o", label="Percentage max num edges 0.25")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.5],configurations_tested[percentage_max_num_edges == 0.5],c="g",marker="x", label="Percentage max num edges 0.5")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.75],configurations_tested[percentage_max_num_edges == 0.75],c="y",marker="v", label="Percentage max num edges 0.75")

    plt.legend()
    plt.title('Number of Configurations Tested for each Experiment with ' + algorithm_name)
    plt.xlabel('Vertices Number')
    plt.ylabel('Number of Configurations Tested')
    plt.savefig("graphics/configurations_tested_" + algorithm_name.replace(" ", "_") + ".png")
    plt.clf()

def basic_operations_num(data, algorithm_name):
    vertices_num = data['vertices_num']
    percentage_max_num_edges = data['percentage_max_num_edges']
    basic_operations_num = data['basic_operations_num']

    if algorithm_name == "Exhaustive Search":
        plt.plot(vertices_num[percentage_max_num_edges == 0.125],basic_operations_num[percentage_max_num_edges == 0.125],c="r",marker="+", label="Percentage max num edges 0.125")
        plt.plot(vertices_num[percentage_max_num_edges == 0.25],basic_operations_num[percentage_max_num_edges == 0.25],c="b",marker="o", label="Percentage max num edges 0.25")
        plt.plot(vertices_num[percentage_max_num_edges == 0.5],basic_operations_num[percentage_max_num_edges == 0.5],c="g",marker="x", label="Percentage max num edges 0.5")
        plt.plot(vertices_num[percentage_max_num_edges == 0.75],basic_operations_num[percentage_max_num_edges == 0.75],c="y",marker="v", label="Percentage max num edges 0.75")
    else:
        plt.scatter(vertices_num[percentage_max_num_edges == 0.125],basic_operations_num[percentage_max_num_edges == 0.125],c="r",marker="+", label="Percentage max num edges 0.125")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.25],basic_operations_num[percentage_max_num_edges == 0.25],c="b",marker="o", label="Percentage max num edges 0.25")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.5],basic_operations_num[percentage_max_num_edges == 0.5],c="g",marker="x", label="Percentage max num edges 0.5")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.75],basic_operations_num[percentage_max_num_edges == 0.75],c="y",marker="v", label="Percentage max num edges 0.75")

    plt.legend()
    plt.title('Number of Basic Operations for each Experiment with ' + algorithm_name)
    plt.xlabel('Vertices Number')
    plt.ylabel('Number of Basic Operations')
    plt.savefig("graphics/basic_operations_num_" + algorithm_name.replace(" ", "_") + ".png")
    plt.clf()


def executions_times(data, algorithm_name):
    vertices_num = data['vertices_num']
    percentage_max_num_edges = data['percentage_max_num_edges']
    execution_time = data['execution_time']

    if algorithm_name == "Exhaustive Search":
        plt.plot(vertices_num[percentage_max_num_edges == 0.125],execution_time[percentage_max_num_edges == 0.125],c="r",marker="+", label="Percentage max num edges 0.125")
        plt.plot(vertices_num[percentage_max_num_edges == 0.25],execution_time[percentage_max_num_edges == 0.25],c="b",marker="o", label="Percentage max num edges 0.25")
        plt.plot(vertices_num[percentage_max_num_edges == 0.5],execution_time[percentage_max_num_edges == 0.5],c="g",marker="x", label="Percentage max num edges 0.5")
        plt.plot(vertices_num[percentage_max_num_edges == 0.75],execution_time[percentage_max_num_edges == 0.75],c="y",marker="v", label="Percentage max num edges 0.75")
    else:
        plt.scatter(vertices_num[percentage_max_num_edges == 0.125],execution_time[percentage_max_num_edges == 0.125],c="r",marker="+", label="Percentage max num edges 0.125")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.25],execution_time[percentage_max_num_edges == 0.25],c="b",marker="o", label="Percentage max num edges 0.25")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.5],execution_time[percentage_max_num_edges == 0.5],c="g",marker="x", label="Percentage max num edges 0.5")
        plt.scatter(vertices_num[percentage_max_num_edges == 0.75],execution_time[percentage_max_num_edges == 0.75],c="y",marker="v", label="Percentage max num edges 0.75")

    plt.legend()
    plt.title('Execution Time for each Experiment with ' + algorithm_name)
    plt.xlabel('Vertices Number')
    plt.ylabel('Time (sec)')
    plt.savefig("graphics/executions_times_" + algorithm_name.replace(" ", "_") + ".png")
    plt.clf()

def main():
    exhaustive_search = pd.read_csv('results/analyze_exhaustive_search.txt', sep=" ", header=0)
    greedy = pd.read_csv('results/analyze_greedy.txt', sep=" ", header=0)
    randomized_graphs_creator = pd.read_csv('results/graphs_creator/analyze_randomized_algorithm.txt', sep=" ", header=0)

    # executions_times(exhaustive_search, "Exhaustive Search")
    # executions_times(greedy, "Greedy")
    executions_times(randomized_graphs_creator, "Randomized Algorithm Graphs Creator")

    # basic_operations_num(exhaustive_search, "Exhaustive Search")
    # basic_operations_num(greedy, "Greedy")
    basic_operations_num(randomized_graphs_creator, "Randomized Algorithm Graphs Creator")
    
    # configurations_tested(exhaustive_search, "Exhaustive Search")
    configurations_tested(randomized_graphs_creator, "Randomized Algorithm Graphs Creator")

    compare_all_solutions(exhaustive_search, greedy, randomized_graphs_creator)

    compare_greedy_randomized_solutions(greedy, randomized_graphs_creator)

if __name__ == "__main__":
    main()