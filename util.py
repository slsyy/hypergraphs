def get_node_id(node_positions):
    '''

    :param node_positions: dict, where x and y keys represent x,y positions
    :return: node id, which is a hash of node position
    '''
    return hash((node_positions['x'], node_positions['y']))
