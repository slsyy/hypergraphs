import os
import uuid
from unittest import TestCase

from matplotlib import pyplot as plt
import networkx as nx
from PIL import Image

from productions import P4


from plot import plot_but_dont_show
from utils import *


IMAGE_PATH = os.path.join(os.path.dirname(
    __file__), "test_data", "four_colors.jpg")


class TestP4(TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)

    def test_show_plot(self):
        self.__create_test_graph()

        plt.subplot(121)
        plt.title("Before")
        plot_but_dont_show(self.graph)

        P4(self.graph, self.f1_c, self.image)

        plt.subplot(122)
        plt.title("After")
        plot_but_dont_show(self.graph)

        plt.show()

    def test_production(self):
        self.__create_test_graph()

        graph_before = self.graph.copy()
        P4(self.graph, self.f1_c, self.image)

        # F1 ids are generated randomly, so I extract them from the result graph
        new_f1 = [n for n in self.graph if self.graph.node[n].get(
            "label", None) == "F1"]
        self.assertEqual(2, len(new_f1))
        new_top_f1, new_bottom_f1 = sorted(
            new_f1, key=lambda x: self.graph.node[x]["y"])

        graph_before.remove_node(self.f1_c)

        new_node_id = get_node_id((200, 200))
        graph_before.add_node(
            new_node_id,
            is_hyperedge=False,
            x=200,
            y=200,
            r=144,
            g=182,
            b=71
        )

        graph_before.add_node(
            new_top_f1,
            is_hyperedge=True,
            x=200,
            y=115,
            label=HyperEdge.F1.name
        )

        graph_before.add_node(
            new_bottom_f1,
            is_hyperedge=True,
            x=200,
            y=285,
            label=HyperEdge.F1.name
        )

        graph_before.add_edge(new_top_f1, self.t_node)
        graph_before.add_edge(new_bottom_f1, self.b_node)

        graph_before.add_edge(new_node_id, new_top_f1)
        graph_before.add_edge(new_node_id, new_bottom_f1)
        graph_before.add_edge(new_node_id, self.tl_I)
        graph_before.add_edge(new_node_id, self.tr_I)
        graph_before.add_edge(new_node_id, self.bl_I)
        graph_before.add_edge(new_node_id, self.br_I)
        graph_before.add_edge(new_node_id, self.f2_l)
        graph_before.add_edge(new_node_id, self.f2_r)

        self.assertTrue(nx.is_isomorphic(graph_before, self.graph))

    def test_throw_exception_on_bad_input(self):
        self.__create_test_graph()

        with self.assertRaises(Exception):
            P4(self.graph, "blablabla", self.image)

        with self.assertRaises(Exception):
            P4(self.graph, self.f2_r, self.image)

        with self.assertRaises(Exception):
            P4(self.graph, self.t_node, self.image)

    def __create_test_graph(self):
        width, height = self.image.size

        c_x, c_y = width//2, height//2

        he_offset = int(min(width, height) * 0.3)
        node_multiplier = 2 ** 0.5

        self.f1_c = self.__add_hyperedge(x=c_x, y=c_y, label="F1")
        self.f2_l = self.__add_hyperedge(x=c_x - he_offset, y=c_y, label="F2")
        self.f2_r = self.__add_hyperedge(x=c_x + he_offset, y=c_y, label="F2")

        self.tl_I = self.__add_hyperedge(
            x=c_x - he_offset, y=c_y + he_offset, label="I")
        self.tr_I = self.__add_hyperedge(
            x=c_x + he_offset, y=c_y + he_offset, label="I")
        self.bl_I = self.__add_hyperedge(
            x=c_x - he_offset, y=c_y - he_offset, label="I")
        self.br_I = self.__add_hyperedge(
            x=c_x + he_offset, y=c_y - he_offset, label="I")

        self.t_node = self.__add_node(
            x=c_x, y=c_y + he_offset * node_multiplier)
        self.b_node = self.__add_node(
            x=c_x, y=c_y - he_offset * node_multiplier)

        self.l_node = self.__add_node(
            x=c_x - he_offset * node_multiplier, y=c_y)
        self. r_node = self.__add_node(
            x=c_x + he_offset * node_multiplier, y=c_y)

        self.tl_node = self.__add_node(
            x=c_x - he_offset * node_multiplier, y=c_y + he_offset * node_multiplier)
        self.tr_node = self.__add_node(
            x=c_x + he_offset * node_multiplier, y=c_y + he_offset * node_multiplier)
        self.bl_node = self.__add_node(
            x=c_x - he_offset * node_multiplier, y=c_y - he_offset * node_multiplier)
        self.br_node = self.__add_node(
            x=c_x + he_offset * node_multiplier, y=c_y - he_offset * node_multiplier)

        self.graph.add_edge(self.f1_c, self.t_node)
        self.graph.add_edge(self.f1_c, self.b_node)

        self.graph.add_edge(self.f2_l, self.l_node)
        self.graph.add_edge(self.f2_r, self.r_node)

        self.graph.add_edge(self.tl_I, self.tl_node)
        self.graph.add_edge(self.tl_I, self.l_node)
        self.graph.add_edge(self.tl_I, self.t_node)

        self.graph.add_edge(self.tr_I, self.tr_node)
        self.graph.add_edge(self.tr_I, self.r_node)
        self.graph.add_edge(self.tr_I, self.t_node)

        self.graph.add_edge(self.bl_I, self.bl_node)
        self.graph.add_edge(self.bl_I, self.l_node)
        self.graph.add_edge(self.bl_I, self.b_node)

        self.graph.add_edge(self.br_I, self.br_node)
        self.graph.add_edge(self.br_I, self.r_node)
        self.graph.add_edge(self.br_I, self.b_node)

    def __add_node(self, **kwargs):
        position = (kwargs["x"], kwargs["y"])
        rgb = self.image.getpixel(((kwargs["x"], kwargs["y"])))

        node_id = get_node_id(position)
        self.graph.add_node(
            node_id,
            is_hyperedge=False,
            **kwargs,
            r=rgb[0],
            g=rgb[1],
            b=rgb[2]
        )
        return node_id

    def __add_hyperedge(self, **kwargs):
        node_id = uuid.uuid4()
        self.graph.add_node(
            node_id,
            is_hyperedge=True,
            **kwargs
        )
        return node_id
