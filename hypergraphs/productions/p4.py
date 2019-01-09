import networkx as nx
from PIL.Image import Image

import uuid

from utils import get_node_id, Direction


def P4(graph: nx.Graph, central_hyperedge, image: Image):
    assert central_hyperedge in graph.node
    central_hyperedge_params = graph.node[central_hyperedge]

    assert central_hyperedge_params['is_hyperedge']

    assert central_hyperedge_params['label'] in ['N', 'S', 'W', 'E']

    central_neighbours = graph[central_hyperedge]
    assert len(central_neighbours) == 2
    first_neighbour, second_neighbour = central_neighbours
    first_neighbour_params, second_neighbour_params = graph.node[
        first_neighbour], graph.node[second_neighbour]

    new_node_pos = {
        "x": (first_neighbour_params["x"] + second_neighbour_params["x"])//2,
        "y": (first_neighbour_params["y"] + second_neighbour_params["y"])//2
    }
    new_node_pos_tuple = (new_node_pos["x"], new_node_pos["y"])
    new_node_id = get_node_id(new_node_pos_tuple)
    graph.add_node(
        new_node_id,
        is_hyperedge=False,
        **new_node_pos,
        **pixel_to_rgb_dict(image.getpixel(new_node_pos_tuple))
    )

    same_x_pos = len(set(
        [new_node_pos["x"], first_neighbour_params["x"], second_neighbour_params["x"]])) == 1
    same_y_pos = len(set(
        [new_node_pos["y"], first_neighbour_params["y"], second_neighbour_params["y"]])) == 1

    assert same_x_pos or same_y_pos

    for n, n_params in zip([first_neighbour, second_neighbour], [first_neighbour_params, second_neighbour_params]):
        new_neighbour_pos = {
            "x": (n_params["x"] + new_node_pos["x"])/2,
            "y": (n_params["y"] + new_node_pos["y"])/2,
        }
        new_neighbour_pos_tuple = (
            new_neighbour_pos["x"], new_neighbour_pos["y"])

        def neighbour_label():
            if same_x_pos:
                return "S" if new_neighbour_pos["y"] < new_node_pos["y"] else "N"
            else:
                return "W" if new_neighbour_pos["x"] < new_node_pos["x"] else "E"

        n_new_id = get_node_id(new_neighbour_pos_tuple)
        graph.add_node(
            n_new_id,
            is_hyperedge=True,
            **new_neighbour_pos,
            label=neighbour_label()
        )
        graph.add_edge(n_new_id, n)
        graph.add_edge(n_new_id, new_node_id)

    graph.remove_node(central_hyperedge)

    for n, n_params in zip([first_neighbour, second_neighbour], [first_neighbour_params, second_neighbour_params]):
        I = [
            i
            for i in graph[n]
            if graph.node[i].get("label", None) == "I" and
            len([
                z for z in graph[i] if graph.node[z]
                ["is_hyperedge"] == False and (
                    graph.node[z]["y"] == new_node_pos["y"] if same_x_pos else graph.node[z]["x"] == new_node_pos["x"]
                )
            ]) > 0
        ]
        assert len(I) == 2
        for i in I:
            Q = [
                q
                for q in graph[i]
                if graph.node[q]["is_hyperedge"] == False and (
                    graph.node[q]["y"] == new_node_pos["y"] if same_x_pos else graph.node[q]["x"] == new_node_pos["x"])
            ]
            assert len(Q) == 1
            q = Q[0]

            def prefered_direction(q):
                if same_x_pos:
                    return "E" if graph.node[q]["x"] < new_node_pos["x"] else "W"
                else:
                    return "S" if graph.node[q]["y"] < new_node_pos["y"] else "N"

            H = [
                h
                for h in graph[q]
                if graph.node[h]["is_hyperedge"] == True and prefered_direction(q) == graph.node[h]["label"]
            ]
            assert len(H) == 1
            graph.add_edge(H[0], new_node_id)

            graph.add_edge(i, new_node_id)


def from_I_to_closest_F2(I_id, graph: nx.Graph, is_top_I: bool):
    I_neighbors = graph[I_id]
    assert len(I_neighbors) == 3

    sign = 1 if is_top_I else -1
    node_id = sorted(I_neighbors, key=lambda n: sign * graph.node[n]["y"])[0]
    return [n for n in graph[node_id] if graph.node[n]["label"] == "F2"][0]


def pixel_to_rgb_dict(pixel):
    return {"r": pixel[0], "g": pixel[1], "b": pixel[2]}
