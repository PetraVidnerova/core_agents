from networkx import degree_centrality, eigenvector_centrality
import pandas as pd
from tqdm import tqdm

from graph import Graph
from sir import SIR, S, I

BETA = 0.1

def run(g, seed, beta=BETA):
    
    model = SIR(beta)
    model.set_graph(g)
    model.setup(S)
    seed = g.node_numbers == seed
    model.node_states[seed] = I

    iters = 150
    for i in range(iters):
        model.iterate()

    df = model.history_to_df()
    return df
    

def main():
    print("Creating graph .... ", end="", flush=True)
    g = Graph("data/twitter/twitter_combined.txt")
    print("ok", flush=True)
    print("Nodes:", g.n_nodes)
    print("Edges:", g.edges.size)    


    G = g.to_nx_graph()

    print(G)

    centrality = eigenvector_centrality(G)
    # print(centrality)
    # exit()    
    nodes, values = centrality.keys(), centrality.values()
    centrality = list(zip(nodes, values))
    centrality.sort(key=lambda x: x[1])

    print(centrality[0])
    print(centrality[-1])

    lowest = centrality[0][0]
    median = centrality[len(centrality)//2][0]
    highest = centrality[-1][0]
    
    dfs = [] 

    for name, number in ("lowest", lowest), ("median", median), ("highest", highest):
        for beta in 0.1, 0.2, 0.3:
            print(f"Computing {name}.")
            repeat = 100
            for i in tqdm(range(repeat)):
                df = run(g, number,beta)
                df["run"] = i
                df["beta"] = beta
                df["seed"] = name
                dfs.append(df)

    df_result = pd.concat(dfs)
    df_result.to_csv(f"twitter_results_eigenvalue.csv")
        

    
if __name__ == "__main__":
    main()
