import uuid
from enum import Enum

import networkx as nx
from PIL.Image import Image

from utils import get_node_id

# hyp_b - B labeled hyperedge id
# hyp_is - I labeled hyperedge_ids
# hyp_f1 - F1 labeled hyperedge_id
def P3(graph: nx.Graph, hyp_b, hyp_is, hyp_f1, image: Image):
    __assert_hyper_edge(graph, hyp_b, 'B')
    for hyp_i in hyp_is:
        __assert_hyper_edge(graph, hyp_i, 'I')
    __assert_hyper_edge(graph, hyp_f1, 'Direction.N')

    hyperedge_data = graph.node[hyp_b]
    new_node_position = (hyperedge_data['x'], hyperedge_data['y'])
    new_node_id = get_node_id(new_node_position)

    __add_new_node(graph, image, new_node_id, new_node_position) # add v
    __add_hyperedges_between_neighbour_nodes(graph, hyp_b, new_node_id, new_node_position) # add 1-b-v-b-2
    for hyp_i in hyp_is:
        __add_edges_between_nodes(graph, new_node_id, hyp_i) # add v-i and v-i
    __add_edges_between_nodes(graph, new_node_id, hyp_f1) # add v-f1
    graph.remove_node(hyp_b)


def __assert_hyper_edge(graph, hyperedge_ids, label):
    for hyperedge_id in hyperedge_ids:
        if not graph.node[hyperedge_id]['is_hyperedge']:
            raise ValueError('Given node_id is not id of hyperedge')
        if not graph.node[hyperedge_id]['label'] is label:
            raise ValueError(f"Given node_id is not hyperedge type '{label}'")


def __add_new_node(graph, image, new_node_id, new_node_position):
    new_node_rgb = image.getpixel(new_node_position)
    graph.add_node(
        new_node_id,
        x=new_node_position[0],
        y=new_node_position[1],
        is_hyperedge=False,
        r=new_node_rgb[0],
        g=new_node_rgb[1],
        b=new_node_rgb[2],
    )


def __add_hyperedges_between_neighbour_nodes(graph, hyperedge_id, new_node_id, new_node_position):
    hyperedge_neighbour_ids = graph.neighbors(hyperedge_id)
    for neighbour_id in hyperedge_neighbour_ids:
        neighbour = graph.node[neighbour_id]
        new_hyperedge_id = uuid.uuid4()
        graph.add_node(
            new_hyperedge_id,
            x=(neighbour['x'] + new_node_position[0]) // 2,
            y=(neighbour['y'] + new_node_position[1]) // 2,
            is_hyperedge=True,
            label='B',
        )
        graph.add_edge(new_hyperedge_id, neighbour_id)
        graph.add_edge(new_hyperedge_id, new_node_id)


def __add_edges_between_nodes(graph, node1, node2):
    graph.add_edge(node1, node2)
