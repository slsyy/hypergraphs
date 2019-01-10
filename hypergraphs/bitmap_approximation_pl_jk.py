APPROX_R = None
APPROX_G = None
APPROX_B = None


def run(graph, max_x, max_y):
    initialize_approx(max_x, max_y)
    i_hyperedges = [(node_id, node_data) for node_id, node_data in graph.nodes(data=True) if __is_hyperedge_i(node_data)]

    for node_id, node_data in i_hyperedges:
        neighbors_data = list(graph.node(neighbor_id) for neighbor_id in graph.neighbors(node_id))
        xs = [neighbor_data['x'] for neighbor_data in neighbors_data]
        ys = [neighbor_data['y'] for neighbor_data in neighbors_data]
        xs.sort()
        ys.sort()
        x1 = min(xs)
        x2 = max(xs)
        y1 = min(ys)
        y2 = max(ys)

        sorted_neighbors_data = __sorted_neighbors_data(neighbors_data, x1, x2, y1, y2)
        rs = [data['r'] for data in sorted_neighbors_data]
        gs = [data['g'] for data in sorted_neighbors_data]
        bs = [data['b'] for data in sorted_neighbors_data]

        approximate_single((x1, y1), (x2, y2), rs, gs, bs)


def initialize_approx(image_width, image_height):
    global APPROX_R
    global APPROX_G
    global APPROX_B
    APPROX_R = [[0.0] * image_height] * image_width
    APPROX_G = [[0.0] * image_height] * image_width
    APPROX_B = [[0.0] * image_height] * image_width


def approximate_single(p1, p2, rs, gs, bs):
    global APPROX_R
    global APPROX_G
    global APPROX_B
    x1, y1 = p1
    x2, y2 = p2

    for px in (x1, x2):
        for py in (y1, y2):
            c1 = (1 - (px - x1) / (x2 - x1)) * ((py - y1) / (y2 - y1))
            APPROX_R[px][py] += rs[0] * c1
            APPROX_G[px][py] += gs[0] * c1
            APPROX_B[px][py] += bs[0] * c1

            c2 = ((px - x1) / (x2 - x1)) * ((py - y1) / (y2 - y1))
            APPROX_R[px][py] += rs[1] * c2
            APPROX_G[px][py] += gs[1] * c2
            APPROX_B[px][py] += bs[1] * c2

            c3 = (1 - (px - x1) / (x2 - x1)) * (1 - (py - y1) / (y2 - y1))
            APPROX_R[px][py] += rs[2] * c3
            APPROX_G[px][py] += gs[2] * c3
            APPROX_B[px][py] += bs[2] * c3

            c4 = ((px - x1) / (x2 - x1)) * (1 - (py - y1) / (y2 - y1))
            APPROX_R[px][py] += rs[3] * c4
            APPROX_G[px][py] += gs[3] * c4
            APPROX_B[px][py] += bs[3] * c4


def __is_hyperedge_i(data):
    return data['is_hyperedge'] and data['label'] == 'I'


def __sorted_neighbors_data(neighbors_data, x1, x2, y1, y2):
    return sorted(neighbors_data, key=lambda data: __neighbor_number(data, x1, x2, y1, y2))


def __neighbor_number(data, x1, x2, y1, y2):
    x, y = data['x'], data['y']
    if x == x1:
        if y == y2:
            return 1
        if y == y1:
            return 3

    if x == x2:
        if y == y2:
            return 2
        if y == y1:
            return 4
