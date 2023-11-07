import pandas as pd
import networkx as nx
from networkx import degree_centrality, eigenvector_centrality, pagerank
from networkx.algorithms import approximation

from graph import Graph


g = Graph("data/twitter/twitter_combined.txt")
G = g.to_nx()
print(G)

nodes = G.number_of_nodes()
print(nodes)
edges = G.number_of_edges()
print(edges)
den = nx.density(G)
print(den)
con =  nx.average_node_connectivity(G)
print(con)

table = { 
    "nodes": nodes,  
    "edges": edges,
    "density":  den,
    "avg. node connectivity": con 
}

df = pd.DataFrame([table])
print(df.T)

    

# centrality = eigenvector_centrality(G)
# print(centrality)



# df = pd.DataFrame([{"name": k, "centrality": v} for k, v in centrality.items()])

# pg = pagerank(G)
# df["pagerank"] = pg.values()

# print(df)

# df.to_csv("verona.csv")
