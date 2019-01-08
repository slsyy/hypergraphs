import os
from typing import Tuple

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "tests/test_data", "four_colors.jpg")


def get_node_id(node_position: Tuple[int, int]) -> int:
    """
    :param node_position: a tuple containing x and y coordinates of a node
    :return: node id, a hash of node position
    """
    return hash(node_position)


def convert_to_hex(rgba: Tuple[int, int, int, int]) -> str:
    return '#%02x%02x%02x' % rgba[:3]
