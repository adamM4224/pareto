import math 
import networkx as nx
from pareto.grid import grid_ids

def euclidean_distance(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

distance = euclidean_distance
def path_distance(tree, root, node):
    path = nx.shortest_path(tree, source=root, target=node)
    return sum(
        distance(path[i-1], path[i]) for i in range(1, len(path))
    )

def find_node_by_id(G, search_id):
    for node, attrs in G.nodes(data=True):
        if attrs.get('id') == search_id:
            return node, attrs
    raise ValueError(f"NODE ID: {search_id} not found. This should not happen.")


def transport(tree, grid):
    """"
    For each nutrient in the grid. Find its corresponding node in the 
    tree and compute the distance to the root of the tree.

    Parameters:
        tree: nx.DiGraph()
        grid: a valid grid as described in grid.py
    """
    flat_grid = [item for sublist in grid for item in sublist]
    ids = [ki['acquired_by_node_id'] for ki in flat_grid if 'acquired_by_node_id' in ki]
    
    nutrients_by_id = {ki: [] for ki in ids}
    
    root = (0, 0)
    total_distance = 0
    for row in grid:
        for cell in row:
            if 'acquired_by_node_id' in cell:
                nutrients_by_id[cell['acquired_by_node_id']].append(cell)

    for segment_group in nutrients_by_id:
        target = None
        for node, data in tree.nodes(data=True):
            if data.get('id') == segment_group:
                target = node
                break
        if not target:
            print('returning early for not finding a node with the id, but this should not happen')

        total_distance += path_distance(tree, root, target)

    return total_distance
