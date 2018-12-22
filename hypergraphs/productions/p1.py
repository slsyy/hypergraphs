import uuid

import networkx as nx
from PIL.Image import Image

from utils import get_node_id


def P1(graph: nx.Graph, x_max_idx: int, y_max_idx: int, image: Image):
    """
    Node ids are x,y position pairs
    Hyperedge ids are uuid

    :param graph: an empty nx.Graph object
    :param y_max_idx: maximum index of picture y (picture y size - 1)
    :param x_max_idx: picture x size (picture x size - 1)
    :return: None
    """

    node_positions = (
        (0, 0),
        (0, y_max_idx),
        (x_max_idx, y_max_idx),
        (x_max_idx, 0),
    )

    # add common nodes
    for node_position in node_positions:
        rgb = image.getpixel((node_position))
        graph.add_node(
            get_node_id(node_position),
            x=node_position[0],
            y=node_position[1],
            is_hyperedge=False,
            r=rgb[0],
            g=rgb[1],
            b=rgb[2],
        )

    hyper_node_positions = (
        (0, y_max_idx // 2),
        (x_max_idx // 2, y_max_idx),
        (x_max_idx, y_max_idx // 2),
        (x_max_idx // 2, 0)
    )

    hyper_node_connections = (
        ((0, 0), (0, y_max_idx)),
        ((0, y_max_idx), (x_max_idx, y_max_idx)),
        ((x_max_idx, y_max_idx), (x_max_idx, 0)),
        ((x_max_idx, 0), (0, 0))
    )
    # add hyper nodes
    for hyper_node_position, hyper_node_connection in zip(hyper_node_positions, hyper_node_connections):
        hyper_node_id = uuid.uuid4()
        graph.add_node(
            hyper_node_id,
            x=hyper_node_position[0],
            y=hyper_node_position[1],
            is_hyperedge=True,
            label='B',
        )

        for connection in hyper_node_connection:
            graph.add_edge(hyper_node_id, get_node_id(connection))

    # create the hyperedge and connect it with four created nodes
    hyperedge_id = uuid.uuid4()
    hyperedge_position = x_max_idx // 2, y_max_idx // 2
    graph.add_node(
        hyperedge_id,
        x=hyperedge_position[0],
        y=hyperedge_position[1],
        is_hyperedge=True,
        label='I',
        should_break=0,
    )

    for node_position in node_positions:
        graph.add_edge(hyperedge_id, get_node_id(node_position))
