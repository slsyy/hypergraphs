from unittest import TestCase

import networkx as nx
from PIL import Image

from hypergraphs.productions import P1
from hypergraphs.utils import IMAGE_PATH


class TestP1(TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)
        width, height = self.image.size
        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
        self.sorted_nodes_with_data = sorted(self.graph.nodes(data=True), key=lambda x: (x[1]['x'], x[1]['y']))

    def test_sets_correct_attributes(self):

        width, height = self.image.size
        max_x, max_y = width - 1, height - 1

        # check node attributes
        expected_node_attributes = (
            {'x': 0, 'y': 0, 'is_hyperedge': False},
            {'is_hyperedge': True, 'label': 'B', 'x': 0, 'y': 199},
            {'x': 0, 'y': max_y, 'is_hyperedge': False},
            {'is_hyperedge': True, 'label': 'B', 'x': 199, 'y': 0},
            {'is_hyperedge': True, 'label': 'I', 'should_break': 0, 'x': 199, 'y': 199},
            {'is_hyperedge': True, 'label': 'B', 'x': 199, 'y': 399},
            {'x': max_x, 'y': 0, 'is_hyperedge': False},
            {'is_hyperedge': True, 'label': 'B', 'x': 399, 'y': 199},
            {'x': max_x, 'y': max_y, 'is_hyperedge': False},
        )

        for node_index in range(self.graph.number_of_nodes()):
            (node_id, node_data) = self.sorted_nodes_with_data[node_index]
            expected_attrs = expected_node_attributes[node_index]

            for attr_key, attr_val in expected_attrs.items():
                self.assertEqual(
                    attr_val,
                    node_data[attr_key],
                    msg="{} attr was not correct in node #{}".format(attr_key, node_index),
                )

    def test_sets_correct_node_connections(self):
        # a list specifying which nodes in self.sorted_nodes_with_data should be connected
        node_connections = (
            (0, 1),
            (1, 2),
            (0, 3),
            (3, 6),
            (2, 5),
            (5, 8),
            (6, 7),
            (7, 8),
            (0, 4),
            (2, 4),
            (6, 4),
            (8, 4),
        )

        node_ids = [node_id for node_id, _ in self.sorted_nodes_with_data]
        for u_index, v_index in node_connections:
            u = node_ids[u_index]
            v = node_ids[v_index]

            self.assertTrue(
                self.graph.has_edge(u, v),
                msg="Nodes number {} and {} were not connected".format(u_index, v_index),
            )

        self.assertEqual(len(node_connections), self.graph.number_of_edges())

    # def test_draw(self):
    #     from plot import plot
    #     plot(self.graph)
