import os
from unittest import TestCase

import networkx as nx
from PIL import Image

from productions import Direction
from productions import P1
from productions import P2
from productions import P3
from utils import get_node_id

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "test_data", "four_colors.jpg")


class TestP3(TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)
        width, height = self.image.size
        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
        hyperedge = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'I'][0]
        hyperedge[1]['should_break'] = 1
        self.graph.add_node(hyperedge[0], **hyperedge[1])
        P2(self.graph, hyperedge_id=self.hyperedge[0], image=self.image)

        plot(self.graph)
        P3(self.graph, hyperedge_id=self.hyperedge[0], image=self.image)
        plot(self.graph)

        # self.hyperedge = self.prepare_graph_and_get_central_hyperedge()
        # self.added_node_position = (self.hyperedge[1]['x'], self.hyperedge[1]['y'])
        # self.added_node_id = get_node_id(self.added_node_position)
        #
        # # self.sorted_nodes_with_data = sorted(self.graph.nodes(data=True), key=lambda x: (x[1]['x'], x[1]['y']))
        # plot(self.graph)

    # def prepare_graph_and_get_central_hyperedge(self):
    #     # width, height = self.image.size
    #     # P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
    #     # hyperedges_to_remove = [x for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'B']
    #     for id in hyperedges_to_remove:
    #         self.graph.remove_node(id)
    #     hyperedge = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'I'][0]
    #     hyperedge[1]['should_break'] = 1
    #     self.graph.add_node(hyperedge[0], **hyperedge[1])
    #     return hyperedge

    def test_if_hyperedge_was_removed(self):
        self.assertTrue(self.hyperedge[0] not in self.graph.node)

    # def test_if_node_was_added_properly(self):
    #     self.assertTrue(self.added_node_id in self.graph.node)
    #     width, height = self.image.size
    #     node = self.graph.node[self.added_node_id]
    #     self.assertEqual(width / 2 - 1, node['x'])
    #     self.assertEqual(height / 2 - 1, node['y'])
    #
    # def test_if_hyperedges_between_nodes_were_added_properly(self):
    #     hyperedge_ids = [idd for idd, data in self.graph.nodes(data=True) if
    #                      'label' in data.keys() and data['label'] == 'I']
    #     hyperedge_positions = [(data['x'], data['y']) for idd, data in self.graph.nodes(data=True) if
    #                            'label' in data.keys() and data['label'] == 'I']
    #     self.assertEqual(len(hyperedge_positions), 4)
    #     expected_positions = [
    #         (99, 99),
    #         (99, 299),
    #         (299, 99),
    #         (299, 299)
    #     ]
    #     for hyperedge_id, hyperedge_position in zip(hyperedge_ids, hyperedge_positions):
    #         self.assertTrue(hyperedge_position in expected_positions)
    #         self.assertEqual(len(self.graph[hyperedge_id]), 2)
    #         expected_node_position = self.count_position_of_second_point(hyperedge_position, self.added_node_position)
    #         print(expected_node_position)
    #         # self.assertTrue(get_node_id(expected_node_position) in self.graph[hyperedge_id])
    #         self.assertTrue(expected_node_position is not self.added_node_position)
    #
    # def test_if_direction_hyperedges_were_added_properly(self):
    #     hyperedge_ids = [idd for idd, data in self.graph.nodes(data=True) if
    #                      'label' in data.keys() and data['label'] in Direction]
    #     hyperedge_positions = [(data['x'], data['y']) for idd, data in self.graph.nodes(data=True) if
    #                            'label' in data.keys() and data['label'] in Direction]
    #     self.assertEqual(len(hyperedge_positions), 4)
    #     expected_positions = [
    #         (99, 199),
    #         (299, 199),
    #         (199, 99),
    #         (199, 299)
    #     ]
    #     for hyperedge_id, hyperedge_position in zip(hyperedge_ids, hyperedge_positions):
    #         self.assertTrue(hyperedge_position in expected_positions)
    #         self.assertEqual(len(self.graph[hyperedge_id]), 1)
    #         self.assertTrue(self.added_node_id in self.graph[hyperedge_id])
    #
    # @staticmethod
    # def count_position_of_second_point(avg_point, first_point):
    #     return (
    #         TestP2.count_second_element_of_two_element_average(avg_point[0], first_point[0]),
    #         TestP2.count_second_element_of_two_element_average(avg_point[1], first_point[1])
    #     )
    #
    # @staticmethod
    # def count_second_element_of_two_element_average(avg, first):
    #     second = 2 * avg - first
    #     if second < 0:
    #         return 0
    #     else:
    #         return second
