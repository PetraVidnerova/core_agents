from networkx import degree_centrality, eigenvector_centrality
import pandas as pd
from tqdm import tqdm

from graph import Graph
from sir import SIR, S, I
from tipping import TippingModel

BETA = 0.1
#MODEL = "TippingModel"
#BETAS = [0.1, 0.05, 0.01]

MODEL = "SIR"
#BETAS = [0.1, 0.2, 0.3]
BETAS = [0.01, 0.05, 0.1, 0.5]

TASK = "Twitter"

METRIC = "eigenvector"


def run(g, seed, beta=BETA):

    if MODEL == "SIR":
        model = SIR(beta)
    elif MODEL == "TippingModel":
        model = TippingModel(beta)
    else:
        raise NotImplementedError

    model.set_graph(g)
    model.setup(S)
    seed = g.node_numbers == seed
    model.node_states[seed] = I
    model.history.update()

    iters = 150
    for i in range(iters):
        model.iterate()

    df = model.history_to_df(include_node_states=(TASK == "Verona"))
    return df


def main():

    print("Creating graph .... ", end="", flush=True)
    if TASK == "Twitter":
        g = Graph("data/twitter/twitter_combined.txt")
    elif TASK == "Verona":
        g = Graph("data/verona/raj-social-edges.csv")

    print("ok", flush=True)
    print("Nodes:", g.n_nodes)
    print("Edges:", g.edges.size)

    G = g.to_nx_graph()

    print(G)

    if METRIC == "eigenvector":
        centrality = eigenvector_centrality(G)
    else:
        raise NotImplementedError
    # print(centrality)
    # exit()
    nodes, values = centrality.keys(), centrality.values()
    centrality = list(zip(nodes, values))
    centrality.sort(key=lambda x: x[1])

    print(centrality[0])
    print(centrality[len(centrality)//2])
    print(centrality[-1])

    lowest = centrality[0][0]
    median = centrality[len(centrality)//2][0]
    highest = centrality[-1][0]

    dfs = []

    for name, number in ("lowest", lowest), ("median", median), ("highest", highest):
        for beta in BETAS:
            print(f"Computing {name}.")
            if MODEL == "SIR":
                repeat = 100
            else:
                repeat = 1
            for i in tqdm(range(repeat)):
                df = run(g, number, beta)
                df["run"] = i
                df["beta"] = beta
                df["seed"] = name
                dfs.append(df)

    df_result = pd.concat(dfs)
    df_result.to_csv(f"{TASK}_{MODEL}_results_{METRIC}.csv")


if __name__ == "__main__":
    main()
