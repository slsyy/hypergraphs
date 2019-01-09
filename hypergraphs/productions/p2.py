import uuid

import networkx as nx
from PIL.Image import Image

from hypergraphs.utils import get_node_id, Direction


def create_direction_calulcator(depth):
    offset = 100 / (2**depth)
    return {
        Direction.N: (lambda x: x, lambda x: x + offset),
        Direction.S: (lambda x: x, lambda x: x - offset),
        Direction.W: (lambda x: x - offset, lambda x: x),
        Direction.E: (lambda x: x + offset, lambda x: x),
    }


def P2(graph: nx.Graph, hyperedge_id, image: Image):
    __assert_hyper_edge(graph, hyperedge_id)
    hyperedge_data = graph.node[hyperedge_id]
    new_node_position = (hyperedge_data['x'], hyperedge_data['y'])
    new_node_id = get_node_id(new_node_position)
    old_depth = hyperedge_data.get("depth", 0)
    new_depth = old_depth + 1

    __add_new_node(graph, image, new_node_id, new_node_position)
    __add_hypereges_between_nodes(
        graph, hyperedge_id, new_node_id, new_node_position, new_depth)
    __add_direction_hyperedges(
        graph, new_node_id, create_direction_calulcator(old_depth))
    graph.remove_node(hyperedge_id)


def __assert_hyper_edge(graph, hyperedge_id):
    if not graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of hyperedge')
    elif graph.node[hyperedge_id]['should_break'] is 0:
        raise ValueError(
            'Hyper edge has should_break set to 0, when it is supposed to be equal 1')


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


def __add_hypereges_between_nodes(graph, hyperedge_id, new_node_id, new_node_position, new_depth):
    hyperedge_neighbour_ids = graph.neighbors(hyperedge_id)
    for neighbour_id in hyperedge_neighbour_ids:
        neighbour = graph.node[neighbour_id]
        new_hyperedge_id = uuid.uuid4()
        graph.add_node(
            new_hyperedge_id,
            x=(neighbour['x'] + new_node_position[0]) // 2,
            y=(neighbour['y'] + new_node_position[1]) // 2,
            is_hyperedge=True,
            label='I',
            should_break=0,
            depth=new_depth
        )
        graph.add_edge(new_hyperedge_id, neighbour_id)
        graph.add_edge(new_hyperedge_id, new_node_id)


def __add_direction_hyperedges(graph, neighbour_id, direction_calulcators):
    for direction in Direction:
        hyperedge_id = uuid.uuid4()
        graph.add_node(
            hyperedge_id,
            label=direction.name,
            is_hyperedge=True,
            x=direction_calulcators[direction][0](
                graph.node[neighbour_id]['x']),
            y=direction_calulcators[direction][1](
                graph.node[neighbour_id]['y'])
        )
        graph.add_edge(hyperedge_id, neighbour_id)
