import matplotlib.pyplot as plt
import networkx as nx

from src.io_handler import load_edge_list
from src.graph_processor import create_graph_from_df, modularity
from src.fast_louvain import fast_louvain 

def main():
    DATA_PATH = "data/karate_club.csv"
    edge_df = load_edge_list(DATA_PATH)
    G = create_graph_from_df(edge_df, source_col="source", dest_col="destination")
    community_map = dict()
    fast_louvain(G, community_map)
    q_value = modularity(G, community_map)
    node_colors = [community_map[node] for node in G.nodes()]
    pos = nx.spring_layout(G, seed=42) 
    
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=plt.cm.jet, node_size=500)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="white")
    
    plt.title("Fast Louvain Algorithm Results:")
    plt.axis("off")

    plt.figtext(
        0.5, 0.05, 
        f"Modularity (Q Value): {q_value:.4f}", 
        ha="center", 
        fontsize=12, 
        bbox={"facecolor":"orange", "alpha":0.2, "pad":5}
    )
    
    plt.show()

if __name__ == "__main__":
    main()