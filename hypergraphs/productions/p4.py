import networkx as nx
from PIL.Image import Image

import uuid

from utils import HyperEdge, get_node_id


def P4(graph: nx.Graph, f1_hyperedge_id, image: Image):
    assert f1_hyperedge_id in graph.node
    input_f1 = graph.node[f1_hyperedge_id]

    assert input_f1['is_hyperedge']
    assert input_f1['label'] == HyperEdge.F1.name

    top_and_bottom = graph[f1_hyperedge_id]
    assert len(top_and_bottom) == 2
    top_id, bottom_id = top_and_bottom

    # Top left and top right I
    tl_I_and_tr_I = [i for i in graph[top_id] if i != f1_hyperedge_id]
    assert len(tl_I_and_tr_I) == 2
    assert all([n for n in tl_I_and_tr_I if graph.node[n]
                ["label"] == HyperEdge.I.name])
    tl_I_id, tr_I_id = sorted(tl_I_and_tr_I, key=lambda x: graph.node[x]["x"])

    # Bottom left and bottom right I
    bl_I_and_br_I = [i for i in graph[bottom_id] if i != f1_hyperedge_id]
    assert len(tl_I_and_tr_I) == 2
    assert all([n for n in bl_I_and_br_I if graph.node[n]
                ["label"] == HyperEdge.I.name])
    bl_I_id, br_I_id = sorted(bl_I_and_br_I, key=lambda x: graph.node[x]["x"])

    left_F2_id = from_I_to_closest_F2(tl_I_id, graph, is_top_I=True)
    right_F2_id = from_I_to_closest_F2(tr_I_id, graph, is_top_I=True)

    # Try from bottom I, not necessary, only to ensure that input graph is ok
    assert left_F2_id == from_I_to_closest_F2(bl_I_id, graph, is_top_I=False)
    assert right_F2_id == from_I_to_closest_F2(br_I_id, graph, is_top_I=False)

    # Graph mutation starts below

    # Add new node in F1 place
    new_node_pos = (input_f1["x"], input_f1["y"])
    new_node_id = get_node_id(new_node_pos)
    graph.add_node(
        new_node_id,
        is_hyperedge=False,
        **pos_to_xy_dict(new_node_pos),
        **pixel_to_rgb_dict(image.getpixel(new_node_pos))
    )

    # New F1 nodes
    half_distance = (new_node_pos[1] - graph.node[top_id]["y"])//2

    new_top_f1_id = uuid.uuid4()
    new_top_f1_pos = (new_node_pos[0], new_node_pos[1] - half_distance)
    graph.add_node(
        new_top_f1_id,
        is_hyperedge=True,
        **pos_to_xy_dict(new_top_f1_pos),
        label=HyperEdge.F1.name
    )

    new_bottom_f1_id = uuid.uuid4()
    new_bottom_f1_pos = (new_node_pos[0], new_node_pos[1] + half_distance)
    graph.add_node(
        new_bottom_f1_id,
        is_hyperedge=True,
        **pos_to_xy_dict(new_bottom_f1_pos),
        label=HyperEdge.F1.name
    )

    # New node to new hyperedges
    graph.add_edge(new_node_id, new_top_f1_id)
    graph.add_edge(new_node_id, new_bottom_f1_id)

    graph.add_edge(new_top_f1_id, top_id)
    graph.add_edge(new_bottom_f1_id, bottom_id)

    # New node -> I
    graph.add_edge(new_node_id, tl_I_id)
    graph.add_edge(new_node_id, tr_I_id)
    graph.add_edge(new_node_id, bl_I_id)
    graph.add_edge(new_node_id, br_I_id)

    # New node -> F2

    graph.add_edge(new_node_id, left_F2_id)
    graph.add_edge(new_node_id, right_F2_id)

    # Remove center F1
    graph.remove_node(f1_hyperedge_id)


def from_I_to_closest_F2(I_id, graph: nx.Graph, is_top_I: bool):
    I_neighbors = graph[I_id]
    assert len(I_neighbors) == 3

    sign = 1 if is_top_I else -1
    node_id = sorted(I_neighbors, key=lambda n: sign * graph.node[n]["y"])[0]
    return [n for n in graph[node_id] if graph.node[n]["label"] == HyperEdge.F2.name][0]


def pos_to_xy_dict(pos):
    return {"x": pos[0], "y": pos[1]}


def pixel_to_rgb_dict(pixel):
    return {"r": pixel[0], "g": pixel[1], "b": pixel[2]}
