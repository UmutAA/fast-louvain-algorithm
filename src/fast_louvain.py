from src.graph_processor import community_weight, compute_ki_in, modularity
import networkx as nx

def fast_louvain(G: nx.Graph, communities: dict) -> None:
    m2 = 2.0 * G.size(weight="weight")
    if m2 == 0:
        m2 = 1.0

    nodes_by_degree = sorted(G.nodes, key=lambda v: G.degree(v, weight="weight"), reverse=True)
    for v in nodes_by_degree:
        communities[v] = 0

    next_community = 1
    for v in nodes_by_degree:
        best_community = 0
        best_delta_q = 0.0
        ki = G.degree(v, weight="weight")

        for c in range(1, next_community):
            ki_in = compute_ki_in(G, v, c, communities)
            tot_c = community_weight(G, communities, c)
            dQ = (ki_in / m2) - ((ki * tot_c) / (m2 * m2))

            if dQ > best_delta_q:
                best_delta_q = dQ
                best_community = c

        if best_delta_q <= 0:
            communities[v] = next_community
            next_community += 1
        else:
            communities[v] = best_community
