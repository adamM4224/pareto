
import networkx as nx
from random import randint
import copy
import math
import numpy as np
from pareto.grid import grids_are_equal, grid_is_valid, grid_meta
import math
from pareto.log import getLogger 


logging = getLogger('gridLogger')

def get_candidates(point, radius, unit_length, grid_width, grid_height):
    """
    Given a point corresponding to a tree node, find all indices in the grid
    array that lie within distance radius to the point

    Parameters
        point: (float, float)
        radius: float 
        unit_length: float
        grid_width: float
        grid_height: float

    Returns
        [(i, j), .....]
    """
    num_cols = int(grid_width // unit_length)
    num_rows = int(grid_height // unit_length)
    
    x, y = point  # point coordinates in cm
    
    # Determine the bounding indices (clamped to grid dimensions)
    min_i = max(0, int((x - radius) // unit_length))
    max_i = min(num_cols - 1, int((x + radius) // unit_length))
    min_j = max(0, int((y - radius) // unit_length))
    max_j = min(num_rows - 1, int((y + radius) // unit_length))
    
    cells = []
    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            # Compute the center coordinates of cell (i, j)
            center_x = i * unit_length + unit_length / 2
            center_y = j * unit_length + unit_length / 2
            
            # Calculate the distance from the cell center to the given point.
            dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
            
            if dist <= radius:
                cells.append((i, j))
                
    return cells




def coverage(tree, grid, radius, unit_length, grid_width, grid_height):
    """
    Coverage needs to return the number of nutrients. 
    It should take a grid of nutrients, and a radius r. 
    
    Each node will look around the radius and accept any nutrient. 
    The function should return the score and the nutrients so the 
    transport score can be computed.

    Params: 
        tree: nx graph of the plant
        grid: a grid of nutrients of the structure [[{nutrient: boolean, available: boolean}, ...]]
            - nutrient: if a nutrient is at that location
            - available: if a nutrient is available and has not been used.
        radius: distance 
    """
    # orient the root of the tree to the top center index
    n_rows = len(grid)
    n_cols = len(grid[0])
    curr_i = int(n_rows / 2)
    curr_j = 0

    root = (0, 0)
    # iterate through the nodes and bfs order and compute the nutrients
    nodes = nx.bfs_tree(tree, root)
    nutrients = []
    for i, ni in enumerate(nodes):
        x = ni[0]
        y = ni[1]
        node_attr = tree.nodes[ni]
        nid = node_attr['id']
            
        # get the nutrients asssociated with x, y and 
        candidate_indices = get_candidates((x, y), radius, unit_length, grid_width, grid_height)
        nutrients_this_iteration = []
        for i, j in candidate_indices:

            cell = grid[i][j]

            if cell['nutrient'] and cell['available']:
                nutrients_this_iteration.append(1)
                cell['available'] = False
                cell['acquired_by_node_id'] = nid
                
        nutrients.append(sum(nutrients_this_iteration))
    
    return sum(nutrients)