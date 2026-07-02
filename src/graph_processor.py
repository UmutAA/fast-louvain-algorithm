import networkx as nx

def create_graph_from_df(df, source_col="source", dest_col="destination"):
    if "weight" in df.columns:
        G = nx.from_pandas_edgelist(df, source=source_col, target=dest_col, edge_attr="weight")
    else:
        G = nx.from_pandas_edgelist(df, source=source_col, target=dest_col)
        nx.set_edge_attributes(G, 1, "weight")
    return G

def compute_ki_in(G: nx.Graph, i: int, target_com: int, communities: dict) -> float:
    return sum(
        data.get("weight", 1)
        for _, u, data in G.edges(i, data=True)
        if communities.get(u) == target_com
    )


def community_weight(G: nx.Graph, communities: dict, target_com: int) -> float:
    return sum(
        G.degree(v, weight="weight")
        for v in G.nodes
        if communities.get(v) == target_com
    )

def modularity(G: nx.Graph, communities: dict) -> float:
    m = G.size(weight="weight")
    if m == 0:
        return 0.0

    Q = 0.0
    for i in G.nodes:
        for j in G.nodes:
            if communities.get(i) == communities.get(j):
                a_ij = G[i][j].get("weight", 1) if G.has_edge(i, j) else 0
                Q += a_ij - (G.degree(i, weight="weight") * G.degree(j, weight="weight")) / (2.0 * m)

    return Q / (2.0 * m)