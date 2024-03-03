import cfpq_data
import networkx as nx


def graph_from_csv(name):
    path = cfpq_data.download(name)
    return cfpq_data.graph_from_csv(path)


def graph_info(name):

    graph = graph_from_csv(name)

    info = [name, graph.number_of_nodes(), graph.number_of_edges()]

    labels = []
    for edge in graph.edges(data=True):
        # ddict under 2nd idx
        labels.append(edge[2]["label"])

    info.append(labels)
    return info


def save_graph_dot(filename, graph):
    pydot_graph = nx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write(filename)


def make_two_cycle_graph(frst_nodes: int, scnd_nodes: int, labels: tuple):
    return cfpq_data.labeled_two_cycles_graph(frst_nodes, scnd_nodes, labels=labels)


if __name__ == "__main__":
    # graph = graph_from_csv("go")
    # print(graph.number_of_edges())
    # print(graph.number_of_nodes())
    graph = make_two_cycle_graph(2, 2, ("0", "1"))
    save_graph_dot("tests/two_cycle1.dot", graph)
