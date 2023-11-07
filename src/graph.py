import numpy as np
import pandas as pd

import networkx as nx
from scipy.sparse import csr_matrix, lil_matrix


class Graph():

    def __init__(self, edges_file):
        nodes = set()
        num_edges = 0

        if edges_file.endswith(".txt"):
            with open(edges_file, "r") as f:
                for line in f:
                    a, b = map(int, line.split())
                    nodes.add(a)
                    nodes.add(b)
                    num_edges += 1
        else:
            df_edges = pd.read_csv(edges_file)

            for i, row in df_edges.iterrows():
                a, b = row["vertex1"], row["vertex2"]
                nodes.add(a)
                nodes.add(b)
                num_edges += 2

        self.node_numbers = np.array(sorted(list(nodes)))
        self.n_nodes = len(self.node_numbers)
        self.nodes = np.arange(self.n_nodes)

        self.edges = np.arange(num_edges)
        self.in_nodes = np.empty(num_edges, dtype=int)
        self.out_nodes = np.empty(num_edges, dtype=int)
        self.e_weight = np.empty(num_edges, dtype=float)

        id_dict = {self.node_numbers[i]: i for i in range(self.n_nodes)}

        tmp_matrix = lil_matrix((self.n_nodes, self.n_nodes), dtype="int")

        if edges_file.endswith(".txt"):
            with open(edges_file, "r") as f:
                for i, line in enumerate(f):
                    a, b = map(int, line.split())
                    self.in_nodes[i] = id_dict[a]
                    self.out_nodes[i] = id_dict[b]
                    self.e_weight[i] = 1.0
                    tmp_matrix[id_dict[a], id_dict[b]] += 1
        else:
            j = 0
            for i, row in df_edges.iterrows():
                a, b = row["vertex1"], row["vertex2"]
                t = row["type"]
                w = row["weight"]
                self.in_nodes[j] = id_dict[a]
                self.out_nodes[j] = id_dict[b]
                self.e_weight[j] = w
                tmp_matrix[id_dict[a], id_dict[b]] += w
                j += 1

                self.in_nodes[j] = id_dict[b]
                self.out_nodes[j] = id_dict[a]
                self.e_weight[j] = w
                tmp_matrix[id_dict[b], id_dict[a]] += w
                j += 1

        self.matrix = csr_matrix(tmp_matrix)

    def get_dest_of_nodes(self, nodes):
        edges = np.isin(self.in_nodes, nodes)
        return self.out_nodes(edges)

    def get_source_of_nodes(self, nodes):
        edges = np.isin(self.out_nodes, nodes)
        return self.in_nodes(edges)

    def get_in_nodes_by_node(self, nodes):
        nodes = np.array(nodes)

        edges = self.out_nodes.reshape(1, -1) == nodes.reshape(-1, 1)
        return edges

    def do_spread(self, nodes, prob):
        edges = np.isin(self.in_nodes, nodes)
        edges_probs = self.e_weight[edges]
        assert len(edges_probs) == edges.sum()
        rand = np.random.rand(edges.sum()) < prob*edges_probs
        candidates = self.out_nodes[edges]
        return candidates[rand]

    def to_nx(self):
        graph = nx.MultiGraph()

        for node in self.nodes:
            graph.add_node(self.node_numbers[node])

        for i, (a, b) in  enumerate(zip(self.in_nodes, self.out_nodes)):
            graph.add_edge(
                self.node_numbers[a],
                self.node_numbers[b],
                weigth = self.e_weight[i]
            )

        return graph


    def to_nx_graph(self):
        graph = nx.Graph()

        for node in self.nodes:
            graph.add_node(self.node_numbers[node])

        for i, (a, b) in enumerate(zip(self.in_nodes, self.out_nodes)):
            if graph.has_edge(a, b):
                graph.edges[a, b]["weight"] += self.e_weight[i]
            else:
                graph.add_edge(
                    self.node_numbers[a],
                    self.node_numbers[b],
                    weight = self.e_weight[i]
                )

        return graph
