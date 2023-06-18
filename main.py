import networkx as nx
import time
import matplotlib.pyplot as plt


# input: number of vertices, list of all subgraphs
# output: list of motifs
# function description: this function gets as input the number of vertices in a graph, then uses sub-functions
#                       to remove isomorphic motifs and at last has a list of unique motifs in graph.
def get_motifs_part_a(n, all_subgraphs_list):
    # remove disconnected subgraphs
    connected_subgraphs = []
    for graph in all_subgraphs_list:
        if check_connectivity(graph, n):
            connected_subgraphs.append(graph.copy())  # Append a copy of the graph
    print("Number of connected graphs:", len(connected_subgraphs))

    # get non-isomorphic subgraphs
    non_isomorphic_subgraphs = get_non_isomorphic_subgraphs(connected_subgraphs)
    print("Number of unique patterns of subgraphs:", len(non_isomorphic_subgraphs))

    write_to_file_part_a(n, non_isomorphic_subgraphs)

    return non_isomorphic_subgraphs


# input: number of vertices, directed graph
# output: list of all sub-graphs
def generate_subgraphs(n, graph):
    if n == 1:
        graph.add_edge(0,0)

    # Relabel the nodes
    if get_lowest_vertex(graph.edges) == 0:
        mapping = {node: node + 1 for node in graph.nodes()}
        graph = nx.relabel_nodes(graph, mapping)

    # generate a list of all edges
    all_edges_list = list(graph.edges())
#    print("List of all edges:", all_edges_list)

    # create all subgraphs using edges list (there are 2^n - 1)
    all_subgraphs = []
    for i in range(1, 2 ** len(all_edges_list)):
        subgraph_edges = [all_edges_list[j] for j in range(len(all_edges_list)) if (i & (1 << j)) != 0]
        subgraph = nx.DiGraph(subgraph_edges)
        all_subgraphs.append(subgraph)
    print("Number of subgraphs:", len(all_subgraphs))
    return all_subgraphs


# input: directed graph
# output: boolean
# function description: this function gets a directed graph, checks if it has "n" vertices & check connectivity.
def check_connectivity(graph, n):
    if graph.nodes.__len__() < n:
        return False
    undirected_graph = graph.to_undirected()
    return nx.is_connected(undirected_graph)


# function description: this function gets a list of subgraphs, and outputs a list of *unique patterns of graphs
#                       for this given graphs list.
def get_non_isomorphic_subgraphs(subgraphs):
    non_isomorphic_subgraphs = []
    for graph in subgraphs:
        is_isomorphic = False
        for existing_graph in non_isomorphic_subgraphs:
            if nx.is_isomorphic(graph, existing_graph):
                is_isomorphic = True
                break
        if not is_isomorphic:
            non_isomorphic_subgraphs.append(graph)

    return non_isomorphic_subgraphs


# function description: this function outputs the results of part a to a text files.
def write_to_file_part_a(n, non_isomorphic_subgraphs):
    # Create a file to write the data
    filename = f"motifs_{n}.txt"
    with open(filename, 'w') as file:
        # Write n and the total number of motifs to the file
        file.write(f"n={n}\n")
        file.write(f"count={len(non_isomorphic_subgraphs)}\n")

        # Write each subgraph to the file
        for i, subgraph in enumerate(non_isomorphic_subgraphs, start=1):
            file.write(f"#{i}\n")
            for edge in subgraph.edges():
                file.write(f"{edge[0]} {edge[1]}\n")


# function description: this function plots running time as a function of n.
def plot_graph(time_compare):
    n_values = range(1, len(time_compare) + 1)
    plt.plot(n_values, time_compare, marker='o')
    plt.xlabel('n')
    plt.ylabel('Time (seconds)')
    plt.title('Comparison of Running Time')
    plt.grid(True)
    plt.show()


def part_a():
    time_compare = []

    for n in range(1, 5):  # run from 1 to 4
        # measuring time
        start_time = time.time()

        print("************************************************************************************")
        print("n = ", n)

        # create a full connected directed graph with n nodes
        graph = nx.complete_graph(n, create_using=nx.DiGraph())

        # generate a list of all subgraphs for n vertices
        all_subgraphs_list = generate_subgraphs(n, graph)

        # count motifs for given group of subgraphs
        num = len(get_motifs_part_a(n, all_subgraphs_list))

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: {:.2f} seconds".format(elapsed_time))
        time_compare.append(elapsed_time)

    print("************************************************************************************")
    plot_graph(time_compare)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         functions for part 2                      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# function description: this function reads data from input file and parses it into variables.
