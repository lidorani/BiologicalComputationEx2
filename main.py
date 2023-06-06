import networkx as nx
import time
import matplotlib.pyplot as plt

# input: number of vertices
# output: number of motifs
# function description: this function gets as input the number of vertices in a graph, then uses sub-functions
#                       to count the number of non-isomorphic motifs that it contains.
def count_motifs(n):
    print("****************************************************************************************************")
    print("n = ",n)

    # generate a list of all subgraphs for n vertices
    all_subgraphs_list = generate_subgraphs(n)

    # remove disconnected subgraphs
    connected_subgraphs = []
    for graph in all_subgraphs_list:
        if check_connectivity(graph, n):
            connected_subgraphs.append(graph.copy())  # Append a copy of the graph
#    for subgraph in all_subgraphs_list:
#        print(subgraph.edges())
    print("Number of connected graphs:", len(connected_subgraphs))

    # get non-isomorphic subgraphs
    non_isomorphic_subgraphs = get_non_isomorphic_subgraphs(connected_subgraphs)
#    for subgraph in non_isomorphic_subgraphs:
#        print(subgraph.edges())
    print("Number of unique patterns of subgraphs:", len(non_isomorphic_subgraphs))

    write_to_file(n, non_isomorphic_subgraphs)

    return len(non_isomorphic_subgraphs)


# input: number of vertices
# output: list of all sub-graphs for input
def generate_subgraphs(n):
    # create a connected directed graph with n nodes
    graph = nx.complete_graph(n, create_using=nx.DiGraph())
    if n == 1:
        graph.add_edge(0,0)

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
# function description: this function gets a directed graph, checks if it has all vertices, and check connectivity.
def check_connectivity(graph, n):
    if graph.nodes.__len__() < n:
        return False
    undirected_graph = graph.to_undirected()
    return nx.is_connected(undirected_graph)


#function description: this function outputs a list of unique patterns of graphs in given graphs list.
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

def write_to_file(n, non_isomorphic_subgraphs):
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


def plot_graph(time_compare):
    n_values = range(1, len(time_compare) + 1)
    plt.plot(n_values, time_compare, marker='o')
    plt.xlabel('n')
    plt.ylabel('Time (seconds)')
    plt.title('Comparison of Running Time')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    time_compare = []

    for n in range(1,6):        # run from 1 to 4
        # measuring time
        start_time = time.time()

        num = count_motifs(n)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: {:.2f} seconds".format(elapsed_time))
        time_compare.append(elapsed_time)

    print("****************************************************************************************************")

    plot_graph(time_compare)
