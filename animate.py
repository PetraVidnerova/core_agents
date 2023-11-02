import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

from graph import Graph
from sir import S, I, R

g = Graph("data/verona/raj-social-edges.csv")
G = g.to_nx_graph()


names = pd.read_csv("data/verona/raj-social-nodes.csv")
name_dict = {}
for _, row in names.iterrows():
    if row["type"] == 0:  # Chorus, not included, add him
        G.add_node(row["type"])
    name_dict[row["type"]] = row["label"]

layout = nx.spring_layout(G, k=1)

print(name_dict)

df = (
    pd.read_csv("Verona_SIR_twitter_results_eigenvalue.csv")
    .drop(columns=["S", "I", "R", "Unnamed: 0", "beta"])
)

seed = "median"
run = 3

df = df[df["seed"] == seed]
df = df[df["run"] == run]
df = df.drop(columns=["seed", "run"])

print(df)


i = 0
for _, row in df.iterrows():

    if i >= 10:
        break
    i += 1

    s_nodes = np.where(row == I)[0]
    s_nodes = g.node_numbers[s_nodes]

    r_nodes = np.where(row == R)[0]
    r_nodes = g.node_numbers[r_nodes]

    nx.draw_networkx(G, layout, node_color='blue',
                     node_size=20, labels=name_dict, edge_color="gray")
    nx.draw_networkx(G, layout, nodelist=list(
        s_nodes), node_color="red", node_size=20, with_labels=False, edge_color="gray")
    nx.draw_networkx(G, layout, nodelist=list(
        r_nodes), node_color="orange", node_size=20, with_labels=False, edge_color="gray")

    plt.savefig(f"verona_{i:03d}.png", dpi=200)
