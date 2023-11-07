import pandas as pd
import networkx as nx
from networkx import degree_centrality, eigenvector_centrality, pagerank
from networkx.algorithms import approximation

from graph import Graph


g = Graph("data/verona/raj-social-edges.csv")
G = g.to_nx()
print(G)



names = pd.read_csv("data/verona/raj-social-nodes.csv")
name_dict = {}
for _, row in names.iterrows():
    if row["type"] == 0:  # Chorus, not included, add him
        G.add_node(row["type"])
    name_dict[row["type"]] = row["label"]

table = {
    "nodes": G.number_of_nodes(),
    "edges": G.number_of_edges(),
    "density": nx.density(G),
    "avg. node connectivity": nx.average_node_connectivity(G),
}

df = pd.DataFrame([table])
print(df.T)

    
G = g.to_nx_graph()
centrality = eigenvector_centrality(G)
print(centrality)

centrality = {
    name_dict[k]: v
    for k, v in centrality.items()
}


df = pd.DataFrame([{"name": k, "centrality": v} for k, v in centrality.items()])

pg = pagerank(G)
df["pagerank"] = pg.values()

print(df)

df.to_csv("verona.csv")
