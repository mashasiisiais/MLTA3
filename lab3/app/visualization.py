import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(edges, pos_coords):
    G = nx.DiGraph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    plt.figure(figsize=(7, 6))
    
    # Малювання вузлів та стрілок
    nx.draw(
        G, pos_coords,
        with_labels=True,
        node_size=1400,
        node_color="lightblue",
        arrows=True,
        arrowstyle='-|>',
        arrowsize=18,
        font_size=16
    )
    
    # Малювання ваги ребер
    labels = {(u, v): w for (u, v, w) in edges}
    nx.draw_networkx_edge_labels(G, pos_coords, edge_labels=labels, font_size=12)
    
    plt.title("Орієнтований граф з вагами")
    plt.axis("off")
    plt.show()