def get_input(name):
    # open file and read it's content
    with open("input.txt", "r") as file:
        lines = file.readlines()

    # transfer input data into variables
    n = int(lines[0].split("=")[1].strip())
    edges = []
    for line in lines[1:]:
        edge = tuple(map(int, line.strip().split()))
        edges.append(edge)

    return n, edges


# function description: this function gets the highest value of vertex in graph.
#                       it was created in order to know the size of input graph.
def get_highest_vertex(edges):
    highest_vertex = max(max(edge) for edge in edges)
    return highest_vertex


# function description: this function gets the lowest value of vertex in graph.
#                       if it's 0, we know we need to relabel the vertices.
def get_lowest_vertex(edges):
    lowest_vertex = min(min(edge) for edge in edges)
    return lowest_vertex


# function description: this function gets a list of edges and a number of vertices & returns a graph.
def create_graph_from_edges(num, edges):
    graph = nx.DiGraph()
    graph.add_nodes_from(range(1, num + 1))
    graph.add_edges_from(edges)
    return graph


# input: number of vertices, list of all subgraphs
# output: number of motifs
# function description: this function gets as input the number of vertices in a graph, then uses sub-functions
#                       to count the number of of appearances of motifs for input graph.
def get_motifs_list_part_b(n, all_subgraphs_list):
    # remove disconnected subgraphs
    connected_subgraphs = []
    for graph in all_subgraphs_list:
        if check_connectivity(graph, n):
            connected_subgraphs.append(graph.copy())  # Append a copy of the graph

    # get non-isomorphic subgraphs
    non_isomorphic_subgraphs = get_non_isomorphic_subgraphs(connected_subgraphs)
    return non_isomorphic_subgraphs


# function description: this function gets a list of motifs & a list of subgraphs, then it counts how many appearances
#                       of each motifs there are in subgraphs list.
def count_num_of_motifs(motifs_list, subgraphs_list):
    graph_counts = {}

    for motif in motifs_list:
        count = 0
        for subgraph in subgraphs_list:
            if nx.is_isomorphic(motif, subgraph):
                count += 1

        graph_counts[motif] = count

    return graph_counts


# function description: this function outputs the results of part b to a text file.
def write_to_file_part_b(n, graphs_list, num_of_appearances, filename):
    # Create a file to write the data
    with open(filename, 'w') as file:
        # Write n and the total number of motifs to the file
        file.write(f"n={n}\n")
        file.write(f"number of motifs={len(graphs_list)}\n\n")

        # Write each subgraph to the file
        for i, subgraph in enumerate(graphs_list, start=1):
            file.write(f"#{i}\n")
            for edge in subgraph.edges():
                file.write(f"{edge[0]} {edge[1]}\n")

            # Write the count of appearances for the current subgraph
            count = num_of_appearances.get(subgraph, 0)
            file.write(f"count={count}\n\n")


def part_b():
    # read input from text file and create a graph
    [n, edges] = get_input("input.txt")
    print("n =", n)
    print("edges =", edges)

    # generate a list of motifs for given "n" value
    graph = nx.complete_graph(n, create_using=nx.DiGraph())
    motifs_list_for_n = get_motifs_part_a(n, generate_subgraphs(n, graph))

    # create all subgraphs for input graph
    vertices_number = get_highest_vertex(edges)
    print("max vertex for input graph is ", vertices_number)
    input_graph = create_graph_from_edges(vertices_number, edges)
    subgraphs_of_input_graph = generate_subgraphs(n, input_graph)

    # count how many appearances each motif has on motifs group, by checking isomorphism
    appearances_list = count_num_of_motifs(motifs_list_for_n, subgraphs_of_input_graph)

    # output results to file "output.txt"
    write_to_file_part_b(n, motifs_list_for_n, appearances_list, "output.txt")

    return


if __name__ == '__main__':
    # part_a()
    part_b()
