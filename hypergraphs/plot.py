import random

import networkx as nx

from hypergraphs.utils import convert_to_hex
from matplotlib import pyplot as plt


def plot(graph: nx.Graph):
    plot_but_dont_show(graph)
    plt.show()


def plot_but_dont_show(graph: nx.Graph):
    labels = {}
    colors = []
    positions = {}
    shapes = {}
    for node_id, node_data in graph.nodes(data=True):
        positions[node_id] = node_data['x'], node_data['y']

        if 'r' in node_data:
            colors.append(convert_to_hex(
                (node_data['r'], node_data['g'], node_data['b'], 0)))
        else:
            colors.append(convert_to_hex((255, 255, 255, 0)))
        if node_data['is_hyperedge']:
            labels[node_id] = "{}".format(node_data['label'])
        else:
            labels[node_id] = ''

        if 'should_break' in node_data:
            labels[node_id] += "; break = {}".format(node_data['should_break'])

        shapes[node_id] = random.choice(['x', 'o'])

    nx.draw_networkx(
        graph,
        pos=positions,
        labels=labels,
        node_color=colors,
    )
    plt.axis('off')
