import uuid

from util import get_node_id


def P1(graph, x_max_idx, y_max_idx, node_color_attributes):
    '''
    Node ids are x,y position pairs
    Hyperedge ids are uuid

    :param node_color_attributes: a collection containing 4 dictionaries, each representing corner_node and containing (R, G, B) values
    :param y_max_idx: maximum index of picture y (picture y size - 1)
    :param x_max_idx: picture x size (picture x size - 1)
    :param graph: Empty, starting graph
    :return:
    '''

    node_positions = ({'x': 0, 'y': 0},
                      {'x': 0, 'y': y_max_idx},
                      {'x': x_max_idx, 'y': 0},
                      {'x': x_max_idx, 'y': y_max_idx})

    # add common nodes
    for attributes, position in zip(node_color_attributes, node_positions):
        graph.add_node(get_node_id(position), attr_dict=attributes)

    # add edges between nodes
    graph.add_edge(get_node_id(node_positions[0]), get_node_id(node_positions[1]))
    graph.add_edge(get_node_id(node_positions[1]), get_node_id(node_positions[2]))
    graph.add_edge(get_node_id(node_positions[2]), get_node_id(node_positions[3]))
    graph.add_edge(get_node_id(node_positions[3]), get_node_id(node_positions[0]))

    # create hyperedge and connect it with four created nodes
    hyperedge_id = uuid.uuid4()
    graph.add_node(hyperedge_id, edge_break=0, hyperedge=True)

    graph.add_edge(hyperedge_id, get_node_id(node_positions[0]))
    graph.add_edge(hyperedge_id, get_node_id(node_positions[1]))
    graph.add_edge(hyperedge_id, get_node_id(node_positions[2]))
    graph.add_edge(hyperedge_id, get_node_id(node_positions[3]))
