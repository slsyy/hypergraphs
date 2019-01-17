import os
import uuid
from unittest import TestCase

from matplotlib import pyplot as plt
import networkx as nx
from PIL import Image
from frozendict import frozendict

from productions import P1
from productions import P2
from productions import P3
from productions import P4
from productions import P5

from utils import HyperEdge, IMAGE_PATH, Direction

from plot import plot_but_dont_show, plot
from utils import *


IMAGE_PATH = os.path.join(os.path.dirname(
    __file__), "test_data", "four_colors.jpg")

B_DIRECTION_EDGE_LAMBDAS = {
    Direction.N: lambda data, f_data: f_data['x'] == data['x'] and f_data['y'] < data['y'],
    Direction.S: lambda data, f_data: f_data['x'] == data['x'] and f_data['y'] > data['y'],
    Direction.E: lambda data, f_data: f_data['x'] < data['x'] and f_data['y'] == data['y'],
    Direction.W: lambda data, f_data: f_data['x'] > data['x'] and f_data['y'] == data['y'],
}


class TestP4(TestCase):
    def test_run_productions_and_draw_plot(self):
        graph_before = self.graph.copy()
        P4(self.graph, self.N, self.image)
        P4(self.graph, self.W, self.image)
        graph_after = self.graph

        plt.subplot(121)
        plt.title("Before")
        plot_but_dont_show(graph_before)

        plt.subplot(122)
        plt.title("After")
        plot_but_dont_show(graph_after)
        plt.show()

    def test_check_output(self):
        graph_before = self.graph.copy()
        P4(self.graph, self.N, self.image)
        P4(self.graph, self.W, self.image)
        graph_after = self.graph

        def nodes(g):
            return set([(k, frozendict(v)) for k, v in g.nodes(data=True)])

        def id_by_data(g, data):
            for k, v in g.nodes(data=True):
                if frozendict(v) == frozendict(data):
                    return k

        def hyperedge_by_2_nodes(g, first, second, label):
            for k, v in g.nodes(data=True):
                if v["is_hyperedge"] == True and v.get("label", None) == label:
                    if first in g[k] and second in g[k]:
                        return k

        expected_removed_nodes = [
            (k, frozendict(graph_before.node[k])) for k in [self.N, self.W]]
        removed_nodes = nodes(graph_before).difference(nodes(graph_after))
        self.assertEqual(set(expected_removed_nodes), set(removed_nodes))

        new_nodes = nodes(graph_after).difference(nodes(graph_before))
        new_nodes_data = [x[1] for x in new_nodes]

        N_new_node_data = {'is_hyperedge': False,
                           'x': 199, 'y': 299, 'r': 255, 'g': 185, 'b': 1}
        N_new_node_id = id_by_data(graph_after, N_new_node_data)
        self.assertIn(N_new_node_data, new_nodes_data)

        N_left = get_node_id((99, 299))
        N_top = get_node_id((199, 399))
        N_right = get_node_id((299, 299))
        N_bottom = get_node_id((199, 199))

        I = [
            hyperedge_by_2_nodes(graph_after, N_left, N_top, "I"),
            hyperedge_by_2_nodes(graph_after, N_top, N_right, "I"),
            hyperedge_by_2_nodes(graph_after, N_right, N_bottom, "I"),
            hyperedge_by_2_nodes(graph_after, N_bottom, N_left, "I")
        ]

        direction_hyperedges = [
            hyperedge_by_2_nodes(graph_after, N_new_node_id, N_left, "E"),
            hyperedge_by_2_nodes(graph_after, N_new_node_id, N_top, "N"),
            hyperedge_by_2_nodes(graph_after, N_new_node_id, N_right, "W"),
            hyperedge_by_2_nodes(graph_after, N_new_node_id, N_bottom, "S")
        ]

        expected_connections = set(graph_after[N_new_node_id])
        actual_connections = set(I + direction_hyperedges)
        self.assertEqual(expected_connections, actual_connections)

        W_new_node_data = {'is_hyperedge': False,
                           'x': 99, 'y': 199, 'r': 1, 'g': 164, 'b': 243}
        W_new_node_id = id_by_data(graph_after, W_new_node_data)
        self.assertIn(W_new_node_data, new_nodes_data)

        W_left = get_node_id((0, 199))
        W_top = N_left
        W_right = N_bottom
        W_bottom = get_node_id((99, 99))

        I = [
            hyperedge_by_2_nodes(graph_after, W_left, W_top, "I"),
            hyperedge_by_2_nodes(graph_after, W_top, W_right, "I"),
            hyperedge_by_2_nodes(graph_after, W_right, W_bottom, "I"),
            hyperedge_by_2_nodes(graph_after, W_bottom, W_left, "I")
        ]

        direction_hyperedges = [
            hyperedge_by_2_nodes(graph_after, W_new_node_id, W_left, "W"),
            hyperedge_by_2_nodes(graph_after, W_new_node_id, W_top, "S"),
            hyperedge_by_2_nodes(graph_after, W_new_node_id, W_right, "E"),
            hyperedge_by_2_nodes(graph_after, W_new_node_id, W_bottom, "N")
        ]

        expected_connections = set(graph_after[W_new_node_id])
        actual_connections = set(I + direction_hyperedges)
        self.assertEqual(expected_connections, actual_connections)

    def test_on_bad_input_raise_exception_and_dont_change_graph(self):
        graph_copy = self.graph.copy()
        incorrect_nodes = set(graph_copy.nodes()).difference(set([self.W]))

        for n in incorrect_nodes:
            with self.assertRaises(Exception):
                P4(self.graph, n, self.image)
            self.assertTrue(nx.is_isomorphic(graph_copy, self.graph))

    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)

        width, height = self.image.size

        P1(self.graph, x_max_idx=width - 1,
           y_max_idx=height - 1, image=self.image)
        i_hyperedges_ids = self.__hyperedges_ids(HyperEdge.I)
        P5(self.graph, i_hyperedges_ids[0], self.image)
        P2(self.graph, i_hyperedges_ids[0], self.image)

        i_hyperedges_ids = self.__hyperedges_ids(HyperEdge.I)
        for i_hyperedge in i_hyperedges_ids[:3]:
            P5(self.graph, i_hyperedge, self.image)

        self.hyp_fs = [(x, y) for x, y in self.graph.nodes(
            data=True) if 'label' in y.keys() and y['label'] in [d.name for d in Direction]]
        self.hyp_bs = [(x, y) for x, y in self.graph.nodes(
            data=True) if 'label' in y.keys() and y['label'] == 'B']
        self.hyp_is = [(x, y) for x, y in self.graph.nodes(
            data=True) if 'label' in y.keys() and y['label'] == 'I']
        self.hyperedges = {
            Direction.N: {},
            Direction.S: {},
            Direction.E: {},
            Direction.W: {},
        }
        for direction, edges in self.hyperedges.items():
            edges['f'] = [x for x in self.hyp_fs if x[1]
                          ['label'] == direction.name][0]
            edges['b'] = [(x, y) for x, y in self.hyp_bs if B_DIRECTION_EDGE_LAMBDAS[direction](
                y, edges['f'][1])][0]

            f_neighbour = list(self.graph.neighbors(edges['f'][0]))[0]
            b_neighbours = list(self.graph.neighbors(edges['b'][0]))
            edges['is'] = []
            for x, y in self.graph.nodes(data=True):
                if 'label' in y and y['label'] == 'I':
                    i_neighbours = list(self.graph.neighbors(x))

                    if f_neighbour in i_neighbours and (b_neighbours[0] in i_neighbours or b_neighbours[1] in i_neighbours):
                        edges['is'].append((x, y))

        for _, edges in self.hyperedges.items():
            P3(self.graph, edges['b'][0], [
               x for x, y in edges['is']], edges['f'][0], self.image)

        for i_hyperedge in i_hyperedges_ids[:3]:
            P2(self.graph, i_hyperedge, self.image)

        self.N = [i for i, d in self.graph.nodes(data=True) if d.get(
            "label", None) == "N" and d["y"] == 299.0][0]

        self.W = [i for i, d in self.graph.nodes(data=True) if d.get(
            "label", None) == "W" and d["x"] == 99.0][0]

    def __hyperedges_ids(self, label):
        return [idd for idd, data in self.__hyperedges(label)]

    def __hyperedges(self, label):
        return [(idd, data) for idd, data in self.graph.nodes(data=True)
                if 'label' in data.keys() and data['label'] == label.name]
